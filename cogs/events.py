import discord
from discord.ext import commands
from database.db import get_guild_config
from config.config import COLORS, BOT_FOOTER
import logging

logger = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Bot está listo"""
        print(f"\n{'='*50}")
        print(f"✅ {self.bot.user.name} está conectado y listo")
        print(f"{'='*50}")
        print(f"📊 Servidores: {len(self.bot.guilds)}")
        print(f"👥 Usuarios: {len(self.bot.users)}")
        print(f"{'='*50}\n")
        
        # Establecer actividad
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Moderación | !help"
            )
        )
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Cuando un usuario entra al servidor"""
        try:
            guild = member.guild
            config = get_guild_config(guild.id)
            
            if not config or not config[4]:  # enabled
                return
            
            guild_id, channel_id, welcome_msg, dm_msg, enabled = config
            
            # Enviar DM
            if dm_msg:
                try:
                    dm_msg_formatted = dm_msg.replace('{username}', member.name).replace('{server_name}', guild.name)
                    
                    embed = discord.Embed(
                        title=f"👋 Bienvenido a {guild.name}",
                        description=dm_msg_formatted,
                        color=COLORS['PRIMARY']
                    )
                    embed.set_footer(text=BOT_FOOTER)
                    embed.timestamp = discord.utils.utcnow()
                    
                    await member.send(embed=embed)
                    print(f"📧 DM de bienvenida enviado a {member.name}")
                except:
                    print(f"⚠️ No se pudo enviar DM a {member.name}")
            
            # Enviar mensaje al canal
            if channel_id:
                try:
                    channel = guild.get_channel(channel_id)
                    if channel:
                        welcome_msg_formatted = welcome_msg.replace('{username}', member.name) if welcome_msg else f"👋 Bienvenido {member.name}"
                        
                        embed = discord.Embed(
                            title="👋 ¡Nuevo miembro!",
                            description=welcome_msg_formatted,
                            color=COLORS['PRIMARY']
                        )
                        embed.add_field(name="Usuario", value=member.mention, inline=True)
                        embed.add_field(name="Total de miembros", value=str(guild.member_count), inline=True)
                        embed.set_footer(text=BOT_FOOTER)
                        embed.timestamp = discord.utils.utcnow()
                        
                        await channel.send(embed=embed)
                        print(f"📢 Mensaje de bienvenida enviado a {member.name}")
                except Exception as e:
                    print(f"❌ Error al enviar mensaje de bienvenida: {e}")
        
        except Exception as e:
            print(f"❌ Error en on_member_join: {e}")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Cuando un usuario sale del servidor"""
        print(f"👋 {member.name} salió del servidor {member.guild.name}")

async def setup(bot):
    await bot.add_cog(Events(bot))
