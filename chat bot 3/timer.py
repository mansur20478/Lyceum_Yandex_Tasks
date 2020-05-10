from const import TOKEN
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="!#")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="set_timer")
async def set_timer(ctx, hours, minutes):
    await ctx.send(f"The timer should start in {hours} and {minutes} minutes")
    await asyncio.sleep(int(hours) * 60 * 60 + int(minutes) * 60)
    await ctx.send("Time X has come")


bot.run(TOKEN)
