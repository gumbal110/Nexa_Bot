from database.db import get_mod_roles
from discord.ext import commands
import discord

async def has_mod_role(ctx):
    """Valida si el usuario tiene permisos de moderación"""
    # Owner siempre tiene permisos
    if ctx.author.id == ctx.guild.owner_id:
        return True
    
    # Admin siempre tiene permisos
    if ctx.author.guild_permissions.administrator:
        return True
    
    # Verificar roles de moderación en BD
    mod_roles = get_mod_roles(ctx.guild.id)
    for role_id in mod_roles:
        if any(role.id == role_id for role in ctx.author.roles):
            return True
    
    return False

def validate_user(target_user, executor, guild):
    """Valida si se puede moderar a un usuario"""
    # No se puede moderar al owner
    if target_user.id == guild.owner_id:
        return False, "No puedo moderar al propietario del servidor"
    
    # No se puede moderar a bots
    if target_user.bot:
        return False, "No puedo moderar a bots"
    
    # No se puede moderar a si mismo
    if target_user.id == executor.id:
        return False, "No puedes moderar a ti mismo"
    
    return True, "Ok"

def validate_member(target_member, executor_member, guild):
    """Valida si se puede moderar a un miembro"""
    # No se puede moderar al owner
    if target_member.id == guild.owner_id:
        return False, "No puedo moderar al propietario del servidor"
    
    # No se puede moderar a bots
    if target_member.user.bot:
        return False, "No puedo moderar a bots"
    
    # No se puede moderar a si mismo
    if target_member.id == executor_member.id:
        return False, "No puedes moderar a ti mismo"
    
    # Validar jerarquía de roles
    if target_member.top_role.position >= executor_member.top_role.position:
        return False, "No puedes moderar a alguien con un rol igual o superior al tuyo"
    
    return True, "Ok"

class ModCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

async def setup(bot):
    await bot.add_cog(ModCheck(bot))
