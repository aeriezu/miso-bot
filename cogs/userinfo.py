import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import commands
from main import client
from collections import deque
from typing import List
from PIL import Image, ImageFont, ImageDraw
import dateutil.parser
import requests
import os, io

#################################################################

class PaginatorView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=30)
        self.embed = embeds
        self.current = embeds[0]
        self.len = len(embeds)
        self.current_page = 0

    @discord.ui.button(label='<', style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page + 1 > 1:
            self.current_page -= 1
        embed = self.embed[self.current_page]
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label='>', style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page + 1 < self.len:
            self.current_page += 1
        embed = self.embed[self.current_page]
        await interaction.response.edit_message(embed=embed)

#################################################################

class userinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

#################################################################

    @app_commands.command(
        name="banner",
        description="get user banner",
    )
    async def banner(self,
                     interaction: discord.Interaction,
                     user: discord.Member = None):  # type: ignore
        if user == None:
            user = interaction.user # type: ignore
        else:
            user = user
        usr = await client.fetch_user(user.id)
        
        if usr.banner:
            banner = usr.banner.url
            img = Image.open(requests.get(banner, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            bannerEmbed = discord.Embed(color=discord.Color.from_rgb(*dom_colors),  # type: ignore
                                        title='',
                                        description=f"**[banner]({banner})**")
            bannerEmbed.set_author(name=f'{usr.display_name}',
                                   icon_url=user.display_avatar.url)
            bannerEmbed.set_image(url=banner)
            bannerEmbed.timestamp = discord.utils.utcnow()
            await interaction.response.send_message(embed=bannerEmbed)

        elif usr.accent_color:
            uc = str(usr.accent_color).format(hex).strip('#')
            colorEmbed = discord.Embed(
                color=usr.accent_color,
                title='',
                description=
                f"**[banner]({f'https://singlecolorimage.com/get/{uc}/400x100'})**"
            )
            colorEmbed.set_author(name=f'{usr.display_name}',
                                  icon_url=user.display_avatar.url)
            colorEmbed.set_image(
                url=f'https://singlecolorimage.com/get/{uc}/400x100')
            colorEmbed.timestamp = discord.utils.utcnow()
            await interaction.response.send_message(embed=colorEmbed)

        else:
            bnerrEmbed = discord.Embed(title='',
                                       description='banner/color not assigned')
            bnerrEmbed.set_author(name=f'{usr.display_name}',
                                  icon_url=user.display_avatar.url)
            bnerrEmbed.timestamp = discord.utils.utcnow()
            await interaction.response.send_message(embed=bnerrEmbed)

#################################################################

    @app_commands.command(
        name="whois",
        description="get info on a user",
    )
    async def whois(self,
                    interaction: discord.Interaction,
                    user: discord.Member = None):  # type: ignore
        if user == None:
            user = interaction.user  # type: ignore
        member = await client.fetch_user(user.id)
        rlist = []
        for role in reversed(user.roles):
            if role.name != "@everyone":
                rlist.append(role.mention)
        b = ' '.join(rlist)
        em = discord.Embed(description=f"{user.mention}\n```{user.id}```")
        em.set_author(name=f"{user.display_name}", icon_url=f"{member.display_avatar.url}")
        em.add_field(name="joined",
                     value=user.joined_at.strftime("%a, %b %d, %Y %I:%M %p").lower())  # type: ignore
        em.add_field(name="registered",
                     value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p").lower())
        em.add_field(name=f"roles [{len(rlist)}]",
                     value=''.join([b]),
                     inline=False)
        em.timestamp = discord.utils.utcnow()
        em.set_thumbnail(url=member.display_avatar.url)
        #get banner
        if member.banner:
            banner = member.banner.url
            img = Image.open(requests.get(banner, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"{user.mention}\n```{user.id}```") # type: ignore
            em.set_author(name=f"{user.display_name}", icon_url=f"{member.display_avatar.url}")
            em.add_field(name="joined",
                        value=user.joined_at.strftime("%a, %b %d, %Y %I:%M %p").lower())  # type: ignore
            em.add_field(name="registered",
                        value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p").lower())
            em.add_field(name=f"roles [{len(rlist)}]",
                        value=''.join([b]),
                        inline=False)
            em.timestamp = discord.utils.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            em.set_image(url=banner)
            await interaction.response.send_message(embed=em)
        elif member.accent_color:
            uc = str(member.accent_color).format(hex).strip('#')
            em = discord.Embed(color=member.accent_color, description=f"{user.mention}\n```{user.id}```")
            em.set_author(name=f"{user.display_name}", icon_url=f"{member.display_avatar.url}")
            em.add_field(name="joined",
                        value=user.joined_at.strftime("%a, %b %d, %Y %I:%M %p").lower())  # type: ignore
            em.add_field(name="registered",
                        value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p").lower())
            em.add_field(name=f"roles [{len(rlist)}]",
                        value=''.join([b]),
                        inline=False)
            em.timestamp = discord.utils.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            em.set_image(url=f'https://singlecolorimage.com/get/{uc}/400x100')
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(embed=em)

#################################################################

    @app_commands.command(
        name="avatar",
        description="get a user's avatar",
    )
    async def avatar(self,
                     interaction: discord.Interaction,
                     user: discord.Member = None):  # type: ignore
        if user == None:
            user = interaction.user  # type: ignore
        member = interaction.guild.get_member(user.id)  # type: ignore
        if member.guild_avatar and member.avatar:  # type: ignore
            img = Image.open(requests.get(member.guild_avatar.url, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[server avatar]({member.guild_avatar.url})**")  # type: ignore
            em.set_author(name=f"{user.display_name}", icon_url=f"{member.guild_avatar.url}")  # type: ignore
            em.set_image(url=member.guild_avatar.url)  # type: ignore
            em.timestamp = discord.utils.utcnow()

            img = Image.open(requests.get(member.avatar.url, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em1 = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[profile avatar]({member.avatar.url})**")  # type: ignore
            em1.set_author(name=f"{user.display_name}", icon_url=f"{member.avatar.url}")  # type: ignore
            em1.set_image(url=member.avatar.url)  # type: ignore
            em1.timestamp = discord.utils.utcnow()
            
            embeds = []
            embeds.append(em)
            embeds.append(em1)

            view = PaginatorView(embeds)
            await interaction.response.send_message(embed=view.current, view=view)

        elif member.guild_avatar and member.default_avatar:  # type: ignore
            img = Image.open(requests.get(member.guild_avatar.url, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[server avatar]({member.guild_avatar.url})**") # type: ignore
            em.set_author(name=f"{user.display_name}", icon_url=f"{member.guild_avatar.url}") # type: ignore
            em.set_image(url=member.guild_avatar.url) # type: ignore
            em.timestamp = discord.utils.utcnow()

            img = Image.open(requests.get(member.default_avatar.url, stream=True).raw).convert('RGB') # type: ignore
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em1 = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[profile avatar]({member.default_avatar.url})**") # type: ignore
            em1.set_author(name=f"{user.display_name}", icon_url=f"{member.default_avatar.url}") # type: ignore
            em1.set_image(url=member.default_avatar.url) # type: ignore
            em1.timestamp = discord.utils.utcnow()
            
            embeds = []
            embeds.append(em)
            embeds.append(em1)

            view = PaginatorView(embeds)
            await interaction.response.send_message(embed=view.current, view=view) # type: ignore

        else:
            if member.avatar: # type: ignore
                img = Image.open(requests.get(member.avatar.url, stream=True).raw).convert('RGB') # type: ignore
                dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
                em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[profile avatar]({member.avatar.url})**") # type: ignore
                em.set_author(name=f"{user.display_name}", icon_url=f"{member.avatar.url}") # type: ignore
                em.set_image(url=member.avatar.url) # type: ignore
                em.timestamp = discord.utils.utcnow()
                await interaction.response.send_message(embed=em)
            else:
                img = Image.open(requests.get(member.default_avatar.url, stream=True).raw).convert('RGB') # type: ignore
                dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
                em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"**[profile avatar]({member.default_avatar.url})**") # type: ignore
                em.set_author(name=f"{user.display_name}", icon_url=f"{member.default_avatar.url}") # type: ignore
                em.set_image(url=member.default_avatar.url) # type: ignore
                em.timestamp = discord.utils.utcnow() 
                await interaction.response.send_message(embed=em)

#################################################################

    @app_commands.command(
        name="profile",
        description="get a user's avatar and banner",
    )
    async def profile(self,
                      interaction: discord.Interaction,
                      member: discord.Member = None): # type: ignore
        if member == None:
            member = interaction.user # type: ignore
        user = await client.fetch_user(member.id)
        status = interaction.guild.get_member(member.id).status # type: ignore

        def get_activity():
            for activity in interaction.guild.get_member(member.id).activities: # type: ignore
                if isinstance(activity, discord.CustomActivity):
                    return activity
                else:
                    activity = interaction.guild.get_member( # type: ignore
                        member.id).activity.name # type: ignore
                    activity_type = interaction.guild.get_member( # type: ignore
                        member.id).activity.type # type: ignore
                    activity_type = str(activity_type)
                    activity_type = activity_type.replace('ActivityType.', '')
                    if activity_type == "listening":
                        activity_type = "listening to"
                    activity = f"{activity_type} **{activity}**"
                    return activity

        usr_activity = get_activity()

        if "Custom Status" in str(usr_activity):
            usr_activity = str(usr_activity).replace('Custom Status', '')

        try:
            activities1 = interaction.guild.get_member( # type: ignore
                member.id).activities[1].name # type: ignore
            activities1_type = interaction.guild.get_member( # type: ignore
                member.id).activities[1].type # type: ignore
            activities1_type = str(activities1_type)
            activities1_type = activities1_type.replace('ActivityType.', '')
            if activities1_type == "listening":
                activities1_type = "listening to"
            activities1 = f"{activities1_type} **{activities1}**"
        except IndexError:
            activities1 = "None"

        usr_emoji = "None"

        def get_emoji():
            if str(status) == "streaming":
                usr_emoji = "<:status_streaming:1121149336470962206>"
            elif str(status) == "offline":
                usr_emoji = "<:status_offline:1004659232131534859>"
                return usr_emoji
            elif str(status) == "idle":
                usr_emoji = "<:status_idle:1004659223239598100>"
                return usr_emoji
            elif str(status) == "dnd":
                usr_emoji = "<:status_dnd:1004659213043245106>"
                return usr_emoji
            elif str(status) == "online":
                usr_emoji = "<:status_online:1004659241119911976>"
            
                return usr_emoji

        usr_emoji = get_emoji()

        if str(usr_activity).startswith("<"):
            try:
                sub1 = "<"
                sub2 = ">"
                idx1 = str(usr_activity).index(sub1)
                idx2 = str(usr_activity).index(sub2)

                res = ''
                # getting elements in between
                for idx in range(idx1 + len(sub1), idx2):
                    res = res + str(usr_activity)[idx]

                emojiName = "<" + res + ">"
                emojiStatus = discord.PartialEmoji.from_str(emojiName)
            except:
                emojiStatus = None

        await interaction.response.defer()

        #get banner
        if user.banner:
            banner = user.banner.url
            img = Image.open(requests.get(banner, stream=True).raw).convert('RGB')
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            bannerEmbed = discord.Embed(
                title='',
                description=
                f"**[avatar]({user.display_avatar.url}) | [banner]({banner})**\n",
                color=discord.Color.from_rgb(*dom_colors)) # type: ignore
            if activities1 != "None":
                bannerEmbed.add_field(
                    name='status',
                    value=f'{usr_emoji} {usr_activity} & {activities1}')
            if activities1 == "None" and usr_activity != None:
                bannerEmbed.add_field(name='status',
                                      value=f'{usr_emoji} {usr_activity}')
            bannerEmbed.set_author(name=f"{member.display_name}",
                                   icon_url=user.display_avatar.url)
            if usr_activity is None:
                bannerEmbed.add_field(name='status',
                                      value=f'{usr_emoji} {status}')
            bannerEmbed.set_thumbnail(url=user.display_avatar.url)
            bannerEmbed.set_image(url=banner)
            bannerEmbed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=bannerEmbed)

        elif user.accent_color:
            uc = str(user.accent_color).format(hex).strip('#')
            colorEmbed = discord.Embed(
                color=user.accent_color,
                title='',
                description=
                f"**[avatar]({user.avatar.url}) | [banner]({f'https://singlecolorimage.com/get/{uc}/400x100'})**" # type: ignore
            ) 
            if activities1 != "None":
                colorEmbed.add_field(
                    name='status',
                    value=f'{usr_emoji} {usr_activity} & {activities1}')
            if activities1 == "None" and usr_activity != None:
                colorEmbed.add_field(name='status',
                                     value=f'{usr_emoji} {usr_activity}')
            colorEmbed.set_author(name=f"{member.display_name}",
                                  icon_url=user.display_avatar.url)
            if usr_activity is None:
                colorEmbed.add_field(name='status',
                                     value=f'{usr_emoji} {status}')
            colorEmbed.set_thumbnail(url=user.avatar.url) # type: ignore
            colorEmbed.set_image(
                url=f'https://singlecolorimage.com/get/{uc}/400x100')
            colorEmbed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=colorEmbed)
        else:
            img = Image.open(requests.get(user.display_avatar.url, stream=True).raw).convert('RGB')
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            bnerrEmbed = discord.Embed(
                color=discord.Color.from_rgb(*dom_colors), # type: ignore
                title='',
                description=
                f'**[avatar]({user.avatar.url}) | banner/color not assigned**') # type: ignore
            if activities1 != "None":
                bnerrEmbed.add_field(
                    name='status',
                    value=f'{usr_emoji} {usr_activity} & {activities1}')
            if activities1 == "None" and usr_activity != None:
                bnerrEmbed.add_field(name='status',
                                     value=f'{usr_emoji} {usr_activity}')
            bnerrEmbed.set_author(name=f"{member.display_name}",
                                  icon_url=user.display_avatar.url)
            if usr_activity is None:
                bnerrEmbed.add_field(name='status',
                                     value=f'{usr_emoji} {status}')
            bnerrEmbed.set_thumbnail(url=user.display_avatar.url)
            bnerrEmbed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=bnerrEmbed)

#################################################################

    @app_commands.command(
        name="nowplaying",
        description="get user's current spotify track",
    )
    async def np(self,
                 interaction: discord.Interaction,
                 member: discord.Member = None):  # type: ignore
        
        if member == None:
            member = interaction.user # type: ignore
        user = await client.fetch_user(member.id)
        
        spotifyPlaying = next((activity for activity in interaction.guild.get_member(member.id).activities if isinstance(activity, discord.Spotify)), None)  # type: ignore

        if spotifyPlaying is None:
            em = discord.Embed(description=f"**{member.display_name}** is not listening to anything on spotify")
            em.set_author(name="spotify", icon_url=member.display_avatar.url)
            await interaction.response.send_message(embed=em)
        else:
            img = Image.open(requests.get(spotifyPlaying.album_cover_url, stream=True).raw).convert('RGB')
            dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
            em = discord.Embed(color=discord.Color.from_rgb(*dom_colors), description=f"🎵 ‎ : ‎ **[{spotifyPlaying.title.lower()}](https://open.spotify.com/track/{spotifyPlaying.track_id})**\n👤 ‎ : ‎ by **{spotifyPlaying.artist.lower()}**\n0:00 ━━━━⬤─────── {dateutil.parser.parse(str(spotifyPlaying.duration)).strftime('%M:%S')}") # type: ignore
            em.set_author(name=f"{member.display_name} is listening to...", icon_url=member.display_avatar.url)
            em.set_thumbnail(url=spotifyPlaying.album_cover_url) # type: ignore
            await interaction.response.send_message(content=f"", embed=em) # type: ignore

#################################################################

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(userinfo(bot))
