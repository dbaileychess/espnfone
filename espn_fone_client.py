import discord
import asyncio
from espn_commands import *

class Command:
    def __init__(self, help, command):
        self.help = help
        self.command = command

    def __call__(self):
        return self.command()

class EspnFoneClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.league = kwargs["league"]
        self.dev_channel_id = kwargs["dev_channel_id"]
        self.commands = {}
        self.register_handler(
            "scores",
            "List Current Scores",
            lambda: get_scoreboard_short(self.league),
        )
        self.register_handler(
            "matchups",
            "List current matchups",
            lambda: get_matchups(self.league),
        )
        self.register_handler(
            "projections",
            "List of Projected Scores",
            lambda: get_projected_scoreboard(self.league),
        )
        self.register_handler(
            "powerrankings",
            "Power Rankings",
            lambda: get_power_rankings(self.league),
        )

    async def setup_hook(self) -> None:
        pass
        # create the background task and run it in the background
        # self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(self.dev_channel_id)  # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(10)  # task runs every 60 seconds

    def help_message(self):
        options = [
            "Why don't you just tell me the name of the _command_ you selected?",
            "",
        ]
        for key, value in self.commands.items():
            options.append("**%s** -- %s" % (key, value.help))

        return "\n".join(options)

    def register_handler(self, name, help, command, *args):
        self.commands[name] = Command(help, command, *args)

    async def on_message(self, message):
        if message.author == self.user:
            # Don't respond to myself
            return

        if self.user not in message.mentions:
            # Don't respond to messages without a direct mention
            return

        # Search for the keywords of the registered commands
        for key, value in self.commands.items():
            if key in message.content:
                await message.channel.send(value())
                return

        if "hello" in message.content:
            await message.channel.send("**Hello** and welcome to ESPNFone!")
        else:
          await message.channel.send(self.help_message())
