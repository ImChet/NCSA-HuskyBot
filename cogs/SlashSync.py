from typing import Optional, Literal

import discord
from discord.ext import commands
from discord.ext.commands import Greedy


# You can only run this as the HuskyBot-NCSA discord account (The owner of the Bot account)
class SlashSync(commands.Cog):
    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # Usage:
    # /sync           -> global sync
    # /sync !         -> sync current guild
    # /sync *         -> copies all global app commands to current guild and syncs
    # /sync ^         -> clears all commands from the current guild target and syncs (removes guild commands)
    # /sync id_1 id_2 -> syncs guilds with id 1 and 2
    @commands.command(name='sync', hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context,
                   guilds: Greedy[discord.Object],
                   spec: Optional[Literal["!", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "!":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.reply(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.reply(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(HuskyBot):
    await HuskyBot.add_cog(SlashSync(HuskyBot))
