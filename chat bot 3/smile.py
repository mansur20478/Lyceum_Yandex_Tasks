from const import TOKEN
from discord.ext import commands
import asyncio
import random

base = ['☺', '😂', '❤', '😍', '😭', '🔥']
points = [0, 0]
bot = commands.Bot(command_prefix="!#")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has joined to Discord!')


@bot.event
async def on_message(message):
    sender = str.split(str(message.author), '#')
    if sender[0] == bot.user.name:
        return
    if message.content == "/stop":
        points[0], points[1] = 0, 0
        await message.channel.send("Restart")
    else:
        random.shuffle(base)
        try:
            if len(base) != 0:
                pos = int(message.content)
                enemy = base.pop(pos % len(base))
                me = base.pop(random.randint(0, len(base)) % len(base))
                if me > enemy:
                    points[0] += 1
                else:
                    points[1] += 1
                await message.channel.send(
                    f'Your emoji {enemy}\nBot emoji {me}\nScore: You {points[1]} - Bot {points[0]}')
                if len(base) == 0:
                    text = f'Emoticons are over\nScore: You {points[1]} - Bot {points[0]}\n'
                    if points[0] == points[1]:
                        text += "Draw"
                    elif points[0] > points[1]:
                        text += "You lose"
                    else:
                        text += "You win"
                    await message.channel.send(text)
            else:
                raise Exception
        except Exception as exc:
            await message.channel.send("Error")


bot.run(TOKEN)
