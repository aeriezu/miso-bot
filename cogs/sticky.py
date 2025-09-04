import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import datetime

OWNER_ID = 776247598184792104  

class StickyMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sticky_tasks = {}  # channel_id: asyncio.Task

    async def sticky_enabled(self, channel_id: int):
        async with self.bot.db.execute(
            "SELECT 1 FROM sticky_messages WHERE channel = ?", (channel_id,)
        ) as cursor:
            return await cursor.fetchone() is not None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.db.execute(
            """
            CREATE TABLE IF NOT EXISTS sticky_messages (
                channel INTEGER PRIMARY KEY,
                description TEXT,
                color INTEGER,
                last_message_id INTEGER,
                timestamp TEXT
            )
            """
        )
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not await self.sticky_enabled(message.channel.id):
            return

        # Cancel any pending sticky task for this channel
        if task := self.sticky_tasks.get(message.channel.id):
            task.cancel()

        # Start a delayed task to repost sticky message
        self.sticky_tasks[message.channel.id] = asyncio.create_task(
            self.repost_sticky_after_delay(message.channel)
        )

        await self.bot.process_commands(message)

    async def repost_sticky_after_delay(self, channel: discord.TextChannel, delay: float = 1.5):
        try:
            await asyncio.sleep(delay)

            async with self.bot.db.execute(
                "SELECT description, color, last_message_id, timestamp FROM sticky_messages WHERE channel = ?",
                (channel.id,),
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                return

            description, color_int, old_msg_id, timestamp_str = row

            try:
                old_msg = await channel.fetch_message(old_msg_id)
                await old_msg.delete()
            except (discord.NotFound, discord.Forbidden):
                pass

            embed = discord.Embed(description=description or " ", color=color_int or discord.Color.blue())

            owner = await self.bot.fetch_user(OWNER_ID)
            embed.set_author(
                name=f"ae is...",
                icon_url=owner.display_avatar.url
            )
            embed.set_footer(text=f"posted: {timestamp_str or 'unknown time'}")

            new_msg = await channel.send(embed=embed)

            await self.bot.db.execute(
                "UPDATE sticky_messages SET last_message_id = ? WHERE channel = ?",
                (new_msg.id, channel.id),
            )
            await self.bot.db.commit()

        except asyncio.CancelledError:
            pass  # Task was cancelled, do nothing

    @app_commands.command(name="sticky", description="Manage sticky embed message in this channel")
    @app_commands.describe(action="set or remove sticky", description="Embed description text", color="Hex color code, e.g. #00ff00")
    async def sticky(
        self,
        interaction: discord.Interaction,
        action: str,
        description: str = None,
        color: str = None,
    ):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("you're not allowed to use this.", ephemeral=True)
            return

        action = action.lower()

        if action == "set":
            if not description:
                await interaction.response.send_message("you must provide a description for the sticky embed.", ephemeral=True)
                return

            color_int = discord.Color.blue().value
            if color:
                try:
                    if color.startswith("#"):
                        color = color[1:]
                    color_int = int(color, 16)
                except:
                    await interaction.response.send_message("invalid color hex code. using default blue.", ephemeral=True)
                    color = "7F83CC"
                    color_int = int(color, 16)

            timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

            async with self.bot.db.execute(
                "SELECT last_message_id FROM sticky_messages WHERE channel = ?", (interaction.channel.id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    try:
                        old_msg = await interaction.channel.fetch_message(row[0])
                        await old_msg.delete()
                    except (discord.NotFound, discord.Forbidden):
                        pass

            await self.bot.db.execute(
                "INSERT OR REPLACE INTO sticky_messages (channel, description, color, last_message_id, timestamp) VALUES (?, ?, ?, ?, ?)",
                (interaction.channel.id, description, color_int, 0, timestamp_str)
            )
            await self.bot.db.commit()

            embed = discord.Embed(description=description, color=color_int)
            owner = await self.bot.fetch_user(OWNER_ID)
            embed.set_author(
                name=f"ae is...",
                icon_url=owner.display_avatar.url
            )
            embed.set_footer(text=f"posted: {timestamp_str}")

            sent_msg = await interaction.channel.send(embed=embed)

            await self.bot.db.execute(
                "UPDATE sticky_messages SET last_message_id = ? WHERE channel = ?",
                (sent_msg.id, interaction.channel.id)
            )
            await self.bot.db.commit()

            await interaction.response.send_message("sticky embed set and posted.", ephemeral=True)

        elif action == "remove":
            async with self.bot.db.execute(
                "SELECT last_message_id FROM sticky_messages WHERE channel = ?", (interaction.channel.id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    try:
                        old_msg = await interaction.channel.fetch_message(row[0])
                        await old_msg.delete()
                    except (discord.NotFound, discord.Forbidden):
                        pass

            await self.bot.db.execute(
                "DELETE FROM sticky_messages WHERE channel = ?", (interaction.channel.id,)
            )
            await self.bot.db.commit()
            await interaction.response.send_message("sticky embed removed.", ephemeral=True)

        else:
            await interaction.response.send_message("invalid action. Use `set` or `remove`.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StickyMessage(bot))
