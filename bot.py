"""
+------------------------------------------------------------+
| * Devify is a discord bot written in python which adds   * |
| * easy developer communication templates to discord      * |
|                                                            |
|                                                            |
| * Devify                                                 * |
| * fall 24 - Nathan Ceci                                  * |
+------------------------------------------------------------+
"""

import discord
import os
import asyncio
from discord.ext import commands
from config import DISCORD_TOKEN, COMMAND_PREFIX

# Define what the bot intends to do with disocrd
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start(DISCORD_TOKEN)

asyncio.run(main())