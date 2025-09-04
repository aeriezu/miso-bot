"""
import discord
from discord import app_commands, Webhook
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import asyncio
import os, random
import json
from discord import Embed
from os import listdir
import time
from time import sleep
from main import client
from random import choice
import aiohttp
import re, typing
from typing import List

class embed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "embed",
      description = "create an embed",
    )

    @app_commands.describe(
      author_name = "input text for the author name (none if empty)",
      author_icon = "input a link for the author icon",
      title = "input text for title",
      description = "input text for description",
      color = "input hex code with or without # for color",
      footer_text = "input text for footer (none if empty)",
      footer_icon = "input a link for footer icon",
      thumbnail = "input link for thumbnail image",
      image = "input link for image",
      timestamp = "input true for timestamp or false for no timestamp (default is false)"
    )

    async def embed(
      self,
      interaction: discord.Interaction,
      description: str,
      author_name: str = None,
      author_icon: str = None,
      title: str = None,
      color: str = None,
      footer_text: str = None,
      footer_icon: str = None,
      thumbnail: str = None,
      image: str = None,
      timestamp: bool = False
    ):
      #get channel
      channel = interaction.channel

      #get color hex
      dec = None
      if color != None:
        if "#" in color:
          color = color.replace('#', '')
        dec = int(color, 16)

      #define variables
      a_icon = 0
      f_icon = 0
      t_icon = 0
      i_icon = 0

      #check if variables are valid links
      if author_icon != None:
        a_icon = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", author_icon)
      if footer_icon != None:
        f_icon = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", footer_icon)
      if thumbnail != None:
        t_icon = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", thumbnail)
      if image != None:
        i_icon = re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", image)

      if f_icon == None and a_icon == None and t_icon == None and i_icon == None:
        await interaction.response.send_message("Your author, footer, thumbnail, and image link is invalid!", ephemeral = True)
      elif f_icon == None and a_icon == None and t_icon == None:
        await interaction.response.send_message("Your author, footer, and thumbnail link is invalid!", ephemeral = True)
      elif f_icon == None and a_icon == None and i_icon == None:
        await interaction.response.send_message("Your author, footer, and image link is invalid!", ephemeral = True)
      elif f_icon == None and a_icon == None:
        await interaction.response.send_message("Your author and footer link is invalid!", ephemeral = True)
      elif a_icon == None and i_icon == None:
        await interaction.response.send_message("Your author and image link is invalid!", ephemeral = True)
      elif a_icon == None and t_icon == None:
        await interaction.response.send_message("Your author and thumbnail link is invalid!", ephemeral = True)
      elif f_icon == None and i_icon == None:
        await interaction.response.send_message("Your footer and image link is invalid!", ephemeral = True)
      elif f_icon == None and t_icon == None:
        await interaction.response.send_message("Your footer and thumbnail link is invalid!", ephemeral = True)
      elif t_icon == None and i_icon == None:
        await interaction.response.send_message("Your thumbnail and image image link is invalid!", ephemeral = True)
      elif a_icon == None:
        await interaction.response.send_message("Your author link is invalid!", ephemeral = True)
      elif f_icon == None:
        await interaction.response.send_message("Your footer link is invalid!", ephemeral = True)
      elif t_icon == None:
        await interaction.response.send_message("Your thumbnail link is invalid!", ephemeral = True)
      elif i_icon == None:
        await interaction.response.send_message("Your image link is invalid!", ephemeral = True)
      else:
        #define embed
        em = discord.Embed(title=title, description=description, color=dec)

        #check timestamp
        if timestamp:
          em.timestamp = discord.utils.utcnow()

        if author_name == None and author_icon == None:
          pass
        elif author_name != None and author_icon != None:
          em.set_author(name=author_name, icon_url=author_icon)
        elif author_name != None and author_icon == None:
          em.set_author(name=author_name, icon_url = None)
        elif author_name == None and a_icon != None:
          em.set_author(name=None, icon_url=author_icon)
        else:
          pass
        
        if footer_text == None and footer_icon == None:
          pass
        elif footer_text != None and footer_icon != None:
          em.set_footer(text=footer_text, icon_url=footer_icon)
        elif footer_text != None and footer_icon == None:
          em.set_footer(text=footer_text, icon_url = None)
        elif footer_text == None and f_icon != None:
          em.set_footer(text="None", icon_url=footer_icon)
        else:
          pass

        if thumbnail != None:
          em.set_thumbnail(url=thumbnail)

        if image != None:
          em.set_image(url=image)

        #send message
        await interaction.response.send_message("Sent!", ephemeral = True)
        await channel.send(embed=em)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    embed(bot)
  )
"""