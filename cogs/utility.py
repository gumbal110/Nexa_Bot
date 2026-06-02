import discord
from discord.ext import commands
from utils.embeds import success_embed, error_embed, announce_embed
from utils.validators import has_mod_role
from config.config import COLORS

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='help')
    async def help(self, ctx):
        """Muestra ayuda de comandos"""
        embed = discord.Embed(
            title="Ayuda - Comandos disponibles",
            description="Usa `/comando` para ejecutar uno de estos comandos.",
            color=COLORS['PRIMARY']
        )
        embed.add_field(name="/ban", value="Banea un usuario", inline=False)
        embed.add_field(name="/unban", value="Desbanea un usuario", inline=False)
        embed.add_field(name="/kick", value="Expulsa un usuario", inline=False)
        embed.add_field(name="/mute", value="Silencia un usuario", inline=False)
        embed.add_field(name="/warn", value="Advierte a un usuario", inline=False)
        embed.add_field(name="/setwelcome", value="Configura canal de bienvenida", inline=False)
        embed.add_field(name="/announce", value="Envía un anuncio a un canal", inline=False)
        embed.set_footer(text="Nexa • Powered by AxioLabs")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='announce')
    async def announce(self, ctx, channel: discord.TextChannel, *, message):
        """Envía un anuncio"""
        
        if not await has_mod_role(ctx):
            embed = error_embed("Permisos insuficientes", "No tienes permisos para usar este comando")
            return await ctx.send(embed=embed)
        
        try:
            parts = message.split('|')
            title = parts[0].strip() if len(parts) > 0 else "Anuncio"
            description = parts[1].strip() if len(parts) > 1 else message
            
            embed = announce_embed(title, description, [
                {'name': 'Enviado por', 'value': ctx.author.name, 'inline': True}
            ])
            
            await channel.send(embed=embed)
            
            confirm = success_embed(
                "Anuncio enviado",
                f"El anuncio ha sido enviado a {channel.mention}"
            )
            await ctx.send(embed=confirm)
        except Exception as e:
            embed = error_embed("Error", f"No se pudo enviar el anuncio: {str(e)}")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='embed')
    async def embed(self, ctx, channel: discord.TextChannel, *, message):
        """Crea un embed personalizado"""
        
        if not await has_mod_role(ctx):
            embed = error_embed("Permisos insuficientes", "No tienes permisos para usar este comando")
            return await ctx.send(embed=embed)
        
        try:
            parts = message.split('|')
            title = parts[0].strip() if len(parts) > 0 else "Embed"
            description = parts[1].strip() if len(parts) > 1 else message
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=COLORS['PRIMARY']
            )
            embed.set_footer(text="Nexa • Powered by AxioLabs")
            embed.timestamp = discord.utils.utcnow()
            
            await channel.send(embed=embed)
            
            confirm = success_embed(
                "Embed enviado",
                f"El embed ha sido enviado a {channel.mention}"
            )
            await ctx.send(embed=confirm)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='say')
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        """Envía un mensaje"""
        
        if not await has_mod_role(ctx):
            embed = error_embed("Permisos insuficientes", "No tienes permisos para usar este comando")
            return await ctx.send(embed=embed)
        
        try:
            await channel.send(message)
            confirm = success_embed(
                "Mensaje enviado",
                f"Tu mensaje ha sido enviado a {channel.mention}"
            )
            await ctx.send(embed=confirm, delete_after=5)
        except Exception as e:
            embed = error_embed("Error", str(e))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
