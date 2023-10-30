#IMPORTS
import discord
import random
import time

#FROM DISCORD
from discord import app_commands, ui
from discord.ext import commands
from discord.app_commands import Choice, AppCommandError

#FROM OTHER
from datetime import timedelta
from components import lists
from re import search
from aiohttp_client_cache import CachedSession, CacheBackend

cache = CacheBackend(expire_after=timedelta(seconds=120))

#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    #MEME COMMAND
    @app_commands.command(name="meme", description="Spooky memes just for you!")
    @app_commands.checks.cooldown(1, 5.0)
    async def meme(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        subreddit = [
            'https://www.reddit.com/r/halloween/new.json?limit=100',
            'https://www.reddit.com/r/spooktober/new.json?limit=100'
        ]
        async with CachedSession(cache=cache) as session:
            async with session.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()
                while True:
                    counter = 0
                    random_post = res["data"]["children"][random.randint(0, 99)]
                    image_url = str(random_post["data"]["url"])
                    if search(".jpg|.jpeg|.png|.gif$", image_url):
                        break
                    else:
                        counter += 1
                        if counter == 100:
                            image_url = None
                            break

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
    

    #HOWLONG COMMAND
    @app_commands.command(name="howlong", description="How long until Halloween?")
    async def howlong(self, interaction: discord.Interaction):
        unixtime = int(time.time())
        if unixtime >= 1698710400:
            embed = discord.Embed(title="Halloween is <t:1698710400:R>! (Coordinated Universal Time)", description="It's halloween!!!", color=0xeb6123)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Halloween is <t:1698710400:R>! (Coordinated Universal Time)", description="It's almost halloween!", color=0xeb6123)
            await interaction.response.send_message(embed=embed)

    
    #SPOOKYSTORY COMMAND
    @app_commands.command(name="spookystory", description="Give random words and get a customized spooky story!")
    @app_commands.choices(story = [
        Choice(name = "Story 1 - The Kidnapping", value = "story1"),
        Choice(name = "Story 2 - A Spooky Encounter", value = "story2"),
        Choice(name = "Story 3 - Trick or Treat", value = "story3"),
        Choice(name = "Story 4 - Spooky Decor!", value = "story4"),
        Choice(name = "Story 5 - The Creator", value = "story5")
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

    outfit1 = ui.TextInput(label="Costume 1", style=discord.TextStyle.short, placeholder="Name a costume! (e.g. ghost, zombie)", required=True)
    outfit2 = ui.TextInput(label="Costume 2", style=discord.TextStyle.short, placeholder="Name a second costume! (e.g. spider, skeleton)", required=True)
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
    Then __{self.neighbour}__ got a heart attack and almost died but the ambulance arrived in time.\n\
    (you really thought someone was going to die again, shame on you)\n\
## THE END."
)

class SpookyStory4(ui.Modal, title="Spooky Story Generator!"):

    decor = ui.TextInput(label="Decoration", style=discord.TextStyle.short, placeholder="Name a scary decoration! (e.g. skeleton, spider, pumpkin)", required=True)
    entity = ui.TextInput(label="Decoration", style=discord.TextStyle.short, placeholder="Name an entity! (e.g. spirit, ghost)", required=True)
    action = ui.TextInput(label="Action", style=discord.TextStyle.short, placeholder="Describe an action! (e.g. spooking, making pancakes)", required=True)
    celeb = ui.TextInput(label="Celebrity", style=discord.TextStyle.short, placeholder="Name a celebrity! (e.g. Will Smith)", required=True)
    num = ui.TextInput(label="Random Number", style=discord.TextStyle.short, placeholder="Type a random number!", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
f"# Once upon a time...\n\
    There was a plastic __{self.decor}__ decoration on the porch of a house.\n\
    This was like any other decoration, meant to spice up the porches of houses during spooky season.\n\
    However, most people that passed by that porch seemed a bit *too* scared of the __{self.decor}__.\n\
    Something seemed off about that __{self.decor}__, but it had to be just a decoration. Right?\n\
    It turns out that a __{self.entity}__ had haunted the __{self.decor}__!\n\
    On Halloween Day, the __{self.entity}__ suddenly woke up and left the porch!\n\
    Spectators saw the __{self.decor}__ running around and __{self.action}__.\n\
    *'What?'*, they thought to themselves.\n\
    Then, out of nowhere, __{self.celeb}__ showed up and started chasing down the __{self.decor}__!\n\
    After about __{self.num}__ hours, __{self.celeb}__ caught the __{self.decor}__, saving the neighbourhood.\n\
    At last, __{self.celeb}__ had saved Halloween for everyone.\n\
## THE END."
)
           

class SpookyStory5(ui.Modal, title="Spooky Story Generator!"):

    feeling = ui.TextInput(label="Feeling", style=discord.TextStyle.short, placeholder="Give a feeling! (e.g. determined, motivated)", required=True)
    num = ui.TextInput(label="Random Number", style=discord.TextStyle.short, placeholder="Type a random number!", required=True)
    time = ui.TextInput(label="Time", style=discord.TextStyle.short, placeholder="Give a time unit! (e.g. hours, seconds, days)", required=True)
    say = ui.TextInput(label="Say Something", style=discord.TextStyle.short, placeholder="Something the character wants to say (e.g. I love you)", required=True)
    feeling2 = ui.TextInput(label="Feeling", style=discord.TextStyle.short, placeholder="Give a feeling! (e.g. scared, confused)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
f"# Once upon a time...\n\
    TeeTwoNot, the creator of this bot, ran out of ideas for stories.\n\
    Halloween was approaching and he still hadn't finished the 5th story.\n\
    He had to do something as soon as possible. That COMING SOON™ placeholder looked really bad!\n\
    So, he sat down on his desk, opened his computer, and started typing!\n\
    He felt __{self.feeling}__ while typing away. Look at him go!\n\
    After an impressive __{self.num}__ __{self.time}__, he finally finished writing the story.\n\
    As he was about to click the button to publish the story, he heard a knock on his door.\n\
    *Knock knock.*\n\
    'Who's there?' he replied.\n\
    '__{self.say}__', a deep, scary voice said.\n\
    'I didn't hear that.', TeeTwoNot said.\n\
    'Wake up.', said the deep, scary voice.\n\
    TeeTwoNot felt __{self.feeling2}__. 'What's happening?', he thought to himself.\n\
    He then suddenly woke up.\n\
    He realized he fell asleep at his desk and dreamed of writing the story.\n\
    He suddenly heard a deep, scary voice from his headphones say:\n\
    'Bro still hasn't finished the 5th story. L + Ratio + Maidenless.'\n\
## THE END."
)


async def setup(bot):
    await bot.add_cog(Fun(bot))