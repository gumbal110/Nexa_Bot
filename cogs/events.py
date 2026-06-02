import logging

import discord
from discord.ext import commands

from config.config import BOT_FOOTER, COLORS
from database.db import get_guild_config

logger = logging.getLogger(__name__)


def format_welcome_message(message, member):
    """Aplica variables disponibles al mensaje de bienvenida."""
    if not message:
        return f"Bienvenido, {member.mention}."

    return (
        message.replace("{username}", member.mention)
        .replace("{server_name}", member.guild.name)
        .replace("{member_count}", str(member.guild.member_count or 0))
    )


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Bot esta listo."""
        print(f"\n{'=' * 50}")
        print(f"[OK] {self.bot.user.name} esta conectado y listo")
        print(f"{'=' * 50}")
        print(f"[INFO] Servidores: {len(self.bot.guilds)}")
        print(f"[INFO] Usuarios: {len(self.bot.users)}")
        print(f"{'=' * 50}\n")

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Moderacion | /help",
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Cuando un usuario entra al servidor."""
        try:
            guild = member.guild
            config = get_guild_config(guild.id)

            if not config or not config[4]:
                return

            guild_id, channel_id, welcome_msg, dm_msg, enabled = config

            if dm_msg:
                try:
                    dm_msg_formatted = format_welcome_message(dm_msg, member)

                    embed = discord.Embed(
                        title=f"Bienvenido a {guild.name}",
                        description=dm_msg_formatted,
                        color=COLORS["PRIMARY"],
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=BOT_FOOTER)
                    embed.timestamp = discord.utils.utcnow()

                    await member.send(embed=embed)
                    print(f"[OK] DM de bienvenida enviado a {member.name}")
                except Exception:
                    print(f"[WARN] No se pudo enviar DM a {member.name}")

            if channel_id:
                try:
                    channel = guild.get_channel(channel_id)
                    if channel:
                        welcome_msg_formatted = format_welcome_message(
                            welcome_msg,
                            member,
                        )

                        embed = discord.Embed(
                            title="Nuevo miembro",
                            description=welcome_msg_formatted,
                            color=COLORS["PRIMARY"],
                        )
                        embed.set_author(
                            name=member.display_name,
                            icon_url=member.display_avatar.url,
                        )
                        embed.set_thumbnail(url=member.display_avatar.url)
                        embed.add_field(
                            name="Miembro",
                            value=f"{guild.member_count or 0}",
                            inline=True,
                        )
                        embed.add_field(
                            name="Cuenta",
                            value=discord.utils.format_dt(member.created_at, style="R"),
                            inline=True,
                        )
                        embed.set_footer(text=f"{guild.name} | {BOT_FOOTER}")
                        embed.timestamp = discord.utils.utcnow()

                        await channel.send(embed=embed)
                        print(f"[OK] Mensaje de bienvenida enviado a {member.name}")
                except Exception as e:
                    print(f"[ERROR] Error al enviar mensaje de bienvenida: {e}")

        except Exception as e:
            print(f"[ERROR] Error en on_member_join: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Cuando un usuario sale del servidor."""
        print(f"[INFO] {member.name} salio del servidor {member.guild.name}")


async def setup(bot):
    await bot.add_cog(Events(bot))
