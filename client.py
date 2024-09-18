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
from discord.ext import commands
import os
import asyncio  # Only needed if you have other asynchronous tasks
from config import DISCORD_TOKEN, COMMAND_PREFIX, DEV_GUILD_ID

# Define the bot's intents
intents = discord.Intents.all()

# Initialize the bot
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.slash_command(    
        name="reload",
        description="Hot reloads all cogs.",
        guild_ids=DEV_GUILD_ID,
)
async def reload_extensions(ctx):
    """
    Hot reloading for cogs
    """
    # Defer the response to give the bot more time to process
    await ctx.defer()

    # Loop through the cogs folder and reload extensions
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f"Reloaded: {filename}")
            except Exception as e:
                print(f"Failed to reload: {filename}\n{str(e)}")
                await ctx.followup.send(f"Failed to reload: {filename}\n{str(e)}")

    # Send a final message when the reload process is complete
    await ctx.followup.send("All cogs hot-reloaded successfully!")

def load_extensions():
    """
    Synchronously load all extensions (cogs) from the cogs directory.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            try:
                client.load_extension(extension)
                print(f"Loaded extension {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

def main():
    """
    Main function to load extensions and run the bot.
    """
    load_extensions()
    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
