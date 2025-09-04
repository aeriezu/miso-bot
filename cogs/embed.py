import discord
from discord import app_commands
from discord.ext import commands

class editMainModal(discord.ui.Modal, title="edit the embed"):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        
        self.emTitle = discord.ui.TextInput(
            label = "title",
            placeholder = "your title here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required= False,
            max_length = 256,
            default = self.embed.title,
        )

        self.emDescription = discord.ui.TextInput(
            label = 'description',
            style = discord.TextStyle.paragraph,
            placeholder = 'your description here...',
            required = True,
            max_length = 4000,
            default = self.embed.description,
        )

        self.emColor = discord.ui.TextInput(
            label = 'color',
            placeholder = 'your color hex here (with or without # | none for no color)...',
            style = discord.TextStyle.short,
            required= False,
            max_length = 7,
            default = str(self.embed.color),
        )

        self.add_item(self.emTitle)
        self.add_item(self.emDescription)
        self.add_item(self.emColor)

    async def on_submit(self, interaction: discord.Interaction):
        em = self.embed
        em.title = self.emTitle.value
        em.description = self.emDescription.value

        color = self.emColor.value
        dec = None
        if color.casefold() != "None".casefold():
            if "#" in color:
                color = color.replace('#', '')
            dec = int(color, 16)
        em.color = dec

        await interaction.response.edit_message(embed=em)
        
class editExtraModal(discord.ui.Modal, title="edit the embed"):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        
        self.emAuthorName = discord.ui.TextInput(
            label = "author name",
            placeholder = "your author name here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required= False,
        )

        self.emAuthorIcon = discord.ui.TextInput(
            label = "author icon",
            placeholder = "your author icon link here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required= False,
        )

        self.emThumbnail = discord.ui.TextInput(
            label = "thumbnail",
            placeholder = "your thumbnail link here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required= False,
        )

        self.emImage = discord.ui.TextInput(
            label = "image",
            placeholder = "your image link here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required= False,
        )

        self.add_item(self.emAuthorName)
        self.add_item(self.emAuthorIcon)
        self.add_item(self.emThumbnail)
        self.add_item(self.emImage)

    async def on_submit(self, interaction: discord.Interaction):
        em = self.embed

        if self.emAuthorName.value:
            em.set_author(name=self.emAuthorName.value or None, icon_url=self.emAuthorIcon.value or None)
        elif self.emAuthorIcon.value:
            em.set_author(name=self.emAuthorName.value or None, icon_url=self.emAuthorIcon.value or None)
        else:
            em.remove_author()

        em.set_thumbnail(url=self.emThumbnail.value or None)
        em.set_image(url=self.emImage.value or None)

        await interaction.response.edit_message(embed=em)

class editFooterModal(discord.ui.Modal, title="edit the embed"):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        
        self.emFooter = discord.ui.TextInput(
            label = "footer text",
            placeholder = "your footer text here... (leave empty for nothing)",
            style = discord.TextStyle.paragraph,
            required = False,
            max_length = 2048,
        )

        self.emFooterIcon = discord.ui.TextInput(
            label = "footer icon",
            placeholder = "your footer icon link here... (leave empty for nothing)",
            style = discord.TextStyle.short,
            required = False,
        )

        self.emTimestamp = discord.ui.TextInput(
            label = "timestamp",
            placeholder = "empty for current time | none for no timstamp",
            style = discord.TextStyle.short,
            required = False,
        )

        self.add_item(self.emFooter)
        self.add_item(self.emFooterIcon)
        self.add_item(self.emTimestamp)

    async def on_submit(self, interaction: discord.Interaction):
        em = self.embed

        if self.emFooter.value:
            em.set_footer(text=self.emFooter.value or "None", icon_url=self.emFooterIcon.value or None)
        elif self.emFooterIcon.value:
            em.set_footer(text=self.emFooter.value or "None", icon_url=self.emFooterIcon.value or None)
        else:
           em.set_footer(text=None, icon_url=None)

        if self.emTimestamp.value.casefold() != "None".casefold():
            em.timestamp = discord.utils.utcnow()
        else:
            em.timestamp = None

        await interaction.response.edit_message(embed=em)

class embedButtons(discord.ui.View):
    def __init__(self, embed):
      super().__init__()
      self.value = None
      self.embed = embed

    @discord.ui.button(label="edit main", style=discord.ButtonStyle.blurple)
    async def editMain(self, interaction: discord.Interaction, button: discord.ui.Button):
      modal = editMainModal(self.embed)
      await interaction.response.send_modal(modal)

    @discord.ui.button(label="edit extra", style=discord.ButtonStyle.blurple)
    async def editExtra(self, interaction: discord.Interaction, button: discord.ui.Button):
      modal = editExtraModal(self.embed)
      await interaction.response.send_modal(modal)

    @discord.ui.button(label="edit footer", style=discord.ButtonStyle.blurple)
    async def editFooter(self, interaction: discord.Interaction, button: discord.ui.Button):
      modal = editFooterModal(self.embed)
      await interaction.response.send_modal(modal)

    @discord.ui.button(label="send embed", style=discord.ButtonStyle.green)
    async def finishEmbed(self, interaction: discord.Interaction, button: discord.ui.Button):
      em = self.embed
      channel = interaction.channel
      await channel.send(embed=em) # type: ignore
      await interaction.response.send_message("The embed has been sent!", ephemeral=True)

class embed(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
      name = "embed",
      description = "create a custom embed",
    )

    async def embed(
      self,
      interaction: discord.Interaction,
    ):
        em = discord.Embed(title="this is the title", description="this is the description\n\nclick the buttons to edit the embed!\n> **main:** title, description, color\n> **extra:** author, thumbnail, image\n> **footer:** footer, timestamp\n> **send embed:** sends to current channel")
        em.set_image(url="https://cdn.discordapp.com/attachments/1024872033068261407/1102468396467105842/embed_image.png")
        em.set_footer(text="this is the footer text", icon_url="https://cdn.discordapp.com/attachments/1024872033068261407/1102469134601682994/embed_footericon.png")
        em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1024872033068261407/1102468680677339176/embed_thumbnail.png")
        em.set_author(name="this is the author name", icon_url="https://cdn.discordapp.com/attachments/1024872033068261407/1102469103903576084/embed_authoricon.png")
        em.timestamp = discord.utils.utcnow()
        view = embedButtons(em)
        await interaction.response.send_message(embed=em, view=view, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    embed(bot)
  )