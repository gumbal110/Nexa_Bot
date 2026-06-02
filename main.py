import asyncio
import logging
import os

import discord
from discord.ext import commands

from config.config import CLIENT_ID, GUILD_ID, TOKEN
from database.db import init_db

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Bot
bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    application_id=CLIENT_ID or None,
    help_command=None,
)
bot.slash_synced = False


@bot.event
async def on_ready():
    """Confirma que Discord acepto la sesion del bot."""
    print(f"\n[OK] Nexa conectado como {bot.user} (ID: {bot.user.id})\n")

    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            if not bot.slash_synced:
                bot.tree.copy_global_to(guild=guild)
                synced = await bot.tree.sync(guild=guild)
                print(f"[OK] Synced {len(synced)} commands")

                bot.tree.clear_commands(guild=None)
                await bot.tree.sync()
                bot.slash_synced = True
            else:
                synced = bot.tree.get_commands(guild=guild)
                print(f"[OK] Synced {len(synced)} commands")

            print(f"[OK] Slash commands sincronizados en el servidor {GUILD_ID}")
        else:
            await bot.tree.sync()
            print("[OK] Slash commands sincronizados globalmente")

        slash_names = (
            [cmd.name for cmd in bot.tree.walk_commands(guild=discord.Object(id=GUILD_ID))]
            if GUILD_ID
            else [cmd.name for cmd in bot.tree.walk_commands()]
        )
        print(f"[INFO] Slash commands cargados: {slash_names}")
        print(f"[INFO] Comandos totales en el bot: {len(slash_names)}")
    except Exception as e:
        print(f"[ERROR] Error sincronizando comandos slash: {e}")


async def load_cogs():
    """Carga todos los cogs."""
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"[OK] Cog cargado: {filename[:-3]}")
            except Exception as e:
                print(f"[ERROR] Error al cargar {filename}: {e}")


@bot.event
async def on_command_error(ctx, error):
    """Manejo de errores."""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Permisos insuficientes",
            description="No tienes permisos para usar este comando",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Argumentos faltantes",
            description=f"Falta el argumento: {error.param.name}",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)
    else:
        print(f"[ERROR] Error: {error}")


async def main():
    """Inicia el bot."""
    try:
        print("\n[INFO] Iniciando Nexa Bot...\n")

        if not TOKEN:
            raise RuntimeError(
                "No se encontro el token de Discord. "
                "Configura DISCORD_TOKEN en Railway o TOKEN en tu .env local."
            )

        # Inicializar base de datos
        print("[INFO] Inicializando SQLite...")
        init_db()

        # Cargar cogs
        print("[INFO] Cargando comandos...\n")
        await load_cogs()

        # Iniciar bot
        print("\n[INFO] Iniciando sesion en Discord...\n")
        await bot.start(TOKEN)

    except Exception as e:
        print(f"[ERROR] Error fatal: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
