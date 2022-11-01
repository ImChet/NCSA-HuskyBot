import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions, parameter, Range


class Administration(commands.Cog, name='Administration', description='Administration'):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # Kick command
    @commands.hybrid_command(name='kick', with_app_command=True, description='Kicks users with optional specified reason.')
    @app_commands.describe(member='The member you wish to kick',
                           reason='The optional reason you kicked the user previously mentioned member')
    @app_commands.default_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def _kick_(self, ctx: commands.Context, member: discord.Member = parameter(description='- The member you wish to kick'), *, reason: str = parameter(default=None, description='- The optional reason you kicked the user specified by <member>')) -> None:
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.', delete_after=5)

    # Ban command
    @commands.hybrid_command(name='ban', with_app_command=True, description='Bans users with optional specified reason.')
    @app_commands.describe(member='The member you wish to ban',
                           reason='The optional reason you banned the user previously mentioned member')
    @app_commands.default_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def _ban_(self, ctx: commands.Context, member: discord.Member = parameter(description='- The member you wish you ban'), *, reason: str = parameter(default=None, description='- The optional reason you banned the user specified by <member>')) -> None:
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.', delete_after=5)

    # Delete previous text command
    @commands.hybrid_command(name='clear', with_app_command=True, description='Clears a specified backlog of messages in channel where command was invoked.')
    @app_commands.describe(amount='Number of previous messages to clear')
    @app_commands.default_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def _delete_(self, ctx: commands.Context, amount: Range[int, 1, 100] = parameter(default=1, description='- Number of previous messages to clear')) -> None:
        await ctx.typing()
        deleted = await ctx.channel.purge(limit=amount, before=ctx.message.created_at)
        await ctx.send(f'Deleted {len(deleted):,} messages.', delete_after=5)


async def setup(HuskyBot):
    await HuskyBot.add_cog(Administration(HuskyBot))
