import re

import discord
from discord.ext import commands

from database.db import get_mod_roles
from utils.embeds import error_embed, info_embed, success_embed


TICKET_CATEGORY_NAME = "Tickets"

TICKET_TYPES = {
    "support": {
        "label": "Soporte general",
        "description": "Ayuda con dudas o problemas generales",
        "channel_prefix": "soporte",
    },
    "report": {
        "label": "Reportar usuario",
        "description": "Reportes sobre miembros del servidor",
        "channel_prefix": "reporte",
    },
    "appeal": {
        "label": "Apelar sancion",
        "description": "Solicita revision de una sancion",
        "channel_prefix": "apelacion",
    },
    "apply": {
        "label": "Aplicar para un puesto",
        "description": "Postulaciones para staff o puestos disponibles",
        "channel_prefix": "aplicar",
    },
    "other": {
        "label": "Otro soporte",
        "description": "Cualquier otra solicitud de ayuda",
        "channel_prefix": "ticket",
    },
}


def safe_channel_name(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    return text.strip("-")[:40] or "usuario"


class TicketPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(TicketTypeSelect(bot))


class TicketTypeSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label=data["label"],
                description=data["description"],
                value=key,
            )
            for key, data in TICKET_TYPES.items()
        ]
        super().__init__(
            placeholder="Selecciona una seccion de soporte",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="tickets:select_type",
        )

    async def callback(self, interaction):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        member = interaction.user
        ticket_type = self.values[0]
        ticket_data = TICKET_TYPES[ticket_type]

        existing_channel = discord.utils.find(
            lambda channel: channel.topic
            and f"ticket_owner:{member.id}" in channel.topic
            and f"ticket_type:{ticket_type}" in channel.topic,
            guild.text_channels,
        )

        if existing_channel:
            embed = error_embed(
                "Ticket ya abierto",
                f"Ya tienes un ticket de esta seccion: {existing_channel.mention}",
            )
            return await interaction.followup.send(embed=embed, ephemeral=True)

        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
            ),
        }

        mod_roles = []
        for role_id in get_mod_roles(guild.id):
            role = guild.get_role(role_id)
            if role:
                mod_roles.append(role)
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_messages=True,
                )

        channel_name = (
            f"{ticket_data['channel_prefix']}-"
            f"{safe_channel_name(member.name)}"
        )

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"ticket_owner:{member.id}|ticket_type:{ticket_type}",
            reason=f"Ticket creado por {member} ({ticket_data['label']})",
        )

        embed = info_embed(
            ticket_data["label"],
            (
                f"{member.mention}, tu ticket fue creado.\n"
                "Describe tu solicitud con el mayor detalle posible y el equipo te atendera pronto."
            ),
            [
                {"name": "Seccion", "value": ticket_data["label"], "inline": True},
                {"name": "Usuario", "value": member.mention, "inline": True},
            ],
        )

        mentions = " ".join(role.mention for role in mod_roles)
        content = f"{member.mention} {mentions}".strip()

        await channel.send(
            content=content,
            embed=embed,
            view=TicketCloseView(self.bot),
            allowed_mentions=discord.AllowedMentions(users=True, roles=True),
        )

        confirm = success_embed(
            "Ticket creado",
            f"Tu ticket fue creado en {channel.mention}",
        )
        await interaction.followup.send(embed=confirm, ephemeral=True)


class TicketCloseView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Cerrar ticket",
        style=discord.ButtonStyle.danger,
        custom_id="tickets:close",
    )
    async def close_ticket(self, interaction, button):
        channel = interaction.channel
        member = interaction.user

        is_owner = channel.topic and f"ticket_owner:{member.id}" in channel.topic
        is_staff = member.guild_permissions.manage_channels

        if not is_staff:
            mod_role_ids = get_mod_roles(interaction.guild.id)
            is_staff = any(role.id in mod_role_ids for role in member.roles)

        if not is_owner and not is_staff:
            embed = error_embed(
                "No autorizado",
                "Solo quien abrio el ticket o el staff puede cerrarlo.",
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Cerrando ticket...", ephemeral=True)
        await channel.delete(reason=f"Ticket cerrado por {member}")


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ticketpanel")
    @commands.has_permissions(administrator=True)
    async def ticketpanel(self, ctx, channel: discord.TextChannel = None):
        """Envia el panel de tickets"""
        target_channel = channel or ctx.channel

        embed = info_embed(
            "Soporte",
            "Selecciona una seccion para abrir un ticket privado con el equipo.",
            [
                {
                    "name": "Secciones",
                    "value": "\n".join(
                        f"- {data['label']}: {data['description']}"
                        for data in TICKET_TYPES.values()
                    ),
                    "inline": False,
                }
            ],
        )

        await target_channel.send(embed=embed, view=TicketPanelView(self.bot))

        confirm = success_embed(
            "Panel enviado",
            f"El panel de tickets fue enviado a {target_channel.mention}",
        )
        await ctx.send(embed=confirm, ephemeral=bool(ctx.interaction))


async def setup(bot):
    bot.add_view(TicketPanelView(bot))
    bot.add_view(TicketCloseView(bot))
    await bot.add_cog(Tickets(bot))
