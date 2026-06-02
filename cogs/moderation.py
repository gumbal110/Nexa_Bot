import discord
from discord.ext import commands
from utils.embeds import success_embed, error_embed, warning_embed
from utils.validators import has_mod_role, validate_member
from database.db import add_warning, get_warnings, count_warnings
from config.config import MAX_WARN_COUNT

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sin razón especificada"):
        """Balea a un usuario"""
        
        # Validar
        if member.id == ctx.guild.owner_id:
            embed = error_embed("Error", "No puedo banear al propietario del servidor")
            return await ctx.send(embed=embed)
        
        if member.bot:
            embed = error_embed("Error", "No puedo banear a bots")
            return await ctx.send(embed=embed)
        
        try:
            await ctx.guild.ban(member, reason=reason)
            embed = success_embed(
                "Usuario baneado",
                f"{member.mention} ha sido baneado del servidor",
                [
                    {'name': 'Moderador', 'value': ctx.author.name, 'inline': True},
                    {'name': 'Razón', 'value': reason, 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo banear: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="Sin razón"):
        """Desbalea a un usuario"""
        try:
            await ctx.guild.unban(user, reason=reason)
            embed = success_embed(
                "Usuario desbaneado",
                f"{user.mention} ha sido desbaneado",
                [{'name': 'Razón', 'value': reason, 'inline': False}]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo desbanear: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sin razón especificada"):
        """Expulsa a un usuario"""
        
        # Validar
        valid, msg = validate_member(member, ctx.author, ctx.guild)
        if not valid:
            embed = error_embed("Error", msg)
            return await ctx.send(embed=embed)
        
        try:
            await member.kick(reason=reason)
            embed = success_embed(
                "Usuario expulsado",
                f"{member.mention} ha sido expulsado",
                [
                    {'name': 'Moderador', 'value': ctx.author.name, 'inline': True},
                    {'name': 'Razón', 'value': reason, 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo expulsar: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 60, *, reason="Sin razón"):
        """Silencia a un usuario (en minutos)"""
        
        valid, msg = validate_member(member, ctx.author, ctx.guild)
        if not valid:
            embed = error_embed("Error", msg)
            return await ctx.send(embed=embed)
        
        try:
            from datetime import timedelta
            await member.timeout(timedelta(minutes=duration), reason=reason)
            embed = success_embed(
                "Usuario silenciado",
                f"{member.mention} ha sido silenciado",
                [
                    {'name': 'Duración', 'value': f"{duration} minutos", 'inline': True},
                    {'name': 'Razón', 'value': reason, 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo silenciar: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Sin razón"):
        """Dessilencia a un usuario"""
        
        valid, msg = validate_member(member, ctx.author, ctx.guild)
        if not valid:
            embed = error_embed("Error", msg)
            return await ctx.send(embed=embed)
        
        try:
            await member.timeout(None, reason=reason)
            embed = success_embed(
                "Usuario dessilenciado",
                f"{member.mention} ha sido dessilenciado"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo dessilenciar: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='warn')
    async def warn(self, ctx, member: discord.Member, *, reason):
        """Advierte a un usuario"""
        
        if not await has_mod_role(ctx):
            embed = error_embed("Permisos insuficientes", "No tienes permisos para usar este comando")
            return await ctx.send(embed=embed)
        
        valid, msg = validate_member(member, ctx.author, ctx.guild)
        if not valid:
            embed = error_embed("Error", msg)
            return await ctx.send(embed=embed)
        
        # Guardar advertencia
        add_warning(ctx.guild.id, member.id, ctx.author.id, reason)
        count = count_warnings(ctx.guild.id, member.id)
        
        embed = success_embed(
            "Advertencia registrada",
            f"{member.mention} ha recibido una advertencia",
            [
                {'name': 'Razón', 'value': reason, 'inline': False},
                {'name': 'Total de advertencias', 'value': f"{count}/{MAX_WARN_COUNT}", 'inline': True}
            ]
        )
        
        if count >= MAX_WARN_COUNT:
            warn_embed = warning_embed(
                "Límite alcanzado",
                f"{member.mention} ha alcanzado el límite de advertencias ({MAX_WARN_COUNT})"
            )
            await ctx.send(embeds=[embed, warn_embed])
        else:
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='warnings')
    async def warnings(self, ctx, member: discord.Member):
        """Ve las advertencias de un usuario"""
        
        warnings = get_warnings(ctx.guild.id, member.id)
        
        if not warnings:
            embed = error_embed("Sin advertencias", f"{member.mention} no tiene advertencias")
            return await ctx.send(embed=embed)
        
        warning_list = "\n".join([
            f"**{i+1}.** {w[4]}\n📅 {w[5]}"
            for i, w in enumerate(warnings[:10])
        ])
        
        from utils.embeds import info_embed
        embed = info_embed(
            f"Advertencias de {member.name}",
            f"Total: **{len(warnings)}**",
            [{'name': 'Historial', 'value': warning_list, 'inline': False}]
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Limpia mensajes"""
        
        if amount > 100:
            amount = 100
        
        try:
            if ctx.interaction:
                await ctx.defer(ephemeral=True)

            deleted = await ctx.channel.purge(limit=amount)
            embed = success_embed(
                "Mensajes borrados",
                f"Se borraron **{len(deleted)}** mensajes"
            )
            await ctx.send(embed=embed, delete_after=5, ephemeral=bool(ctx.interaction))
        except Exception as e:
            embed = error_embed("Error", f"No se pudieron borrar: {str(e)}")
            await ctx.send(embed=embed, ephemeral=bool(ctx.interaction))
    
    @commands.hybrid_command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Establece modo lento"""
        
        if seconds > 21600:
            seconds = 21600
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            status = "desactivado" if seconds == 0 else f"{seconds} segundo(s)"
            embed = success_embed(
                "Modo lento actualizado",
                f"El modo lento es ahora de **{status}**"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Cierra un canal"""
        
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = success_embed(
                "Canal cerrado",
                f"{ctx.channel.mention} ha sido cerrado"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """Abre un canal"""
        
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
            embed = success_embed(
                "Canal abierto",
                f"{ctx.channel.mention} ha sido abierto"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='nick')
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname=None):
        """Cambia el apodo de alguien"""
        
        valid, msg = validate_member(member, ctx.author, ctx.guild)
        if not valid:
            embed = error_embed("Error", msg)
            return await ctx.send(embed=embed)
        
        try:
            old_nick = member.nick or member.name
            await member.edit(nick=nickname)
            embed = success_embed(
                "Apodo actualizado",
                f"El apodo de {member.mention} ha sido cambiado",
                [
                    {'name': 'Anterior', 'value': old_nick, 'inline': True},
                    {'name': 'Nuevo', 'value': nickname or "Removido", 'inline': True}
                ]
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
