import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter
from functions import removeDirectory


class FileOperations(commands.Cog, name='File Commands', description='File Commands'):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # Makes and uploads files bases on user's decision
    @commands.hybrid_group(name='delimited', with_app_command=True, description='Creates and uploads a file based on the user\'s descision.\n/delimited <desired_file_type> <user_input>')
    async def _create_file_(self, ctx: commands.Context) -> None:
        print('I am the parent delimited command')

    @_create_file_.command(name='csv', with_app_command=True, description='Creates a csv delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on', user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/HuskyBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = ', '.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    @_create_file_.command(name='tab', with_app_command=True, description='Creates a tab delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on', user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/HuskyBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = '\t'.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)

    @_create_file_.command(name='line', with_app_command=True, description='Creates a line delimited file based on user input.')
    @app_commands.describe(where_to_split='Optional character to split your input on', user_input='Any input given by the user to be added to the file')
    async def _create_file_csv_(self, ctx: commands.Context, *, where_to_split: str = parameter(default=' ', description='- Optional character to split your input on'), user_input: str = parameter(description='- Any input given by the user to be added to the file')) -> None:

        # Make unique temporary directory to use for each user
        parent_dir = 'WorkingFiles/FilesToCreate/'
        user_dir = str(ctx.author.id)
        temp_directory = os.path.join(parent_dir, user_dir)
        os.mkdir(temp_directory)

        working_file = f'{temp_directory}/HuskyBot.csv'
        space_seperated = user_input.split(where_to_split)
        working_text = '\n'.join(space_seperated)
        f = open(working_file, "w")
        f.write(working_text)
        f.close()
        await ctx.send(file=discord.File(working_file))
        removeDirectory(temp_directory)


async def setup(HuskyBot):
    await HuskyBot.add_cog(FileOperations(HuskyBot))
