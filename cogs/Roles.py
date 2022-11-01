import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, has_permissions, parameter


class Roles(commands.Cog):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    @commands.hybrid_group(name='role', with_app_command=True, description='Does various role-based functions based on the choice of subcommand.')
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def _role_command_(self, ctx: commands.Context) -> None:
        print(f'I am the parent role command')

    @_role_command_.command(name='add', with_app_command=True, description='Adds the user to the specified role.')
    @app_commands.describe(member='The member to add the role to', role='The role to add the member to')
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def _role_add_command_(self, ctx: commands.Context, member: discord.Member = parameter(description='- The member to add the role to'), *, role: discord.Role = parameter(description='- The role to add the member to')) -> None:
        if role in member.roles:
            await ctx.send(f'That user already has that role.', delete_after=5)
        else:
            await member.add_roles(role)
            await ctx.send(f'Added {member} to {role}.', delete_after=5)

    @_role_command_.command(name='remove', with_app_command=True, description='Removes the user from the specified role.')
    @app_commands.describe(member='The member to remove the role from', role='The role to remove from the user')
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def _role_add_command_(self, ctx: commands.Context, member: discord.Member = parameter(description='- The member to remove the role from'), *, role: discord.Role = parameter(description='- The role to remove from the user')) -> None:
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'Removed {role} from {member}.', delete_after=5)
        else:
            await ctx.send(f'{member} does not have the role: {role}.', delete_after=5)


async def setup(HuskyBot):
    await HuskyBot.add_cog(Roles(HuskyBot))
