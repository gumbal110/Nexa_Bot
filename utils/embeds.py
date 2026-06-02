import discord
from config.config import COLORS, BOT_FOOTER

def create_embed(title, description, color='PRIMARY', fields=None):
    """Crea un embed básico"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS[color]
    )
    embed.set_footer(text=BOT_FOOTER)
    embed.timestamp = discord.utils.utcnow()
    
    if fields:
        for field in fields:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field.get('inline', False)
            )
    
    return embed

def success_embed(title, description, fields=None):
    """Embed de éxito"""
    return create_embed(f"✅ {title}", description, 'SUCCESS', fields)

def error_embed(title, description, fields=None):
    """Embed de error"""
    return create_embed(f"❌ {title}", description, 'ERROR', fields)

def warning_embed(title, description, fields=None):
    """Embed de advertencia"""
    return create_embed(f"⚠️ {title}", description, 'WARNING', fields)

def info_embed(title, description, fields=None):
    """Embed de información"""
    return create_embed(f"ℹ️ {title}", description, 'PRIMARY', fields)

def announce_embed(title, description, fields=None):
    """Embed de anuncio"""
    return create_embed(f"📢 {title}", description, 'PRIMARY', fields)
