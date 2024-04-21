import discord
from discord.ext import commands
import asyncio
import subprocess
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# urlday API endpoints
URLDAY_API_BASE_URL = "https://www.urlday.com/api/v1"
URLDAY_API_KEY = "9tMDiMwZZBSNAN27LbTYW0d78yP4WC3hOlMkm1ftlPxyjLOnbsMyJEF6XULK"  # Replace with your API key

async def shorten_url(url, alias=None):
    api_url = f"{URLDAY_API_BASE_URL}/links"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {URLDAY_API_KEY}"
    }
    data = {
        "url": url,
        "alias": alias
    }
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("url")
    else:
        return None

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
        shortened_url = await shorten_url(elink)
        if shortened_url:
            await message.channel.send(f"{message.author.mention}, here is your file from {platform}: {shortened_url}")
        else:
            await message.channel.send(f"Sorry, {message.author.mention}, couldn't shorten the link for {platform}.")
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
