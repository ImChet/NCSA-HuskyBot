import discord
from discord.ext import commands


class ErrorHandling(commands.Cog):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # Error catch
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Cannot use CheckFailure error, or MissingPermissions and BotMissingPermissions will not trigger
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, you don\'t have permission to run this command.', delete_after=10)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'{ctx.author.mention}, I do not have the required permissions to run this command.', delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'{ctx.author.mention}, your inputted arguments are invalid.', delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, the command you chose requires arguments that are missing.', delete_after=10)
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(f'{ctx.author.mention}, your previous command has too many arguments.', delete_after=10)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{ctx.author.mention}, the command you typed does not exist.\nTry the /help command.', delete_after=10)
        elif isinstance(error, discord.HTTPException):
            await ctx.send(f'{ctx.author.mention}, an HTTP request operation failed. Try again shortly.', delete_after=10)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.author.mention}, this command is currently on cooldown. Try again shortly.', delete_after=10)


async def setup(HuskyBot):
    await HuskyBot.add_cog(ErrorHandling(HuskyBot))
