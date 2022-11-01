from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter

from functions import to_lower, to_upper


class Miscellaneous(commands.Cog, name='Miscellaneous Commands', description='Miscellaneous Commands'):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # To lowercase
    @commands.hybrid_command(name='low', with_app_command=True, description='Changes the input provided to lowercase.')
    @app_commands.describe(user_input='Any input given by the user to be changed to lowercase')
    async def _low_(self, ctx: commands.Context, *, user_input: to_lower = parameter(description='- Any input given by the user to be changed to lowercase')) -> None:
        await ctx.send(user_input)

    # To uppercase
    @commands.hybrid_command(name='up', with_app_command=True, description='Changes the input provided to uppercase.')
    @app_commands.describe(user_input='Any input given by the user to be changed to uppercase')
    async def _up_(self, ctx: commands.Context, *, user_input: to_upper = parameter(description='- Any input given by the user to be changed to uppercase')) -> None:
        await ctx.send(user_input)


async def setup(HuskyBot):
    await HuskyBot.add_cog(Miscellaneous(HuskyBot))
