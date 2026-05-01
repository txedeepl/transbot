import os
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Carga de variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID_ES = int(os.getenv('ID_ESPANOL'))
ID_EN = int(os.getenv('ID_INGLES'))

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot traductor conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content:
        return

    try:
        # Si escribe el usuario de ESPAÑOL -> Traducir a INGLÉS
        if message.author.id == ID_ES:
            traduccion = GoogleTranslator(source='es', target='en').translate(message.content)
            await message.channel.send(f"🇬🇧 {traduccion}")

        # Si escribe el usuario de INGLÉS -> Traducir a ESPAÑOL
        elif message.author.id == ID_EN:
            traduccion = GoogleTranslator(source='en', target='es').translate(message.content)
            await message.channel.send(f"🇪🇸 {traduccion}")

    except Exception as e:
        print(f"Error: {e}")

    await bot.process_commands(message)

if TOKEN:
    bot.run(TOKEN)