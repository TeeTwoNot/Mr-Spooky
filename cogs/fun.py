#IMPORTS
import discord
import random
import aiohttp
import asyncio

#FROM DISCORD
from discord import app_commands, ui
from discord.ext import commands
from discord.app_commands import Choice

#FROM OTHER
from components import lists


#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #MEME COMMAND
    @app_commands.command(name="halloween", description="Halloween reddit posts!")
    async def halloween(self, interaction: discord.Interaction) -> None:
        subreddit = lists.halloweensub

        async with aiohttp.ClientSession() as clientsesh:
            async with clientsesh.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()

                random_post = res["data"]["children"][random.randint(0, 25)]
                image_url = random_post["data"]["url"]
                title = random_post["data"]["title"]
                subreddit_title = random_post["data"]["subreddit"]

                embed = discord.Embed(
                    title=f"{title}",
                    description="", 
                    color=0xEB6123
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"By r/{subreddit_title}")
                await interaction.response.send_message(embed=embed)


    #SPOOKIFY COMMAND
    @app_commands.command(name="spookify", description="Spookifies your text!")
    async def spookify(self, interaction: discord.Interaction, msg: str):
        spook = " 🎃 "
        msg = msg.replace(" ", spook)
        await interaction.response.send_message("🎃 " + msg + " 🎃")


    #SPOOKYJOKE COMMAND
    @app_commands.command(name="spookyjoke", description="Very spooky!")
    async def spookyjoke(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(lists.spookyjoke))

    
    #DOOT COMMAND
    @app_commands.command(name="doot", description="Doot!")
    async def doot(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://tenor.com/view/skeleton-trumpet-gif-4622525')

    
    #SPOOKYSTORY COMMAND
    @app_commands.command(name="spookystory", description="Very spooky!")
    @app_commands.choices(story = [
        Choice(name = "Story 1 - The Kidnapping", value = "story1"),
        Choice(name = "Story 2 - A Spooky Encounter", value = "story2"),
        Choice(name = "Story 3 - Trick or Treat", value = "story3")
    ])
    async def spookystory(self, interaction: discord.Interaction, story: str):
        if story == "story1":
            await interaction.response.send_modal(SpookyStory1())
        elif story == "story2":
            await interaction.response.send_modal(SpookyStory2())
        elif story == "story3":
            await interaction.response.send_modal(SpookyStory3())


class SpookyStory1(ui.Modal, title="Spooky Story Generator!"):

    name = ui.TextInput(label="Name", style=discord.TextStyle.short, placeholder="Give a name to your character!", required=True)
    emotion = ui.TextInput(label="Emotion", style=discord.TextStyle.short, placeholder="Give an emotion adjective! (e.g. happy, sad)", required=True)
    music = ui.TextInput(label="Music", style=discord.TextStyle.short, placeholder="What music does your character listen to? (e.g. jazz, rap)", required=True)
    drink = ui.TextInput(label="Drink", style=discord.TextStyle.short, placeholder="What is your character's favourite drink?", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Once upon a time...\n\nThere was __{self.name}__, chilling on the couch, watching spooky memes on their phone, and sipping on __{self.drink}__.\nAnd, since it's spooky month, and it's the best month of the year (obviously), __{self.name}__ decided to do something different this time around.\n__{self.name}__ decided to *kidnap a stranger* and *tie him on a chair* in the basement.\n__{self.name}__ then put __{self.music}__ music on max volume and left.\nThe stranger felt __{self.emotion}__ while being tortured by the loud music.\nThen the stranger got spooked by a spooky ghost and died.\n\nTHE END."
            )

        
class SpookyStory2(ui.Modal, title="Spooky Story Generator!"):

    name = ui.TextInput(label="Name", style=discord.TextStyle.short, placeholder="Give a name to your character!", required=True)
    number = ui.TextInput(label="Number", style=discord.TextStyle.short, placeholder="Give any number!", required=True)
    emotion = ui.TextInput(label="Emotion", style=discord.TextStyle.short, placeholder="Give an emotion adjective! (e.g. happy, sad)", required=True)
    verb = ui.TextInput(label="Verb", style=discord.TextStyle.short, placeholder="Give a verb! (e.g. running, swimming, eating)", required=True)
    say = ui.TextInput(label="Say Something", style=discord.TextStyle.short, placeholder="Something the character wants to say (e.g. I love you)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Once upon a time...\n\nThere was __{self.name}__ and their huge mansion! The mansion had all sorts of rooms... A theater, a bar, and a lot of jacuzzis.\nOne day, while __{self.name}__ was relaxing in jacuzzi #__{self.number}__, a spooky ghost suddenly appeared in front of them!\nThey stared at eachother very awkwardly, until the ghost started speaking in its deep voice.\n'Hello stranger... I would like to say something...'\n__{self.name}__, being extremely confused, agreed to hear what the ghost had to say.\n'__{self.say}__', said the ghost.\n'What?', __{self.name}__ responded.\nThe ghost then started __{self.verb}__.\n__{self.name}__ felt __{self.emotion}__ with what the ghost said...\nThen they got jumpscared by their spooky pet spider and died.\n\nTHE END."
            )


class SpookyStory3(ui.Modal, title="Spooky Story Generator!"):

    outfit1 = ui.TextInput(label="Costume 1", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. 'a ghost costume')", required=True)
    outfit2 = ui.TextInput(label="Costume 2", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. 'a zombie costume')", required=True)
    treat = ui.TextInput(label="Treat", style=discord.TextStyle.short, placeholder="Your favourite treat! (e.g. candy, chocolate)", required=True)
    feeling = ui.TextInput(label="Feeling", style=discord.TextStyle.short, placeholder="Give a feeling! (e.g. shocked, confused)", required=True)
    neighbour = ui.TextInput(label="Neighbour", style=discord.TextStyle.short, placeholder="Name a neighbour! (e.g. grandma, teacher)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        spooktober = "IT'S SPOOKTOBER!"
        await interaction.response.send_message(
            f"Once upon a time...\n\nThere were two bros chillin' in a hot tub, five feet apart cuz they're not gay (haha get it)\nThey were chatting about how spooktober is arriving soon, and what they should do.\nSuddenly, they heard bells going off...they were both __{self.feeling}__. After a short pause, they both said to each other with excitement in their eyes...\n'{spooktober}'\nSo they got out of the hot tub and quickly went inside to change to their spooky costumes!\nThe first outfit was __{self.outfit1}__, very spooky.\nThe second outfit was __{self.outfit2}__, even spookier!\nThey then got their spooky bags and went on their way to Trick or Treat!\nTheir favourite treat was __{self.treat}__! That's a really good treat to be fair.\nThe first house they went to was their neighbour __{self.neighbour}__'s house!\nThey knocked on the door and the __{self.neighbour}__ slowly opened the door...\n'TRICK OR TREAT?', the bros shouted.\nThen the __{self.neighbour}__ got a heart attack and almost died but they got to the hospital in time.\n(you really thought someone was going to die again, shame on you)\n\nTHE END."
            )


async def setup(bot):
    await bot.add_cog(Fun(bot))