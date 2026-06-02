import os
from dotenv import load_dotenv

load_dotenv()

# Discord
TOKEN = os.getenv('TOKEN')
CLIENT_ID = int(os.getenv('CLIENT_ID', 0))
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# Colors
COLORS = {
    'PRIMARY': 0x00BFFF,      # Azul Neon
    'SECONDARY': 0x8A2BE2,    # Morado
    'SUCCESS': 0x00FF00,      # Verde
    'ERROR': 0xFF0000,        # Rojo
    'WARNING': 0xFFA500,      # Naranja
}

# Bot Info
BOT_NAME = os.getenv('BOT_NAME', 'Nexa')
BOT_OWNER = os.getenv('BOT_OWNER', 'AxioLabs')
BOT_FOOTER = os.getenv('BOT_FOOTER', 'Nexa • Powered by AxioLabs')

# Database
DB_PATH = 'data/bot.db'

# Validation
MAX_WARN_COUNT = 3
