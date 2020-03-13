'''
Main file for the cog
'''

# Imports
# import discord
from discord.ext import commands

class HelloWorld(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(HelloWorld(bot))