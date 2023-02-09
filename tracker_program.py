import discord
from pysolana.api import *
import asyncio
import time
import datetime
import requests
import json
from bs4 import BeautifulSoup
import subprocess
import shlex

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

done = False

@client.event
async def on_ready():
    global done   
    text_channel = client.get_channel(1073175360902008852)
    #print(text_channel);
    while True:
        curr = time.localtime().tm_min
        if curr in (37,40,44,48,2,6,12,19,25,32,52,58) and not done:
          done = False
          try:
            is_working=False;
            prev_min = curr  
            temp = shlex.split('node get_positions.js')
            values =  subprocess.run(temp,capture_output=True);
            asset_list = values.stdout.decode('ascii').split(',')
            print(values.stderr.decode('ascii'))
            print(asset_list);

            #getting live price of tokens
            page_bonk = requests.get('https://coinmarketcap.com/currencies/bonk1/')
            soup_bonk = BeautifulSoup(page_bonk.text, "html.parser")
            bonk_price = (soup_bonk.body.div.div.div.contents[1].div.div.contents[1].div.contents[1].div.div.span.string)
            bonk_price = float(str('{:.10f}'.format(float(str(bonk_price[1:])))))

            #print(bonk_price)
            
            await asyncio.sleep(2);

            page_sol =  requests.get('https://coinmarketcap.com/currencies/solana/')
            soup_sol = BeautifulSoup(page_sol.text, "html.parser")
            sol_price = (soup_sol.body.div.div.div.contents[1].div.div.contents[1].div.contents[1].div.div.span.string)
            sol_price = float(str(sol_price[1:]))

            #print(sol_price)
            await asyncio.sleep(2);

            
            page_usdc =  requests.get('https://coinmarketcap.com/currencies/usd-coin/')
            soup_usdc = BeautifulSoup(page_usdc.text, "html.parser")
            usdc_price = (soup_usdc.body.div.div.div.contents[1].div.div.contents[1].div.contents[1].div.div.span.string)
            usdc_price = (float(str(usdc_price[1:])))

            #print(usdc_price)
            
            await asyncio.sleep(2);
            
            #current_time.tm_hour == 0 and current_time.tm_min == 0:
            headers={'Content-type': 'application/json'}
            
            #lp-spl-tokens
            lp_bonk =  {
              "jsonrpc": "2.0",
              "id": 1,
              "method": "getTokenAccountBalance",
              "params": [
                "FYj69uxq52dee8AyZbRyNgkGbhJdrPT6eqMhosJwaTXB"
              ]
            }
            response =  requests.post('https://api.mainnet-beta.solana.com',headers=headers,json=lp_bonk) 
            lp_bonk = response.json()['result']['value']['uiAmount']
            #print(lp_bonk)

            lp_usdc =  {
              "jsonrpc": "2.0",
              "id": 1,
              "method": "getTokenAccountBalance",
              "params": [
                "4TGNXq8vamcPFXvUh9HMWm86nr4HKR2dEBizNbHLCbgS"
              ]
            }
            response =  requests.post('https://api.mainnet-beta.solana.com',headers=headers,json=lp_usdc) 
            lp_usdc = response.json()['result']['value']['uiAmount']
            #print(lp_usdc)

            #lp-spl-tokens
            tres_bonk =  {
              "jsonrpc": "2.0",
              "id": 1,
              "method": "getTokenAccountBalance",
              "params": [
                "2AvMzonXASq2ximCf3aa8epjdpsTdrbU3QeZDsVf3W6s"
              ]
            }
            response =  requests.post('https://api.mainnet-beta.solana.com',headers=headers,json=tres_bonk) 
            tres_bonk = response.json()['result']['value']['uiAmount']
            #print(lp_bonk)

            tres_usdc =  {
              "jsonrpc": "2.0",
              "id": 1,
              "method": "getTokenAccountBalance",
              "params": [
                "QhZQwMSFcrBQVji9sZzN9VnaJUiLi4YHW2cP5NMn6Yz"
              ]
            }
            response =  requests.post('https://api.mainnet-beta.solana.com',headers=headers,json=tres_usdc) 
            tres_usdc = response.json()['result']['value']['uiAmount']
            print(tres_usdc)
            #print(all_spl_accounts,'\n')
            curr_royalties = getBalance('2ApaxgJpTgjaoANNTwxKvJXk9F4upRCmcXYLoNxBdMZJ');
            curr_royalties = float((curr_royalties['value']))/(10**9)
            curr_tres = getBalance('5uG1TFNxa8VoZRQggn1t55ny5EN3U88eB7m2yHWmZ2rk');
            curr_tres = float((curr_tres['value']))/(10**9)
            curr_lp = getBalance('pDhcgHW36JSG2TqKtVhAx9HauFZK3pcFkVE9kLRXCHb');
            curr_lp = float((curr_lp['value']))/(10**9)

            #calculations
            tres_sol_val = float('{:.3f}'.format(float(curr_tres)*float(sol_price)))
            tres_usdc_val = float('{:.3f}'.format(float(tres_usdc)*float(usdc_price)))
            tres_bonk_val = float('{:.3f}'.format(float(tres_bonk)*float(bonk_price)))
            total_tres_val = '{:.3f}'.format(tres_sol_val+tres_bonk_val+tres_usdc_val)
            #print(tres_sol_val,tres_usdc_val,tres_bonk_val,total_tres_val)

            lp_sol_val = float('{:.3f}'.format(float(curr_lp)*float(sol_price)))
            lp_usdc_val = float('{:.3f}'.format(float(lp_usdc)*float(usdc_price)))
            lp_bonk_val = float('{:.3f}'.format(float(lp_bonk)*float(bonk_price)))
            total_lp_val = '{:.3f}'.format(lp_sol_val+lp_bonk_val+lp_usdc_val)
            #print(lp_sol_val,lp_usdc_val,lp_bonk_val,total_lp_val)

            royalties_sol_val = float('{:.3f}'.format(float(curr_royalties)*float(sol_price)))


            positions_sol_val = float('{:.3f}'.format(float(asset_list[0])*float(sol_price)))
            positions_usdc_val = float('{:.3f}'.format(float(asset_list[1])*float(usdc_price)))
            positions_bonk_val = float('{:.3f}'.format(float(asset_list[2])*float(bonk_price)))
            tot_positions_val = positions_sol_val+positions_usdc_val+positions_bonk_val
            
            liq_value = float(total_lp_val)+float(total_tres_val)+float(royalties_sol_val)+float(tot_positions_val)

            embed = discord.Embed(title='Daily Assets Snapshot',description=str(datetime.date.today()))        

            embed.add_field(name="Treasury Wallet Balance:", value=f"--> {curr_tres} Sol (${tres_sol_val})\n--> {tres_usdc} USDC (${tres_usdc_val})\n--> {tres_bonk} Bonk (${tres_bonk_val})\n\n--> Assets Value: ${total_tres_val}\n\nhttps://solscan.io/account/5uG1TFNxa8VoZRQggn1t55ny5EN3U88eB7m2yHWmZ2rk#tokenAccounts", inline=False)
            embed.add_field(name="Royalties Wallet Balance:", value=f"--> {curr_royalties} Sol (${royalties_sol_val})\n--> 0.0 USDC ($0)\n--> 0.0 Bonk ($0)\n\n--> Assets Value: ${royalties_sol_val}\n\nhttps://solscan.io/account/2ApaxgJpTgjaoANNTwxKvJXk9F4upRCmcXYLoNxBdMZJ", inline=False)
            embed.add_field(name="LP Wallet Balance:", value=f"--> {curr_lp} Sol (${lp_sol_val})\n--> {lp_usdc} USDC (${lp_usdc_val})\n--> {lp_bonk} Bonk (${lp_bonk_val})\n\n--> Assets Value: ${total_lp_val}\n\nhttps://solscan.io/account/pDhcgHW36JSG2TqKtVhAx9HauFZK3pcFkVE9kLRXCHb", inline=False)
            embed.add_field(name="Open LP Positions:", value=f'--> {len(asset_list)} Open Positions\n--> {asset_list[0]} Sol (${positions_sol_val})\n--> {asset_list[1]} USDC (${positions_usdc_val})\n--> {asset_list[2]} Bonk (${positions_bonk_val})\n\n--> Assets Value: ${"{:.3f}".format(tot_positions_val)}', inline=False)
            embed.add_field(name="Project Stats:", value=f'• liquid-Asset Value: ${"{:.3f}".format(liq_value-tot_positions_val)} (LP Positions Exempt)\n• Cumulative-Asset Value: ${"{:.3f}".format(liq_value)}', inline=False);

            if not done:
              await text_channel.send(embed=embed)
              done = True
            await asyncio.sleep(60);
          except Exception as e:
            print (repr(e));
            await asyncio.sleep(10);
            continue
        elif curr not in (37,40,44,48,2,6,12,19,25,32,52,58):
           done = False
client.run('MTA3MjI1NDI4MTMxNjU2OTIzOA.G5uKsU.LeJSZvDxlZsfobB3eIHfDoH8rm9vHiDeMUjhpk')
