import discord
from discord.ext import commands
import asyncio
import requests


TOKEN = ""
bot = commands.Bot(command_prefix="#!")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if 'кот' in message.content.lower():
        json = requests.get("https://api.thecatapi.com/v1/images/search").json()
        await message.channel.send(json[0]['url'])


bot.run(TOKEN)

