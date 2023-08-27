import json
import ssl

import aiohttp
import discord
import requests
from discord.ext import commands


TOKEN = "MTEzOTM0OTUwNzg4MTA1MDExMg.GmBoiP.me74gFJn1WR4u4Zwy539maFi8Nr6KAhMGuqaUUg"
api_key = "9314ce0f45ad4139a0d151042230408"

intents = discord.Intents.default()

intents.members = True

# create instance of discord bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


async def create_session():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))


# command to fetch weather
@bot.command(name='weatherBOT')
async def fetch_weather(ctx, *, city: str):
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=yes")
    data = json.loads(response.text)
    if 'error' in data:
        await ctx.send(data['error']['message'])
    else:
        weather_info = data['current']
        city_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        condition = weather_info['condition']['text']
        icon_url = "http:" + weather_info['condition']['icon']
        temperature = weather_info['temp_c']
        localtime = data['location']['localtime']
        # Create Embedded message
        embed = discord.Embed(
            title=f"weather in {city_name}, {region}, {country}",
            description=f"""**Condition:{condition}"\n
                            **Temperature: {temperature} degrees\n
                            **Local time: {localtime}\n
                            """,
            color=discord.color.blue()
        )
        # embed.set_thumbnail(url=icon_url)
        await ctx.send(embed=embed)


# Run the BOT
bot.run(TOKEN)
