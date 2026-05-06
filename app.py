import requests as req
from bs4 import BeautifulSoup as bs
import discord as disc
from discord.ext import commands as cmd, tasks
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
#LAST U PDATE

##############################################
###########----LOGIC FUNCTIONS----############
##############################################
def getPrices():
    URL = 'https://www.leskamas.com/en-gb/sell-kamas.html'
    servers = []
    r = req.get(URL)
    soup = bs(r.text, "html.parser")


    for row in soup.find_all('tr'):
        row = str(row)
        if "Boune" in row:
            data = row.split('td')
            server = {
                'name'  : data[1][1:-2],
                'price' : data[9][1:-2],
            }
            servers.append(server)
    return servers

def build_embed(servers):
    embed = disc.Embed(
        title="💰 LES KAMAS WAS UPDATE THEIR PRICES !",
        color=0xFFD700
    )

    for server in servers:
        embed.add_field(
            name=server['name'],
            value=f"```{server['price']}```",
            inline=False
        )

    embed.set_footer(text="leskamas.com • auto-updated every 10 min")
    embed.timestamp = disc.utils.utcnow()
    return embed

def printf(message):
    now = str(datetime.now().date()) + " " + str(datetime.now().time())[:8]
    print(f"\033[1;30m{now}\033[34m INFO     \033[35m{message}\033[0m")
    
##############################################
##########----BOT CONFIGURATION----###########
##############################################
"""TOKEN OF BOT & AND PERMISSION WHICH'S NEED & BOT CREATION"""
## CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1488931321270108404
LAST_PRICES = []

intents = disc.Intents.default()
intents.message_content = True

bot = cmd.Bot(command_prefix="!", intents=intents)
##############################################
#############----BOT EVENTS----###############
##############################################

@bot.event
async def on_ready():
    now = str(datetime.now().date()) + " " + str(datetime.now().time())[:8]
    print(f"\033[1;30m{now}\033[34m INFO     \033[35mLogged in as \033[32m{bot.user}\033[0m")
    check_prices.start()
    
    
@bot.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return
    if not message.author.bot:
        await message.delete()
    c = message.content
    keywords = ['k','km','kamas','leskamas','boune']
    if c.lower() in keywords:
        last_prices = getPrices()
        embed = build_embed(last_prices)
        await message.channel.send(embed=embed)
        await message.channel.send(f"`====LesKamas BOT - Developed by Kabouwa====`")
        printf('Message Sent')
    await bot.process_commands(message)


@tasks.loop(minutes=15)
async def check_prices():
    global LAST_PRICES
    channel = bot.get_channel(CHANNEL_ID)
    try:
        data = getPrices()
    except Exception as e:
        print('\033[31mERROR : \033[0m', e)
        return
    
    if LAST_PRICES:
        if data[1] == LAST_PRICES[1]:
            printf('Prices checked, no updates !');
            return
        
    LAST_PRICES = data
    embed = build_embed(data)
    #############################
    user = await bot.fetch_user(592762749952458789)
    await user.send(embed=embed) 
    ############################
    await channel.send(embed=embed)
    await channel.send(f"`====LesKamas BOT - Developed by Kabouwa====`")
    printf('Prices updated - Message sent successfuly')

##############################################
###############----RUN BOT----################
##############################################
bot.run(TOKEN)