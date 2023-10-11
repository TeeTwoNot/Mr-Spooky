#IMPORTS
import discord
import aiohttp
import os
from typing import Final
import asyncio
import time
import json

#FROM DISCORD
from discord import app_commands
from discord.ext import commands
from discord.app_commands import AppCommandError

OPENAI_TOKEN : Final[str] = os.environ['OPENAI_TOKEN']

#COG CLASS
class AI(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """
    PRODUCTION-READY CHECKLIST:
    - [] Premium Feature
    - [] Change /imagine desc
    - [] Error handling (https://help.openai.com/en/articles/6897213-openai-library-error-types-guidance) & (https://platform.openai.com/docs/guides/error-codes/api-errors)
    - [] Credits & Usage Limits (https://platform.openai.com/account/billing/overview)
    - [] Remove all test code
    - [] Replace try/except with error handler
    """

    #SAMPLE AI IMAGE GENERATOR (OPENAI API)
    @app_commands.command(name="imagine", description="Custom AIOHTTP POST request")
    @app_commands.checks.cooldown(1, 10.0)
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        url = "https://api.openai.com/v1/images/generations"
        data = {
            "prompt": prompt,
            "size": "256x256"
        }
        payload = json.dumps(data)
        headers = {
            "Content-type": "application/json", 
            "Authorization": f"Bearer {OPENAI_TOKEN}"
            }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, data=payload) as res:
                    data = await res.json()
                    img_url = data['data']['url']
                    embed = discord.Embed(title=f"{prompt}", description="", color=0xeb6123)
                    embed.set_image(url=img_url)
                    embed.set_footer(text=f"Requested by {interaction.user.global_name}")
                    await interaction.response.send_message(embed=embed)

            # Move these on error handler & change to embed responses
            except aiohttp.ClientConnectionError as e:
                await interaction.response.send_message(f"Sorry! Something went wrong when trying to generate your image.")
            except aiohttp.ClientResponseError as e:
                await interaction.response.send_message(f"Sorry! Something went wrong when trying to generate your image.")
            except asyncio.exceptions.TimeoutError as e:
                await interaction.response.send_message(f"Sorry! Your request timed out.")

    @imagine.error
    async def imagine_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AI(bot))
