#IMPORTS
import os
import discord
import asyncio
import sys
import platform


#FROM DISCORD
from discord.ext import commands

#INTENTS
intents = discord.Intents.default()

#DON'T GENERATE __PYCACHE__
sys.dont_write_bytecode = True


#DOTENV
TOKEN = os.environ['DISCORD_TOKEN']


#BOT CLASS
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", help_command=None, intents=intents)

    #ON_READY 
    async def on_ready(self):
        print("-------------------")
        print('Mr. Spooky is online!')
        print('Ping: {0}ms'.format(round(bot.latency, 3)))
        print(f"API: {discord.__version__}")
        print(f"Python: {platform.python_version()}")
        print("-------------------")

        #BOT STATUS LOOP
        bot.loop.create_task(status_task())


    #LOAD COGS & SYNC SLASH COMMANDS
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.startswith("__pycache__"):
                continue

            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"-------------------\nLoaded {filename}")

            else:
                print(f"-------------------\nError loading {filename}")

        await self.tree.sync()
        print("-------------------")
        print("Synced Slash Commands!")
        print("-------------------")


#DEFINE BOT
bot = Bot()

#VVV COG COMMANDS WON'T WORK WITHOUT MESSAGE CONTENT (NOT NEEDED EITHER WAY) VVV

#LOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded **{extension}** extension!")


#UNLOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded **{extension}** extension!")


#RELOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded **{extension}** extension!")


#SHUTDOWN COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down!")
    await bot.close()


#BOT STATUS
@bot.event
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name="BOO!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="Made for the Halloween Hackathon 2022 by Top.gg"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="Supports Slash Commands!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="I'm Mr. Spooky!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="Made in Greece! (even though we don't have Halloween here)"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="OoOoOoo I'm a spooky ghost!"))
        await asyncio.sleep(120)


bot.run(TOKEN)