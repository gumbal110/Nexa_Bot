import os
from dotenv import load_dotenv

load_dotenv()

def _get_int_env(name, default=0):
    value = os.getenv(name)
    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{name} debe ser un numero entero valido")

# Discord
TOKEN = os.getenv('DISCORD_TOKEN') or os.getenv('TOKEN')
CLIENT_ID = _get_int_env('CLIENT_ID')
GUILD_ID = _get_int_env('GUILD_ID')

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
