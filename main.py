import os
import discord
import re
from discord.ext import commands
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID_ES = int(os.getenv('ID_ESPANOL'))
ID_EN = int(os.getenv('ID_INGLES'))

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

def es_solo_emoji(texto):
    # Esta expresión regular busca mensajes que NO contienen letras ni números
    # Si el mensaje solo tiene emojis, espacios o símbolos, devolverá True
    if not re.search(r'[a-zA-Z0-9]', texto):
        return True
    return False

@bot.event
async def on_ready():
    print(f'✅ Bot listo. Filtro de emojis activado.')

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content:
        return

    # Si el mensaje son solo emojis o iconos, no hacemos nada
    if es_solo_emoji(message.content):
        return

    try:
        if message.author.id == ID_ES:
            traduccion = GoogleTranslator(source='es', target='en').translate(message.content)
            # Solo enviamos si la traducción no es vacía o idéntica
            if traduccion and traduccion.strip().lower() != message.content.strip().lower():
                await message.channel.send(f"🇬🇧 {traduccion}")

        elif message.author.id == ID_EN:
            traduccion = GoogleTranslator(source='en', target='es').translate(message.content)
            if traduccion and traduccion.strip().lower() != message.content.strip().lower():
                await message.channel.send(f"🇪🇸 {traduccion}")

    except Exception as e:
        print(f"Error: {e}")

    await bot.process_commands(message)

if TOKEN:
    bot.run(TOKEN)