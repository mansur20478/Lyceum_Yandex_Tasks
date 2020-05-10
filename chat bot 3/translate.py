from const import TOKEN
from discord.ext import commands
import asyncio
import requests

need = "ru-en"
bot = commands.Bot(command_prefix="!#")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="help_bot")
async def set_timer(ctx):
    await ctx.send("set_lang для смены языка, пример set_lang ru-en. Означает что с русского на английский\n"
                   "text перевод, пример text картошка. Ответ будет дан potato, так как стоит ru-en")


@bot.command(name="set_lang")
async def set_timer(ctx, text):
    global need
    need = text
    await ctx.send("set_lang для смены языка, пример set_lang ru-en. Означает что с русского на английский\n"
                   "text перевод, пример text картошка. Ответ будет дан potato, так как стоит ru-en")


@bot.command(name="text")
async def trans(ctx, text):
    params = {
        'key': 'trnsl.1.1.20200510T063837Z.9d452e880ab33516.ac524792a3446e1ae81742675030dde8fa99134e',
        'text': text,
        'lang': need
    }
    info = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params=params).json()
    print(info)
    await ctx.send(info['text'][0])


bot.run(TOKEN)
