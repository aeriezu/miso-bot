import discord
from discord import app_commands
from discord.ext import commands
from main import client

class info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "ping",
      description = "get the bot's ping",
    )

    async def ping(
      self,
      interaction: discord.Interaction,
    ):
      member = await client.fetch_user(interaction.user.id)
      em = discord.Embed(description = f"> loading . . .")
      em.set_author(name=f'{interaction.user}', icon_url=interaction.user.display_avatar.url)
      em.set_thumbnail(url=interaction.client.user.avatar.url) # type: ignore
      em.timestamp = discord.utils.utcnow()
      await interaction.response.send_message(embed=em)
      bot_ping = round(client.latency * 1000)
      em = discord.Embed(description = f"> pong! :eyes: \n```{bot_ping} ms . . .```")
      em.set_author(name=f'{interaction.user.display_name}', icon_url=member.display_avatar.url)
      em.set_thumbnail(url=interaction.client.user.avatar.url) # type: ignore
      em.timestamp = discord.utils.utcnow()
      await interaction.edit_original_response(embed=em)
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    info(bot)
  )