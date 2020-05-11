from const import TOKEN, KEY
import discord
from discord.ext import commands
import asyncio
import requests


bot = commands.Bot(command_prefix="#!")
city = "Алматы"


def get_coordinates(city_name):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        'geocode': city_name,
        'format': 'json'
    }
    response = requests.get(url, params)
    json = response.json()
    coordinates_str = json['response']['GeoObjectCollection'][
        'featureMember'][0]['GeoObject']['Point']['pos']
    long, lat = map(float, coordinates_str.split())
    return long, lat


def calc(place):
    coords = get_coordinates(place)
    params = {
        "lon": coords[0],
        "lat": coords[1],
        "lang": "ru_RU"
    }
    response = requests.get("https://api.weather.yandex.ru/v1/forecast",
                            params=params, headers={"X-Yandex-API-Key": KEY})
    return response.json()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="help_bot")
async def help_bot(ctx):
    await ctx.send('place - to change place\n'
                   'current - current weather\n'
                   'forecast x - forecast weather for x days')


@bot.command(name="place")
async def change_place(ctx, place):
    global city
    city = place
    await ctx.send("Done")


@bot.command(name="current")
async def current_weather(ctx):
    info = calc(city)
    text = "Current weather in {} for {}:\n".format(city, info['now_dt'])
    text += "Temperature: {}\n".format(info['fact']['temp'])
    text += "Pressure: {} mm\n".format(info['fact']['pressure_mm'])
    text += "Humidity: {} %\n".format(info['fact']['humidity'])
    text += "{}\n".format(info['fact']['condition'])
    text += "Wind {}, {} m/s\n".format(info['fact']['wind_dir'], info['fact']['wind_speed'])
    await ctx.send(text)


@bot.command(name="forecast")
async def forecast_weather(ctx, days):
    info = calc(city)
    text = ""
    for i in range(0, int(days)):
        print(info['forecasts'])
        data = info['forecasts'][i]
        text += "Weather forecast in {} for {}:\n".format(city, data['date'])
        text += "Temperature: {}\n".format(data['parts']['day']['temp_avg'])
        text += "Pressure: {} mm\n".format(data['parts']['day']['pressure_mm'])
        text += "Humidity: {} %\n".format(data['parts']['day']['humidity'])
        text += "{}\n".format(data['parts']['day']['condition'])
        text += "Wind {}, {} m/s\n\n\n\n".format(data['parts']['day']['wind_dir'], data['parts']['day']['wind_speed'])
    await ctx.send(text)


bot.run(TOKEN)
