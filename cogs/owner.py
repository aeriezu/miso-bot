import discord
from discord.ext import commands
import typing

class owner(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
      self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
          if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
          elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
          elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
          else:
            synced = await ctx.bot.tree.sync()
    
          await ctx.message.delete()
          await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}", delete_after=2
            )
          return
    
        ret = 0
        for guild in guilds:
          try:
            await ctx.bot.tree.sync(guild=guild)
          except discord.HTTPException:
            pass
          else:
            ret += 1

        await ctx.message.delete()
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.", delete_after=2)

    @commands.command()
    @commands.is_owner()
    async def say(
      self, 
      ctx: commands.Context,
      *,
      text: str
    ):
      await ctx.message.delete()
      await ctx.send(text)

    @commands.command()
    @commands.is_owner()
    async def leave(
      self, 
      ctx: commands.Context,
      *,
      guildinput
    ):
      try:
        guildid = int(guildinput)
      except:
        await ctx.send("invalid")

      try:
        guild = self.bot.get_guild(guildid)
      except:
        await ctx.send("invalid")

      try:
        await guild.leave()
        await ctx.send("left fuild")
      except:
        await ctx.send("couldn't leave'")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    owner(bot)
  )