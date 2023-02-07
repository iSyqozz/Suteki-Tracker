import discord
from pysolana.api import*
import asyncio
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    text_channel = client.get_channel(1072257836861624401)
    print(text_channel);
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == 0 and current_time.tm_min == 0:
            
            curr_royalties = getBalance('2ApaxgJpTgjaoANNTwxKvJXk9F4upRCmcXYLoNxBdMZJ');
            curr_royalties = float((curr_royalties['value']))/(10**9)
            curr_tres = getBalance('5uG1TFNxa8VoZRQggn1t55ny5EN3U88eB7m2yHWmZ2rk');
            curr_tres = float((curr_tres['value']))/(10**9)
            curr_lp = getBalance('pDhcgHW36JSG2TqKtVhAx9HauFZK3pcFkVE9kLRXCHb');
            curr_lp = float((curr_lp['value']))/(10**9)

            embed = discord.Embed(title='Daily Assets Snapshot',description=str(datetime.date.today()))        

            embed.add_field(name="Treasury Wallet Balance: ", value= f"{curr_tres} Sol\nhttps://solscan.io/account/5uG1TFNxa8VoZRQggn1t55ny5EN3U88eB7m2yHWmZ2rk", inline=False)
            embed.add_field(name="Royalties Wallet Balance:", value=f"{curr_royalties} Sol\nhttps://solscan.io/account/2ApaxgJpTgjaoANNTwxKvJXk9F4upRCmcXYLoNxBdMZJ", inline=False)
            embed.add_field(name="[REDACTED] Wallet Balance:", value=f"{curr_lp} Sol\nhttps://solscan.io/account/pDhcgHW36JSG2TqKtVhAx9HauFZK3pcFkVE9kLRXCHb", inline=False)
            embed.add_field(name="Total [REDACTED] Balance:", value='In Progress', inline=True)

            #print(curr_tres,curr_royalties,curr_lp)
            await text_channel.send(embed=embed)
        
        time.sleep(60)

client.run('MTA3MjI1NDI4MTMxNjU2OTIzOA.G5uKsU.LeJSZvDxlZsfobB3eIHfDoH8rm9vHiDeMUjhpk')
