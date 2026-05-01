import os
import discord
from discord.ext import commands
from googletrans import Translator
from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID_ES = int(os.getenv('ID_ESPANOL'))
ID_EN = int(os.getenv('ID_INGLES'))

# Configuración de Discord
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f'✅ Bot listo como {bot.user}')
    print(f'Configurado para IDs: {ID_ES} y {ID_EN}')

@bot.event
async def on_message(message):
    # Evitar bucles (que el bot se lea a sí mismo)
    if message.author == bot.user or not message.content:
        return

    try:
        # Traducción según el ID del autor
        if message.author.id == ID_ES:
            # Viene de español -> Traducir a inglés
            res = translator.translate(message.content, src='es', dest='en')
            await message.channel.send(f"🇬🇧 {res.text}")

        elif message.author.id == ID_EN:
            # Viene de inglés -> Traducir a español
            res = translator.translate(message.content, src='en', dest='es')
            await message.channel.send(f"🇪🇸 {res.text}")

    except Exception as e:
        print(f"Error en la traducción: {e}")

    await bot.process_commands(message)

# Ejecutar el bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: No se encontró el DISCORD_TOKEN en el archivo .env")