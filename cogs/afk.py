import discord
from discord import app_commands
from discord.ext import commands
from main import client
from PIL import Image, ImageFont, ImageDraw
import requests

class afk(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "afk",
      description = "go afk",
    )

    async def afk(
      self,
      interaction: discord.Interaction,
      reason: str = None # type: ignore
    ):
      if reason == None:
        reason = "reason not provided"
      #get db
      async with client.db.cursor() as cursor: # type: ignore
        await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (interaction.user.id, interaction.user.guild.id,)) # type: ignore
        data = await cursor.fetchone()
        if data:
          if data[0] != "":
            return await interaction.response.send_message("You are already afk!", ephemeral = True)
          await cursor.execute("UPDATE afk SET reason = ? WHERE user = ? AND guild = ?", (reason, interaction.user.id, interaction.user.id,))
        else:
          img = Image.open(requests.get(interaction.user.display_avatar.url, stream=True).raw).convert('RGB') # type: ignore
          dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
          await cursor.execute("INSERT INTO afk (user, guild, reason) VALUES (?, ?, ?)", (interaction.user.id, interaction.user.guild.id, reason,)) # type: ignore
          em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description = f"you are now **afk**\nreason - **`{reason}`**") # type: ignore
          em.set_author(name=f'{interaction.user.display_name}', icon_url=interaction.user.display_avatar.url)
          em.set_thumbnail(url=interaction.user.display_avatar.url)
          em.timestamp = discord.utils.utcnow()
          try:
            await interaction.user.edit(nick = f"[afk] {interaction.user.display_name}") # type: ignore
          except:
            pass
          await interaction.response.send_message(embed=em)
      await client.db.commit() # type: ignore
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    afk(bot)
  )