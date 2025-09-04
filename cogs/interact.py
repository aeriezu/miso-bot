import discord
from discord import app_commands
from discord.ext import commands
import random

class interact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "hug",
      description = "hug a member",
    )

    async def hug(
      self,
      interaction: discord.Interaction,
      user: discord.Member
    ):
      hugs = [
        "https://cdn.discordapp.com/attachments/990812705634025502/990815525816897616/ezgif-3-73ce8511d2.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815526127284264/ezgif-3-2f317812fc.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815527003897876/ezgif-3-a9da3805a7.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815527276511262/heejin-chuu.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815527498842132/cravity-cravity-allen.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815527830183986/hug-kpop.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815528086024202/mina-twice.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990815861461901312/txt-tomorrow-x-together.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/991027684165447740/IMG_6719.gif"
      ]
      
      if user == interaction.user:
        await interaction.response.send_message("you can't hug yourself :(", ephemeral = True)
      else:
        random_hug = random.choice(hugs)
        em = discord.Embed(description = f"{interaction.user.mention} has hugged you!")
        em.set_image(url=random_hug)
        await interaction.response.send_message(f"{user.mention}", embed=em)

    @app_commands.command(
      name = "slap",
      description = "slap a member",
    )

    async def slap(
      self,
      interaction: discord.Interaction,
      user: discord.Member
    ):
      slaps = [
        "https://cdn.discordapp.com/attachments/990812705634025502/990812783811625020/IMG_6483.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990813818412208138/IMG_6485.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990813981126033448/IMG_6484.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990813995638337546/IMG_6486.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/990814803905880084/IMG_6487.gif",
        "https://cdn.discordapp.com/attachments/990812705634025502/991027910435549254/IMG_6721.gif"
      ]
      
      if user == interaction.user:
        await interaction.response.send_message("you can't slap yourself :(", ephemeral = True)
      else:
        random_slap = random.choice(slaps)
        em = discord.Embed(description = f"{interaction.user.mention} has slapped you!")
        em.set_image(url=random_slap)
        await interaction.response.send_message(f"{user.mention}", embed=em)
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    interact(bot)
  )