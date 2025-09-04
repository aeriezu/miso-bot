#################################
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import os, sys, random
import main
import json
from json import loads, dumps
from time import strftime, sleep
from discord import Webhook, Embed
from os import listdir
from itertools import cycle
import aiosqlite
import aiohttp
from os import system
from PIL import Image, ImageFont, ImageDraw
import requests

#################################

class MyBot(commands.Bot):
  def __init__(self):
    super().__init__(
      command_prefix = 'miso ',
      intents = discord.Intents().all(),
      application_id = os.getenv('id'))

    self.initial_extensions = ['cogs.info', 'cogs.userinfo', 'cogs.afk', 'cogs.color', 'cogs.membercount', 'cogs.interact', 'cogs.embed', 'cogs.emoji', 'cogs.owner', 'cogs.sticky']
  
  async def setup_hook(self):
    self.session = aiohttp.ClientSession()
    self.db = await aiosqlite.connect("main.db")

    for ext in self.initial_extensions:
      await self.load_extension(ext)
      print(f"extention: {ext} has loaded")
    
    await client.tree.sync()

client = MyBot()
#status = cycle(['with fqiry!', "drummin'!"])

#########################

def remove_afk(nick: str) -> str:
  prefix = "[afk] "
  if nick and nick.lower().startswith(prefix):
    return nick[len(prefix):]
  else:
    return nick
    
@client.event
async def on_message(message):
  if message.author.bot:
    return
  async with client.db.cursor() as cursor: # type: ignore
    await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id,))
    data = await cursor.fetchone()
    if data:
      try:
        nickname = remove_afk(message.author.display_name)
        await message.author.edit(nick = nickname)
      except:
        pass
      img = Image.open(requests.get(message.author.display_avatar.url, stream=True).raw).convert('RGB') # type: ignore
      dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
      em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description = f"afk removed...\nwelcome back!") # type: ignore
      em.set_author(name=f'{message.author.display_name}', icon_url=message.author.display_avatar.url)
      em.set_thumbnail(url=message.author.display_avatar.url)
      em.timestamp = discord.utils.utcnow()
      await message.channel.send(f"{message.author.mention}", embed=em, delete_after=10)
      await cursor.execute("DELETE FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id,))
    if message.mentions:
      for mention in message.mentions:
        await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (mention.id, message.guild.id,))
        data2 = await cursor.fetchone()
        if data2 and mention.id != message.author.id:
          img = Image.open(requests.get(message.author.display_avatar.url, stream=True).raw).convert('RGB') # type: ignore
          dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
          em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description = f"{mention.mention} is currently **afk**\nreason - **`{data2[0]}`**") # type: ignore
          em.set_author(name=f'{message.author.display_name}', icon_url=message.author.display_avatar.url)
          em.set_thumbnail(url=mention.display_avatar.url)
          em.timestamp = discord.utils.utcnow()
          await message.channel.send(embed=em)
  await client.db.commit() # type: ignore
  await client.process_commands(message)
  
#########################

@client.event
async def on_ready():
  #change_status.start()
  print(f'{client.user} is online!')

  async with client.db.cursor() as cursor: # type: ignore
    await cursor.execute("CREATE TABLE IF NOT EXISTS afk (user INTEGER, guild INTERGER, reason TEXT)")
    await cursor.execute("CREATE TABLE IF NOT EXISTS sticky_messages (channel INTEGER PRIMARY KEY, message TEXT, last_message_id INTEGER)")
  await client.db.commit()

  activity = discord.Activity(type=discord.ActivityType.playing, name="with ae!")
  await client.change_presence(status = discord.Status.idle, activity=activity)

#loop status
#@tasks.loop(seconds=60)
#async def change_status():
  #status_set = next(status)

  #if status_set == 'with fqiry!':
    #await client.change_presence(status = discord.Status.idle, activity=discord.Game(name='with fqiry!'))
  #if status_set == "drummin'!":
    #await client.change_presence(status = discord.Status.idle, activity=discord.Streaming(name="drummin'!", url="https://www.youtube.com/watch?v=AE7CbOAc3no&ab_channel=TO1"))

#########################

try:
    client.run(os.getenv('token')) # type: ignore
except discord.errors.HTTPException:
    system('kill 1')