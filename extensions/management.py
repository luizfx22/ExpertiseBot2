# Imports
import discord
import random
import time
from discord.ext import commands, tasks
from discord import Guild, Role, utils

class Management(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(name='rename', pass_context=True)
  async def rename(self, ctx, new_name: str):
    server = ctx.message.guild

    server_members = server.members

    for user in server_members:
      try:
        await server.get_member(user.id).edit(nick=None)
      except Exception as e:
        continue

      time.sleep(.500)

  # def cog_unload(self):
  #   self.countdown_vote_timer.cancel()

def setup(client):
  client.add_cog(Management(client))
