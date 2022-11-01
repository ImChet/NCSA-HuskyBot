import json
import os
from datetime import datetime

import discord
from discord import utils, app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions


class TicketLauncher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60,
                                                               commands.BucketType.member)  # 60 second, per-member cooldown

    @discord.ui.button(label='Create A Ticket', style=discord.ButtonStyle.gray, custom_id='ticket_button')
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        # Cooldown logic
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.response.send_message(
                f'Slow down! You are currently on cooldown to make another ticket. Try again in {round(retry, 1)} seconds.',
                ephemeral=True)
        # No cooldown, continue
        else:
            ticket_str = f'ticket-for-{interaction.user.name.lower().replace(" ", "-")}-{interaction.user.discriminator}'
            ticket = utils.get(interaction.guild.text_channels, name=ticket_str)
            if ticket is not None:
                await interaction.response.send_message(
                    f'No need to create a new ticket! You already have a one open: {ticket.mention}', ephemeral=True)
            else:
                messageid = interaction.message.id
                with open('WorkingFiles/Databases/TicketingJSON.json', "r") as database:
                    data = json.load(database)

                data_scan = data['Ticketing_IDs']
                for item in data_scan:
                    value = item.get('messageid')
                    if value == messageid:
                        roleid = item.get('roleid')

                if type(roleid) is not discord.Role:
                    roleid = interaction.guild.get_role(roleid)

                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, read_message_history=True),
                    interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                    roleid: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, read_message_history=True)
                }

                channel = await interaction.guild.create_text_channel(name=ticket_str, overwrites=overwrites, reason=f'Ticket opened by {interaction.user}')

                # Send in ticket
                await channel.send(f'{interaction.user.mention}, here is the ticket you requested.\n'
                                   f'Some things for you to know:\n\n'
                                   f'Ticket Support: {roleid.mention}\n'
                                   f'- Use the `/add` command to to add anyone else that you might need to see this ticket.\n'
                                   f'- When you wish to close this ticket click the button below or use the `/close` command.',
                                   view=TicketInternals())

                # Send a modal to get more information from the user
                await interaction.response.send_modal(TicketInformationModal(ticket_str))


class Confirmation(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.red, custom_id='confirm')
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.channel.delete()
        except:
            await interaction.response.send_message(f'Channel deletion failed! Do I have the `manage_channels` permission?', ephemeral=True)


class TicketInternals(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label='Close Your Ticket', style=discord.ButtonStyle.red, custom_id='close_ticket')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title='Are you sure that you would like to close this ticket?', color=discord.Color.red())
        await interaction.response.send_message(embed=embed, view=Confirmation(), ephemeral=True)

    @discord.ui.button(label='Generate Transcript', style=discord.ButtonStyle.blurple, custom_id='create_transcript')
    async def generate_transcript(self, interaction: discord.Interaction, button: discord.ui.Button):
        transcript_file = f'WorkingFiles/FilesToCreate/{interaction.channel.id}.log'
        counter = 0
        await interaction.response.defer(ephemeral=True)
        if os.path.exists(transcript_file):
            return await interaction.followup.send(f'A transcript is already being generated. Please wait...', ephemeral=True)
        else:
            with open(transcript_file, "a") as transcript:
                generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                transcript.write(f'Transcript of: {interaction.channel.name}:\n\n\n'
                                 f'Generated at {generated} by {interaction.user.name}#{interaction.user.discriminator}\n'
                                 f'Date Formatting: MM/DD/YY at HH:MM:SS\n'
                                 f'Time Zone: UTC\n\n'
                                 f'Transcript:\n\n')

                # Look for the oldest messages first
                async for message in interaction.channel.history(limit=None, oldest_first=True):
                    counter += 1
                    # Ignore the first two messages in a ticket, just information sent by HuskyBot
                    if counter not in [1, 2]:
                        if message.type != discord.MessageType.chat_input_command:
                            created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                            if message.edited_at:
                                if message.attachments:
                                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                                    transcript.write(
                                        f'(Message originally sent on {created})\n'
                                        f'{message.author} said:\n'
                                        f'[File(s) were attached to this message]\n'
                                        f'[Message was edited on {edited}]\n'
                                        f'{message.clean_content}\n\n')
                                else:
                                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                                    transcript.write(
                                        f'(Message originally sent on {created})\n'
                                        f'{message.author} said:\n'
                                        f'[Message was edited on {edited}]\n'
                                        f'{message.clean_content}\n\n')
                            else:
                                if message.attachments:
                                    transcript.write(
                                        f'(Message originally sent on {created})\n'
                                        f'{message.author} said:\n'
                                        f'[File(s) were attached to this message]\n'
                                        f'{message.clean_content}\n\n')

                                else:
                                    transcript.write(f'(Message originally sent on {created})\n'
                                                     f'{message.author} said:\n'
                                                     f'{message.clean_content}\n\n')
            await interaction.followup.send(file=discord.File(transcript_file), ephemeral=True)
            os.remove(transcript_file)


class TicketInformationModal(discord.ui.Modal, title='Additional Information'):
    def __init__(self, ticket_name_str: str) -> None:
        super().__init__(timeout=None)
        self.ticket_name_str = ticket_name_str

    type_of_problem = discord.ui.TextInput(
        label='Type of Problem',
        style=discord.TextStyle.short,
        placeholder='Describe the type of problem occuring...',
        required=True
    )
    additional_information = discord.ui.TextInput(
        label='What additional information should we know?',
        style=discord.TextStyle.paragraph,
        placeholder='Type the information here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        ticket = utils.get(interaction.guild.text_channels, name=self.ticket_name_str)
        if ticket is not None:
            await interaction.response.send_message(
                f'Thank you for adding additional information to the ticket, {interaction.user.mention}.\n\nThe new ticket: {ticket.mention}',
                ephemeral=True)
            await ticket.send(f'Additional Ticket Information:\n'
                              f'**Type Of Problem:**\n'
                              f'{str(self.type_of_problem.value)}\n'
                              f'**Additional Information:**\n'
                              f'{str(self.additional_information.value)}')


class TicketingSystem(commands.Cog, name='Ticketing System', description='Ticketing System'):

    def __init__(self, HuskyBot):
        self.HuskyBot = HuskyBot

    # Need to have manage_channels permissions to run and see this command
    @app_commands.default_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    @app_commands.command(name='ticket', description='Creates a ticket for a specified user')
    @app_commands.describe(member='The member that you would like to open a ticket for',
                           ticket_support_role='The role that you would like to assign as the dedicated Ticket Support to this ticket')
    async def ticket(self, interaction: discord.Interaction, member: discord.Member, ticket_support_role: discord.Role):
        ticket_string = f'ticket-for-{member.name.lower().replace(" ", "-")}-{member.discriminator}'
        ticket = utils.get(interaction.guild.text_channels, name=ticket_string)
        if ticket is not None:
            await interaction.response.send_message(
                f'No need to create a new ticket! There is already one open: {ticket.mention}', ephemeral=True)
        else:
            roleid = ticket_support_role.id

            if type(roleid) is not discord.Role:
                roleid = interaction.guild.get_role(roleid)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                                    embed_links=True, read_message_history=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                                              embed_links=True, read_message_history=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                  read_message_history=True),
                roleid: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                                    embed_links=True, read_message_history=True)
            }

            channel = await interaction.guild.create_text_channel(name=ticket_string, overwrites=overwrites,
                                                                  reason=f'Ticket opened by {interaction.user}')

            # Send in ticket
            await channel.send(f'{interaction.user.mention}, here is the ticket you requested for {member.mention}.\n'
                               f'Some things for you to know:\n\n'
                               f'Ticket Support: {roleid.mention}\n'
                               f'- Use the `/add` command to to add anyone else that you might need to see this ticket.\n'
                               f'- When you wish to close this ticket click the button below or use the `/close` command.',
                               view=TicketInternals())

            # Send a modal to get more information from the user
            await interaction.response.send_modal(TicketInformationModal(ticket_string))

    # Need to have manage_channels permissions to run and see this command
    @app_commands.default_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    @app_commands.command(name='launch-ticketing', description='Launches the ticketing system')
    @app_commands.describe(ticket_support_role='The role that you would like to assign as the dedicated Ticket Support')
    async def ticketing(self, interaction: discord.Interaction, ticket_support_role: discord.Role):

        embed = discord.Embed(title='If you need any support, click the button below and create a ticket!',
                              color=discord.Color.yellow())
        ticket_launcher = await interaction.channel.send(embed=embed, view=TicketLauncher())
        await interaction.response.send_message(
            f'I launched the Ticketing System. I am now listening for help requests...', ephemeral=True)

        # use a .json to
        # {"messageid": ticket_launcher.id, "roleid": role.id}
        add_to_json = {"messageid": ticket_launcher.id,
                       "roleid": ticket_support_role.id}

        with open('WorkingFiles/Databases/TicketingJSON.json', "r") as database:
            data = json.load(database)

        with open('WorkingFiles/Databases/TicketingJSON.json', "w") as database:
            data['Ticketing_IDs'].append(add_to_json)
            database.seek(0)
            json.dump(data, database, indent=4)

    @app_commands.command(name='close', description='Closes the current ticket')
    async def close(self, interaction: discord.Interaction):
        if 'ticket-for-' in interaction.channel.name:
            embed = discord.Embed(title='Are you sure that you would like to close this ticket?',
                                  color=discord.Color.red())
            await interaction.response.send_message(embed=embed, view=Confirmation(), ephemeral=True)
        else:
            await interaction.response.send_message(
                f'This channel is not a ticket. I am only allowed to close tickets.\n*I would get yelled at if I was able to delete any channel that you wanted me to...*',
                ephemeral=True)

    @app_commands.command(name='transcript', description='Provides the transcript for the current ticket')
    async def transcript(self, interaction: discord.Interaction):
        if 'ticket-for-' in interaction.channel.name:
            transcript_file = f'WorkingFiles/FilesToCreate/{interaction.channel.id}.log'
            counter = 0
            await interaction.response.defer(ephemeral=True)
            if os.path.exists(transcript_file):
                return await interaction.followup.send(f'A transcript is already being generated. Please wait...', ephemeral=True)
            else:
                with open(transcript_file, "a") as transcript:
                    generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                    transcript.write(f'Transcript of: {interaction.channel.name}:\n\n\n'
                                     f'Generated at {generated} by {interaction.user.name}#{interaction.user.discriminator}\n'
                                     f'Date Formatting: MM/DD/YY at HH:MM:SS\n'
                                     f'Time Zone: UTC\n\n'
                                     f'Transcript:\n\n')

                    # Look for the oldest messages first
                    async for message in interaction.channel.history(limit=None, oldest_first=True):
                        counter += 1
                        # Ignore the first two messages in a ticket, just information sent by HuskyBot
                        if counter not in [1, 2]:
                            if message.type != discord.MessageType.chat_input_command:
                                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                                if message.edited_at:
                                    if message.attachments:
                                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                                        transcript.write(
                                            f'(Message originally sent on {created})\n'
                                            f'{message.author} said:\n'
                                            f'[File(s) were attached to this message]\n'
                                            f'[Message was edited on {edited}]\n'
                                            f'{message.clean_content}\n\n')
                                    else:
                                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                                        transcript.write(
                                            f'(Message originally sent on {created})\n'
                                            f'{message.author} said:\n'
                                            f'[Message was edited on {edited}]\n'
                                            f'{message.clean_content}\n\n')
                                else:
                                    if message.attachments:
                                        transcript.write(
                                            f'(Message originally sent on {created})\n'
                                            f'{message.author} said:\n'
                                            f'[File(s) were attached to this message]\n'
                                            f'{message.clean_content}\n\n')

                                    else:
                                        transcript.write(f'(Message originally sent on {created})\n'
                                                         f'{message.author} said:\n'
                                                         f'{message.clean_content}\n\n')
                await interaction.followup.send(file=discord.File(transcript_file))
                os.remove(transcript_file)
        else:
            await interaction.response.send_message(f'This channel is not a ticket. I am only allowed to generate transcripts for tickets.', ephemeral=True)

    @app_commands.command(name='add', description='The member that you would like to add to this ticket.')
    @app_commands.describe(member='Which member you would like to add to the current ticket.')
    async def add(self, interaction: discord.Interaction, member: discord.Member):
        if 'ticket-for-' in interaction.channel.name:
            await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, attach_files=True,
                                                      embed_links=True)
            await interaction.response.send_message(f'{member.mention} has been added to this ticket.', ephemeral=True)
        else:
            await interaction.response.send_message(
                f'This channel is not a ticket. I am only allowed to add users to tickets.', ephemeral=True)

    # Need to have manage_channels permissions to run and see this command
    @app_commands.default_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    @app_commands.command(name='remove', description='The member that you would like to remove from this ticket.')
    @app_commands.describe(member='Which member you would like to remove from the current ticket.')
    async def remove(self, interaction: discord.Interaction, member: discord.Member):
        if 'ticket-for-' in interaction.channel.name:
            await interaction.channel.set_permissions(member, overwrite=None)
            await interaction.response.send_message(f'{member.mention} has been removed from this ticket.',
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(
                f'This channel is not a ticket. I am only able to remove members from a ticket.')


async def setup(HuskyBot):
    await HuskyBot.add_cog(TicketingSystem(HuskyBot))
