import discord
from discord.ext import commands
from utils.embeds import success_embed, error_embed, info_embed
from database.db import set_welcome_channel, set_welcome_message, set_dm_message, get_guild_config

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        """Configura el canal de bienvenida"""
        
        set_welcome_channel(ctx.guild.id, channel.id)
        
        embed = success_embed(
            "Canal de bienvenida configurado",
            f"Los mensajes de bienvenida se enviarán a {channel.mention}",
            [{'name': 'Estado', 'value': 'Bienvenida automática activada ✅', 'inline': True}]
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='welcomemessage')
    @commands.has_permissions(administrator=True)
    async def welcomemessage(self, ctx, *, message):
        """Configura el mensaje de bienvenida"""
        
        set_welcome_message(ctx.guild.id, message)
        
        embed = success_embed(
            "Mensaje de bienvenida actualizado",
            f"El nuevo mensaje es:\n\n{message}",
            [{'name': 'Variables disponibles', 'value': '{username}, {member_count}', 'inline': False}]
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='setdmmessage')
    @commands.has_permissions(administrator=True)
    async def setdmmessage(self, ctx, *, message):
        """Configura el mensaje privado de bienvenida"""
        
        set_dm_message(ctx.guild.id, message)
        
        embed = success_embed(
            "Mensaje privado actualizado",
            f"El nuevo mensaje es:\n\n{message}",
            [{'name': 'Variables disponibles', 'value': '{username}, {server_name}', 'inline': False}]
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='welcomeinfo')
    async def welcomeinfo(self, ctx):
        """Ve la configuración de bienvenida"""
        
        config = get_guild_config(ctx.guild.id)
        
        if not config:
            embed = info_embed(
                "Configuración de bienvenida",
                "No hay configuración de bienvenida establecida"
            )
            return await ctx.send(embed=embed)
        
        guild_id, channel_id, welcome_msg, dm_msg, enabled = config
        
        channel_name = f"<#{channel_id}>" if channel_id else "No configurado"
        status = "✅ Activado" if enabled else "❌ Desactivado"
        
        embed = info_embed(
            "Configuración de Bienvenida",
            status,
            [
                {'name': 'Canal de bienvenida', 'value': channel_name, 'inline': False},
                {'name': 'Mensaje de canal', 'value': welcome_msg or 'Por defecto', 'inline': False},
                {'name': 'Mensaje privado', 'value': dm_msg or 'Por defecto', 'inline': False}
            ]
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Config(bot))
