#IMPORTS
import discord

#FROM DISCORD
from discord import app_commands
from discord.ext import commands

#COG CLASS
class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #SUPPORT COMMAND
    @app_commands.command(name="support", description="Get support about the bot!")
    async def support(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Something went wrong?", description="", color=0xeb6123)
        embed.add_field(name="Support Server", value="[Timeless28](https://discord.gg/ZmjXmfvxHU)", inline=False)
        embed.add_field(name="GitHub Issues", value="[Mr. Spooky](https://github.com/TeeTwoNot/Mr-Spooky/issues)", inline=False)
        embed.add_field(name="Email (Not Preferred)", value="info@teetwonot.com", inline=False)
        await interaction.response.send_message(embed=embed)

    #SERVERS COMMAND
    @app_commands.command(name="servers", description="See how many servers Mr. Spooky is haunting!")
    async def servers(self, interaction: discord.Interaction):
        count = len(self.bot.guilds)
        embed = discord.Embed(title="Currently haunting...", description="", color=0xeb6123)
        embed.add_field(name=f"{count} servers!", value="")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))