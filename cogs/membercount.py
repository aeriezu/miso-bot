import discord
from discord import app_commands
from discord.ext import commands
from main import client

class membercount(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "membercount",
      description = "shows to membercount of the server",
    )

    async def membercount(
      self,
      interaction: discord.Interaction,
    ):
      member = await client.fetch_user(interaction.user.id)
      true_member_count = len([m for m in interaction.guild.members if not m.bot]) # type: ignore
      em = discord.Embed(description = f"**members**\n> {true_member_count}")
      em.set_author(name=interaction.guild.name, icon_url=member.display_avatar.url) # type: ignore
      em.set_thumbnail(url=interaction.guild.icon.url) # type: ignore
      em.timestamp = discord.utils.utcnow()
      await interaction.response.send_message(embed=em)
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    membercount(bot)
  )