import discord
from discord.ext import commands
import asyncio
import subprocess
import requests
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def process_link(message, platform, filename, script_name):
    wait_message = await message.channel.send(f"Please wait a moment, getting your file from {platform}...")

    with open(filename, "w") as file:
        file.write(message.content)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: subprocess.run(["python", script_name]))

    max_attempts = 10
    attempts = 0
    elink = ""

    while attempts < max_attempts and not elink:
        with open("elink.txt", "r") as elink_file:
            elink = elink_file.read().strip()

        if not elink:
            attempts += 1
            await asyncio.sleep(5)

    await wait_message.delete()
    await message.delete()

    if elink:
        await message.channel.send(f"{message.author.mention}, here is your file from {platform}: {elink}")
        # Clear elink.txt
        with open("elink.txt", "w") as elink_file:
            elink_file.write("")
    else:
        await message.channel.send(f"Sorry, couldn't find a link for {platform}. Please try again later.")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
TOKEN = os.environ.get('token')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "facebook.com" in message.content:
        asyncio.create_task(process_link(message, "Facebook", "facebook_link.txt", "newdownloader.py"))
    elif "instagram.com" in message.content:
        asyncio.create_task(process_link(message, "Instagram", "instagram_link.txt", "instadownloader.py"))

    await bot.process_commands(message)

bot.run(TOKEN)
