import discord
from discord.ext import commands
from utils.embeds import success_embed, error_embed, info_embed
from database.db import add_mod_role, remove_mod_role, get_mod_roles

class Permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='setmodrole')
    @commands.has_permissions(administrator=True)
    async def setmodrole(self, ctx, role: discord.Role):
        """Agrega un rol con permisos de moderación"""
        
        add_mod_role(ctx.guild.id, role.id)
        
        embed = success_embed(
            "Rol agregado",
            f"El rol {role.mention} ahora tiene permisos de moderación",
            [{'name': 'Estado', 'value': 'Rol autorizado ✅', 'inline': True}]
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='removemodrole')
    @commands.has_permissions(administrator=True)
    async def removemodrole(self, ctx, role: discord.Role):
        """Quita permisos de moderación de un rol"""
        
        remove_mod_role(ctx.guild.id, role.id)
        
        embed = success_embed(
            "Rol removido",
            f"El rol {role.mention} ya no tiene permisos de moderación"
        )
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='modroles')
    async def modroles(self, ctx):
        """Lista los roles con permisos de moderación"""
        
        role_ids = get_mod_roles(ctx.guild.id)
        
        if not role_ids:
            embed = info_embed(
                "Sin roles de moderación",
                "No hay roles con permisos de moderación configurados"
            )
            return await ctx.send(embed=embed)
        
        roles_list = []
        for role_id in role_ids:
            role = ctx.guild.get_role(role_id)
            if role:
                roles_list.append(f"• {role.mention}")
            else:
                roles_list.append(f"• Rol eliminado ({role_id})")
        
        embed = info_embed(
            "Roles de Moderación",
            f"Total: **{len(role_ids)}**",
            [{'name': 'Roles autorizados', 'value': '\n'.join(roles_list), 'inline': False}]
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Permissions(bot))
