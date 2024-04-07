from math import floor
import random
import time
import traceback
import requests
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import lib.words as words


def generate_string():
    # get a random word
    random_word = random.choice(words.example_words)
    # get a random length 3 substring from that word
    index = random.randint(0, len(random_word)-3)
    rand_sub = random_word[index:index + 3]
    return rand_sub.upper()
    
def check_word(word):
    # make request to dictionary api to check if word is valid
    dictionary_api = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    url = dictionary_api + word
    req = requests.get(url)
    j = (req.json())
    # invalid word requests contain a 'title' key in the json file response
    if 'title' in j:
        return False
    return True

class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # on ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Game command loaded')
    
    @app_commands.command(name='wordgame', description='play a word game!') # this is a slash command
    async def game(self, interaction:discord.Interaction):
        # defer the response because discord requires one in 15 seconds
        await interaction.response.defer(thinking=True)
        message_embed = discord.Embed(title='Word Game', description='React below to join!', color=discord.Color.green())
        # send the message
        await interaction.followup.send(embed=message_embed)
        msg = await interaction.original_response()
        await msg.add_reaction(":white_check_mark:")
        
        # wait 3 seconds
        for i in range(3):
            message_embed.description = f"React below to join!\nWaiting {3-i} seconds..."
            await asyncio.sleep(1)
            await msg.edit(embed=message_embed)
        
        # get all the players
        msg = await msg.fetch()
        players = []
        async for user in (msg.reactions[0].users()):
            if user.id != self.bot.user.id:
                players.append(user)

        # check if enough players joined
        if len(players) <= 1:
        # if len(players) < 1:   
            message_embed.description = f'Not enough players joined!'
            await msg.edit(embed=message_embed)
            return
        
        players_string = ', '.join([player.mention for player in players])
        message_embed.description = f'Starting game with {players_string}!'
        await msg.edit(embed=message_embed)
        await asyncio.sleep(2)
        
        # create 3 lives for each player
        player_lives = {player: 3 for player in players}
        
        # loop until a winner is found
        winner_found = False
        while not winner_found:
            for i in range(len(players)):
                # check if someone won and end the game
                if len(players) == 1:
                    message_embed.description = f'{players[0].mention} is the winner!'
                    await msg.edit(embed=message_embed)
                    winner_found = True
                    break
                # if player is out of lives, skip them
                if player_lives[players[i]] == 0:
                    continue
                # generate a string
                generated_string = generate_string()
                # wait 5 seconds for a response
                message_embed.description = f'{players[i].mention} write a word that contains: {generated_string}\nWaiting {5} seconds...'
                msg = await msg.reply(embed=message_embed)
                valid_word = False
                # check if word is valid
                start_time = floor(time.time())
                
                
                # function to change # of emojis in embed
                async def edit_timer(msg):
                    last_time_passed = 0
                    while True:
                        time_passed = floor(time.time() - start_time)
                        if time_passed != last_time_passed:
                            if time_passed >= 5:
                                break
                            message_embed.description = f'{players[i].mention} write a word that contains: {generated_string}\nWaiting {5-time_passed} seconds...\n{":coffee:"*(5-time_passed)}'
                            await msg.edit(embed=message_embed)
                            last_time_passed = time_passed
                    
                # function to check if message is valid
                def check(m):
                    return (m.author == players[i]) and (generated_string in m.content.upper()) and (check_word(m.content))
                try:
                    # task = asyncio.create_task(edit_timer(msg))
                    response = await self.bot.wait_for('message', check=check, timeout=5)
                    await response.add_reaction(":white_check_mark:") 
                    # task.cancel()
                    valid_word = True
                except asyncio.TimeoutError:
                    pass
                except Exception as e:
                    traceback.print_exc()
                # try:
                #     # check if word is valid
                #     def check(m):
                #         return (m.author == players[i]) and (generated_string in m.content.upper()) and (check_word(m.content))
                #     response = await self.bot.wait_for('message', check=check, timeout=5)
                #     # react to the message
                #     await response.add_reaction(":white_check_mark:") 
                    
                # player was unable to respond with a valid word in time
                # subtract a life
                # except asyncio.TimeoutError:
                if not valid_word:
                    player_lives[players[i]] -= 1
                    message_embed.description = f"{players[i].mention} ran out of time!\nLives left:{':heart:'*player_lives[players[i]] + ':broken_heart:'*(3-player_lives[players[i]])}"
                    # if player is out of lives, remove them from the game
                    if player_lives[players[i]] == 0:
                            message_embed.description = f'{players[i].mention} is out of lives!'
                            msg = await msg.reply(embed=message_embed)
                            players.remove(players[i])  
                    msg = await msg.reply(embed=message_embed)

# add cog to bot
async def setup(bot):
    await bot.add_cog(Game(bot))