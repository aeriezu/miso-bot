import discord
from discord import app_commands
from discord.ext import commands
from PIL import ImageColor

class color(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
  
    @app_commands.command(
      name = "color",
      description = "get info about a hex code color",
    )

    async def color(
      self,
      interaction: discord.Interaction,
      color: str
    ):
      if '#' in color:
        color = color.replace('#', '')
      dec = int(color, 16)
      image = f"https://serux.pro/rendercolour?hex={color}&height=100&width=225"
      get_rgb = ImageColor.getcolor(f"#{color}", "RGB")
      rgb = str(get_rgb)[1:-1]
        
      em = discord.Embed(color = dec)
      em.add_field(name="hex", value=f"```#{color}```")
      em.add_field(name="rgb", value=f"```{rgb}```")
      em.set_image(url=image)
      await interaction.response.send_message(embed=em)

    @app_commands.command(
      name = "rolecolor",
      description = "get color of a role",
    )

    async def rolecolor(
      self,
      interaction: discord.Interaction,
      role: discord.Role
    ):
      color = str(role.color)
      if '#' in color:
        color = color.replace('#', '')
      dec = int(color, 16)
      image = f"https://serux.pro/rendercolour?hex={color}&height=100&width=225"
      get_rgb = ImageColor.getcolor(f"#{color}", "RGB")
      rgb = str(get_rgb)[1:-1]
        
      em = discord.Embed(description = f"> {role.mention}", color = dec)
      em.add_field(name="hex", value=f"```#{color}```")
      em.add_field(name="rgb", value=f"```{rgb}```")
      em.set_image(url=image)
      await interaction.response.send_message(embed=em)

    @app_commands.command(
      name = "changerolecolor",
      description = "get color of a role",
    )
    
    @app_commands.checks.has_permissions(manage_roles=True)

    async def changerolecolor(
      self,
      interaction: discord.Interaction,
      color: str,
      role: discord.Role
    ):
      if "#" in color:
        color = color.replace('#', '')
      dec = int(color, 16)
      image = f"https://serux.pro/rendercolour?hex={color}&height=100&width=225"
      em = discord.Embed(description = f"> {role.mention} is now `#{color}`", color = dec)
      em.set_image(url=image)
      await role.edit(colour=dec)
      await interaction.response.send_message(embed=em)

    @changerolecolor.error
    async def changerolecolor_error(
      self,
      interaction: discord.Interaction,
      error: app_commands.AppCommandError
    ):
      if isinstance(error, app_commands.CommandInvokeError):
        await interaction.response.send_message("I don't have permission to change role color. Try placing my role above the role you want to change!", ephemeral = True)
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    color(bot)
  )