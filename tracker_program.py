import discord
from pysolana.api import*
import asyncio
res = getBalance('2ApaxgJpTgjaoANNTwxKvJXk9F4upRCmcXYLoNxBdMZJ');
print(int((res['value']))/(10**9))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    text_channel = client.get_channel(1072257836861624401)
    print(text_channel);
    await text_channel.send('Test')


client.run('MTA3MjI1NDI4MTMxNjU2OTIzOA.G5uKsU.LeJSZvDxlZsfobB3eIHfDoH8rm9vHiDeMUjhpk')
