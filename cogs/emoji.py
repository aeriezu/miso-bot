import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import commands
from main import client
from collections import deque
from typing import List

class emoteName(discord.ui.Modal, title="edit emoji name"):
    def __init__(self, emoji):
        super().__init__()
        self.emoji = emoji
        
        self.emojiName = discord.ui.TextInput(
            label = "emoji name",
            placeholder = "your emoji name here...",
            style = discord.TextStyle.short,
            required= True
        )

        self.add_item(self.emojiName)
        
    async def on_submit(self, ctx):
      emojiName = self.emojiName.value
      emoji = self.emoji
      await ctx.guild.create_custom_emoji(name=emojiName, image=await emoji.read())
      await ctx.response.send_message(content=f'the emoji named, "{emojiName}", has been cloned! {emoji}', ephemeral=True)

class yesNoButtons(discord.ui.View):
    def __init__(self, embed, emoji):
      super().__init__(timeout=100)
      self.embed = embed
      self.emoji = emoji
      
    @discord.ui.button(label="yes", style=discord.ButtonStyle.blurple)
    async def yes(self, ctx, button: discord.ui.Button):
      modal = emoteName(self.emoji)
      await ctx.response.send_modal(modal)
       
    @discord.ui.button(label="no", style=discord.ButtonStyle.blurple)
    async def no(self, ctx, button: discord.ui.Button):
      emoji = self.emoji
      self.response = "no"
      await ctx.guild.create_custom_emoji(name=emoji.name, image=await emoji.read())
      await ctx.response.send_message(content=f'the emoji named, "{emoji.name}", has been cloned! {emoji}', ephemeral=True)

class embedButtons(discord.ui.View):
    def __init__(self, embed: List[discord.Embed], emotes: List[discord.PartialEmoji]):
      super().__init__(timeout=100)
      self.embed = embed
      self.current = embed[0]
      self.len = len(embed)
      self.current_page = 0
      self.emotes = emotes
      self.emoteCur = emotes[0]

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def pageLeft(self, ctx, button: discord.ui.Button):
      if self.current_page + 1 > 1:
        self.current_page -= 1
      embed = self.embed[self.current_page]
      embed.set_footer(text=f"page {self.current_page + 1}/{self.len}")
      await ctx.response.edit_message(embed=embed)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def pageRight(self, ctx, button: discord.ui.Button):
      if self.current_page + 1 < self.len:
        self.current_page += 1
      embed = self.embed[self.current_page]
      embed.set_footer(text=f"page {self.current_page + 1}/{self.len}")
      await ctx.response.edit_message(embed=embed)

    @discord.ui.button(label="clone", style=discord.ButtonStyle.blurple)
    async def stealEmoji(self, ctx, button: discord.ui.Button):
      emoji = self.emotes[self.current_page]
      view = yesNoButtons(self.embed, emoji)
      if ctx.user.guild_permissions.manage_emojis:
        await ctx.response.send_message(content=f"would you like to set a custom name?", view=view, ephemeral=True)
      else:
        await ctx.response.send_message(content=f"you don't have permission to clone emojis :(", view=view, ephemeral=True)

class emoji(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()

    async def emoji(self, ctx: commands.Context, *emojis: discord.PartialEmoji):
      emotes = []
      for emoji in emojis:
        emotes.append((emoji))

      embeds = []
      for emoji in emotes:
        em = discord.Embed(description=f"```{emoji.name} {emoji.id}```")
        em.set_author(name="emoji viewer", icon_url=ctx.author.avatar.url) # type: ignore
        em.set_image(url=emoji.url)
        em.set_footer(text=f"page 1/{len(emotes)}")
        embeds.append(em)
        
      view = embedButtons(embeds, emotes)
      await ctx.send(embed=view.current, view=view)
      
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    emoji(bot)
  )