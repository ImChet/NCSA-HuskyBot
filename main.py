import asyncio
import logging.handlers
import os

import discord
from discord.ext import commands

from apikeys import discordBotAPIKey
from cogs.TicketingSystem import TicketLauncher, TicketInternals
from functions import checkDirectoryExists, getCurrentDateTime, ensureTicketingJSON_Exists


# HuskyBot constructor class
class CreateBot(commands.Bot):
    def __init__(self):
        # Specifies intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True
        super().__init__(command_prefix="/", intents=intents,
                         activity=discord.Activity(type=discord.ActivityType.watching, name='over the universe'),
                         status=discord.Status.do_not_disturb)

    async def setup_hook(self) -> None:
        print("HuskyBot spinning up...\n-----")

    async def on_ready(self):
        self.add_view(TicketLauncher())
        self.add_view(TicketInternals())
        print(f'We have successfully logged in as {self.user} on {getCurrentDateTime()}.\n-----')


HuskyBot = CreateBot()

# Defines the initial_extensions array
initial_extensions = []

# Logging setup / parameters
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logHandler = logging.FileHandler(filename='HuskyBot.log', encoding='utf-8', mode='w')
loggingDateFormat = '%Y-%m-%d %H:%M:%S'
loggingFormatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', loggingDateFormat, style='{')
logHandler.setFormatter(loggingFormatter)
logger.addHandler(logHandler)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append('cogs.' + filename[:-3])


async def main():
    # Ensures the all the needed working directories exist
    checkDirectoryExists('WorkingFiles/')
    checkDirectoryExists('WorkingFiles/FilesToCreate/')
    checkDirectoryExists('WorkingFiles/Databases/')
    ensureTicketingJSON_Exists()

    # Loads all cogs
    for extension in initial_extensions:
        await HuskyBot.load_extension(extension)


if __name__ == '__main__':
    asyncio.run(main())

HuskyBot.run(discordBotAPIKey, log_handler=None)
