"""
main.py
~~~~~~~~~~~~~~~~~~~
Main file.
"""

#IMPORTS
import os
import datetime
import asyncio
import sys
import platform
import logging
import discord
import aiohttp

from typing import Final
from discord.ext import commands, tasks
from colorama import init as colorama_init
from colorama import Fore, Style

colorama_init(autoreset=True)

#INTENTS
intents = discord.Intents.default()


#DON'T GENERATE __PYCACHE__
sys.dont_write_bytecode = True

#LOGGING
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '{1}[%(asctime)s]{0} {2}[%(levelname)s]{0} {3}%(name)s{0} - %(message)s'.format(
        Style.RESET_ALL,
        Fore.LIGHTBLACK_EX,
        Fore.BLUE,
        Fore.MAGENTA,
        ),
    "%d-%m-%Y %H:%M:%S"
    )
handler.setFormatter(formatter)
root.addHandler(handler)

#DOTENV
TOKEN : Final[str] = os.environ['DISCORD_TOKEN']
TOPGG_TOKEN : Final[str] = os.environ['TOPGG_TOKEN']

#BOT CLASS
class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="/", help_command=None, intents=intents)
        self.discord_version = discord.__version__
        self.platform = platform.python_version()
        self.user_agent = f"Mr. Spooky/1.0 (discord.py {self.discord_version}, Python {self.platform})"

    @tasks.loop(hours=12)
    async def serverpost(self):
        c = (
            Style.RESET_ALL,
            Fore.LIGHTGREEN_EX,
            Fore.RED,
            Fore.LIGHTBLACK_EX
            )
        servers = len(bot.guilds)
        shards = bot.shard_count
        url = "https://top.gg/api/bots/1029085465086795866/stats"
        payload = {'server_count': servers, 'shard_count': shards}
        headers = {
            "Authorization": TOPGG_TOKEN,
            "User-Agent": self.user_agent
            }
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(url, headers=headers, data=payload)
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        print(f"{c[1]}POST - Top.gg!{c[0]}\nResponse: {response.status}\n{c[3]}----------------------")
                    else:
                        print(f"{c[2]}Something went wrong! - Top.gg{c[0]}\nResponse: {response.status}\n{c[3]}----------------------")
            except aiohttp.ClientConnectionError as e:
                print(f"{c[2]}Something went wrong! - Top.gg{c[0]}\n{e}\n{c[3]}----------------------")
            except aiohttp.ClientResponseError as e:
                print(f"{c[2]}Something went wrong! - Top.gg{c[0]}\n{e}\n{c[3]}----------------------")
            except asyncio.exceptions.TimeoutError as e:
                print(f"{c[2]}Something went wrong! - Top.gg{c[0]}\n{e}\n{c[3]}----------------------")


    @serverpost.before_loop
    async def before_serverpost(self):
        await self.wait_until_ready()

    #ON_READY
    async def on_ready(self):
        c = (
            Style.RESET_ALL,
            Fore.LIGHTGREEN_EX,
            Fore.LIGHTCYAN_EX,
            Fore.MAGENTA,
            Fore.LIGHTBLACK_EX
            )
        timestamp = datetime.datetime.now()
        amount = len(bot.guilds)
        shards = bot.shard_count
        print(f'{c[4]}----------------------')
        print(f'Mr. Spooky is online and in {amount} servers!')
        print(f'{c[2]}Shards:{c[0]} {shards}')
        print(f'{c[2]}Ping:{c[0]} {round(bot.latency, 3)}ms')
        print(f'{c[2]}API:{c[0]} {self.discord_version}')
        print(f'{c[2]}Python:{c[0]} {self.platform}')
        print(timestamp.strftime(f"{c[3]}T: %d/%m/%Y %H:%M:%S\n{c[4]}----------------------"))

        #BOT LOOPS
        bot.loop.create_task(status_task())

        if not bot.serverpost.is_running():
            await bot.serverpost.start()

    #LOAD COGS & SYNC SLASH COMMANDS
    async def setup_hook(self):
        c = (
            Style.RESET_ALL,
            Fore.LIGHTBLACK_EX,
            Fore.YELLOW,
            Fore.RED
            )
        for filename in os.listdir('./cogs'):
            if filename.startswith("__pycache__"):
                continue
            if filename.startswith("indev"):
                continue
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{c[1]}----------------------{c[0]}\nLoaded {c[2]}{filename}")
            else:
                print(f"{c[1]}----------------------\n{c[3]}Error loading {c[2]}{filename}")

        await self.tree.sync()
        print(f"{c[1]}----------------------")
        print("Synced Slash Commands")
        print(f"{c[1]}----------------------")


#DEFINE BOT
bot = Bot()

#COG CONTROL COMMANDS WON'T WORK DUE TO INTENTS. THIS IS INTENTIONAL.

#LOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.channel.send(f"Loaded **{extension}.py** successfully!")


#UNLOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.channel.send(f"Unloaded **{extension}.py** successfully!")


#RELOAD COG COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")
    await ctx.channel.send(content=f"Reloaded **{extension}.py** successfully!")


#SHUTDOWN COMMAND
@bot.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Shutting down...")
    await bot.close()


#BOT STATUS
@bot.event
async def status_task():
    amount = len(bot.guilds)
    while True:
        await bot.change_presence(activity=discord.Game(name="BOO!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="Supports Slash Commands!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name="OoOoOoo I'm a spooky ghost!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name=f"in {len(bot.guilds)} servers!"))
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="TeeTwoNot while he sleeps"))
        await asyncio.sleep(120)

async def main():
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
