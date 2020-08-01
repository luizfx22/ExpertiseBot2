# Imports
import discord
import random
import time
from discord.ext import commands, tasks
from discord import Guild, Role, utils

class Management(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.up_emoji = '⬆️'
    self.down_emoji = '⬇️'
    self.reactions = []
    self.target_votes = 0
    self.target_time = None
    self.target_user = None
    self.total_votes = 0
    self.move_to = None
    self.return_to = None
    self.ban_request = None

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    react = {
      "reaction": reaction,
      "user": user
    }

    last_reaction = next((item for item in self.reactions if item["user"] == user), None)

    if (last_reaction != None) and (user.id != reaction.message.author.id):
      await reaction.message.remove_reaction(last_reaction["reaction"], last_reaction["user"])
      self.reactions.append(react)
      self.reactions.remove(last_reaction)

    else:
      if user.id != reaction.message.author.id:
        self.reactions.append(react)

    ress = len([item for item in self.reactions if item['reaction'].emoji == self.up_emoji])

    self.total_votes = ress

    if ress >= self.target_votes:
      await reaction.message.channel.send(f"Voting reached the votes needed ({ress} votes)!")
    
      self.countdown_vote_timer.stop()

      await self.target_user.move_to(self.move_to, reason="LOL")
      time.sleep(5)
      await self.target_user.move_to(self.return_to, reason="Don't do this anymore!")
      await self.ban_request.delete()

  @tasks.loop(seconds=1.0)
  async def countdown_vote_timer(self, ctx, message):
    print(self.target_time)

    self.target_time -= 1

    if self.target_time == 30.0:
      msg = await ctx.send('30 seconds left!')
      await msg.delete(delay=5)

    if self.target_time == 10.0:
      msg = await ctx.send('10 seconds left!')
      await msg.delete(delay=5)
    
    if self.target_time == 5.0:
      msg = await ctx.send('5 seconds left!')
      await msg.delete(delay=5)

    if self.target_time == 0:
      await message.delete()
      msg = await ctx.send(f'Voting ended! With insuficient votes!')
      await msg.delete(delay=5)
      await self.ban_request.delete()
      self.countdown_vote_timer.stop()

  @commands.command(name='ban', pass_context=True)
  async def ban(self, ctx, member: discord.Member, target: int = 2, timeout: float = 2.0):
    self.target_votes = target
    self.target_time = timeout
    self.target_user = member
    self.ban_request = ctx.message

    voice_channel_id = ctx.message.author.voice

    if not voice_channel_id:
      warning = await ctx.send(f"Sorry {ctx.message.author.mention}, it looks like you're not in a voice channel!")
      await warning.delete(delay=5)
      return False
        
    vc_users = utils.get(ctx.guild.voice_channels, id=voice_channel_id.channel.id)

    if vc_users != None:
      t_user = next((user for user in vc_users.members if user.id == member.id), None)
      if not t_user:
        await ctx.send(f"It looks like {member.mention} is not in your voice channel {ctx.message.author.mention}!")
        return False
    
    message = await ctx.send(f"Starting ban voting for {member.mention}. Minimum votes for ban {target}! Vote in {timeout} seconds to get it done!")

    await message.add_reaction(self.up_emoji)
    await message.add_reaction(self.down_emoji)

    # Select channel to move user to
    self.move_to = utils.get(ctx.guild.voice_channels, id=738903437252624385)
    self.return_to = utils.get(ctx.guild.voice_channels, id=voice_channel_id)
    
    self.countdown_vote_timer.start(ctx, message)

    await message.delete(delay=timeout)

  def cog_unload(self):
    self.countdown_vote_timer.cancel()

def setup(client):
  client.add_cog(Management(client))
