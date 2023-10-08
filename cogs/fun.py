#IMPORTS
import discord
import random
import aiohttp
import time
from components import lists

#FROM DISCORD
from discord import app_commands, ui
from discord.ext import commands
from discord.app_commands import Choice, AppCommandError

#FROM OTHER
from components import lists
from re import search


#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #MEME COMMAND
    @app_commands.command(name="meme", description="Spooky memes just for you!")
    @app_commands.checks.cooldown(1, 10.0)
    async def meme(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        subreddit = lists.halloweensub

        async with aiohttp.ClientSession() as clientsesh:
            async with clientsesh.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()

                if reddit.status != 200:
                    embed = discord.Embed(title="Something went wrong!", description=f"Try again later. (Status Code: {reddit.status})", color=0xeb6123)
                    await interaction.followup.send(embed=embed)
                else:
                    while True:
                        random_post = res["data"]["children"][random.randint(0, 24)]
                        image_url = str(random_post["data"]["url"])
                        if search(".jpg|.jpeg|.png|.gif$", image_url):
                            break
                        else:
                            image_url = None
                    
                    permalink = random_post["data"]["permalink"]
                    title = random_post["data"]["title"]
                    subreddit_title = random_post["data"]["subreddit"]

                    embed = discord.Embed(title=f"{title}", description="", url=f"https://reddit.com{permalink}", color=0xeb6123)
                    embed.set_image(url=image_url)
                    embed.set_footer(text=f"By r/{subreddit_title}")
                    await interaction.followup.send(embed=embed)

    @meme.error
    async def meme_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    #SPOOKIFY COMMAND
    @app_commands.command(name="spookify", description="Spook-ifies your text!")
    async def spookify(self, interaction: discord.Interaction, msg: str):
        spook = " 🎃 "
        msg = msg.replace(" ", spook)
        await interaction.response.send_message("🎃 " + msg + " 🎃")


    #GHOSTIFY COMMAND
    @app_commands.command(name="ghostify", description="Ghost-ifies your text!")
    async def ghostify(self, interaction: discord.Interaction, msg: str):
        ghost = " 👻 "
        msg = msg.replace(" ", ghost)
        await interaction.response.send_message("👻 " + msg + " 👻")


    #SPOOKYJOKE COMMAND
    @app_commands.command(name="spookyjoke", description="Tells you a spooky joke!")
    async def spookyjoke(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(lists.spookyjoke))

    
    #DOOT COMMAND
    @app_commands.command(name="doot", description="A skeleton dooting a trumpet. Because why not?")
    async def doot(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://tenor.com/view/skeleton-trumpet-gif-4622525')

    
    #SPOOKYSTORY COMMAND
    @app_commands.command(name="spookystory", description="Give random words and get a customized spooky story!")
    @app_commands.choices(story = [
        Choice(name = "Story 1 - The Kidnapping", value = "story1"),
        Choice(name = "Story 2 - A Spooky Encounter", value = "story2"),
        Choice(name = "Story 3 - Trick or Treat", value = "story3"),
        Choice(name = "Story 4 - COMING SOON", value = "story4"),
        Choice(name = "Story 4 - COMING SOON", value = "story5")
    ])
    async def spookystory(self, interaction: discord.Interaction, story: str):
        if story == "story1":
            await interaction.response.send_modal(SpookyStory1())
        elif story == "story2":
            await interaction.response.send_modal(SpookyStory2())
        elif story == "story3":
            await interaction.response.send_modal(SpookyStory3())
        elif story == "story4":
            await interaction.response.send_modal(SpookyStory4())
        elif story == "story5":
            await interaction.response.send_modal(SpookyStory5())


class SpookyStory1(ui.Modal, title="Spooky Story Generator!"):

    name = ui.TextInput(label="Name", style=discord.TextStyle.short, placeholder="Give a name to your character!", required=True)
    emotion = ui.TextInput(label="Emotion", style=discord.TextStyle.short, placeholder="Give an emotion adjective! (e.g. happy, sad)", required=True)
    music = ui.TextInput(label="Music", style=discord.TextStyle.short, placeholder="What music does your character listen to? (e.g. jazz, rap)", required=True)
    drink = ui.TextInput(label="Drink", style=discord.TextStyle.short, placeholder="What is your character's favourite drink?", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
f"# Once upon a time...\n\
    There was __{self.name}__, chilling on the couch, watching spooky memes on the phone, and sipping on __{self.drink}__.\n\
    And, since it's spooky month, and it's the best month of the year (obviously), __{self.name}__ decided to do something different this time around.\n\
    So, __{self.name}__ decided to ***kidnap a stranger*** and ***tie him on a chair*** in the basement. Perfectly normal for spooky month.\n\
    __{self.name}__ then played __{self.music}__ on max volume and left.\n\
    The stranger felt __{self.emotion}__ while being tortured by the loud music.\n\
    Then the stranger got spooked by a spooky ghost and died.\n\
## THE END."
        )

        
class SpookyStory2(ui.Modal, title="Spooky Story Generator!"):

    name = ui.TextInput(label="Name", style=discord.TextStyle.short, placeholder="Give a name to your character!", required=True)
    number = ui.TextInput(label="Number", style=discord.TextStyle.short, placeholder="Give any number!", required=True)
    emotion = ui.TextInput(label="Emotion", style=discord.TextStyle.short, placeholder="Give an emotion adjective! (e.g. happy, sad)", required=True)
    verb = ui.TextInput(label="Verb", style=discord.TextStyle.short, placeholder="Give a verb! (e.g. running, swimming, eating)", required=True)
    say = ui.TextInput(label="Say Something", style=discord.TextStyle.short, placeholder="Something the character wants to say (e.g. I love you)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
f"# Once upon a time...\n\
    There was __{self.name}__ and their huge mansion! The mansion had all sorts of rooms... A theater, a bar, and a lot of jacuzzis!\n\
    One day, while __{self.name}__ was relaxing in jacuzzi #__{self.number}__, a spooky ghost suddenly appeared in front of them!\n\
    __{self.name}__ and the ghost stared at eachother very awkwardly, until the ghost started speaking in its deep, scary voice:\n\
    'Hello stranger... I would like to say something...'\n\
    __{self.name}__, being extremely confused, agreed to hear what the ghost had to say.\n\
    '__{self.say}__', said the ghost.\n\
    'What?', __{self.name}__ responded.\n\
    The ghost then started __{self.verb}__.\n\
    __{self.name}__ felt __{self.emotion}__ with what the ghost had to say.\n\
    Then __{self.name}__ got jumpscared by their spooky pet spider and died.\n\
## THE END."
            )


class SpookyStory3(ui.Modal, title="Spooky Story Generator!"):

    outfit1 = ui.TextInput(label="Costume 1", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. 'a ghost costume')", required=True)
    outfit2 = ui.TextInput(label="Costume 2", style=discord.TextStyle.short, placeholder="Name a second costume! (e.g. 'a zombie costume')", required=True)
    treat = ui.TextInput(label="Treat", style=discord.TextStyle.short, placeholder="Your favourite treat! (e.g. candy, chocolate)", required=True)
    feeling = ui.TextInput(label="Feeling", style=discord.TextStyle.short, placeholder="Give a feeling! (e.g. shocked, confused)", required=True)
    neighbour = ui.TextInput(label="Neighbour", style=discord.TextStyle.short, placeholder="Name a neighbour! (e.g. grandma, teacher)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
f"# Once upon a time...\n\
    There were two friends chillin' in their very expensive jacuzzi. (these stories have way too many for whatever reason)\n\
    They were chatting about how spooktober is arriving soon, and what they should do.\n\
    Suddenly, they heard their phones go off...they were both __{self.feeling}__. After a short pause, they both said to each other with excitement in their eyes...\n\
    '**IT'S SPOOKTOBER!!!**'\n\
    So they got out of the jacuzzi and quickly went inside to change to their spooky costumes!\n\
    The first one was a __{self.outfit1}__ costume! Very spooky.\n\
    The second one was a __{self.outfit2}__ costume! Even spookier!\n\
    They then got their snack bags and went on their way to Trick or Treat!\n\
    Their favourite treat was __{self.treat}__! That's really tasty!\n\
    The first house they went to was their neighbour __{self.neighbour}__'s house!\n\
    They knocked on the door and the door opened slowly...\n\
    'TRICK OR TREAT?', the friends shouted.\n\
    Then the __{self.neighbour}__ got a heart attack and almost died but the ambulance arrived in time.\n\
    (you really thought someone was going to die again, shame on you)\n\
## THE END."
            )

class SpookyStory4(ui.Modal, title="Spooky Story Generator!"):

    variable = ui.TextInput(label="Costume 1", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. 'a ghost costume')", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("COMING SOON!")
           

class SpookyStory5(ui.Modal, title="Spooky Story Generator!"):

    variable = ui.TextInput(label="Costume 1", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. 'a ghost costume')", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("COMING SOON!")


async def setup(bot):
    await bot.add_cog(Fun(bot))