# HuskyBot
###### (v1.0)

HuskyBot is a Discord bot made with the Discord.py library. The primary function of HuskyBot is to act as a ticketing system.

## Commands

### Ticketing System
### /launch-ticketing
Launches a persistent ticket creation embed with a 'Create Ticket' button. When the user clicks on the button, they are prompted with a modal asking for additional information that will support the Ticket Support role initially declared when the command was called, then a new ticket text channel is created for them. The chosen `ticket_support_role` will get added to every ticket.

`/launch-ticketing <ticket_support_role>`

###### (User must have manage_channels permission to run this as each ticket is a new channel)

Arguments:
* ticket_support_role - The role that you would like to assign as the dedicated Ticket Support

### /ticket
Manually creates a ticket for the desired member. After this command is called, the user is then prompted with a modal asking for additional information that will support the Ticket Support role initially declared when the command was called, then a new ticket text channel is created for the requested member. The chosen `ticket_support_role` will get added to every ticket.

`/ticket <member> <ticket_support_role>`

###### (User must have manage_channels permission to run this as each ticket is a new channel)

Arguments:
* member - The member that you would like to open a ticket for
* ticket_support_role - The role that you would like to assign as the dedicated Ticket Support

### /close
When inside a ticket text channel, the user can choose to either click the "Close Ticket" button that spawns at the top of every new ticket, or call this command to close out the ticket.

`/close`

###### (User must be in a ticket text channel to call this)

### /transcript
When inside a ticket text channel, the user can choose to either click the "Generate Transcript" button that spawns at the top of every new ticket, or call this command to generate a `.log` file that contains the transcripts of the entire ticket.

`/transcript`

###### (User must be in a ticket text channel to call this)

### /add
When inside a ticket text channel, the user can call this command to add any users that they think should also be in the ticket.

`/add`

###### (User must be in a ticket text channel to call this)

### /remove
When inside a ticket text channel, the user can call this command to remove any users that they think should no longer be in the ticket.

`/remove`

###### (User must have manage_channels permission to run this. This is assuming that if the user can make a new ticket, they should be able to remove users from them also)

### Administration Commands
### /kick
Kicks users with optional specified reason. 
###### (You must have kick permissions to run this)

`/kick <member> <reason>`

Arguments:
* member - The member you wish to kick
* reason - The optional reason you kicked the user specified by <member> (default: None)

### /ban
Bans users with optional specified reason. 
###### (You must have ban permissions to run this)

`/ban <member> <reason>`

Arguments:
* member - The member you wish to ban
* reason - The optional reason you banned the user specified by <member> (default: None)

### /clear
Clears a specified backlog of messages in channel where command was invoked.
###### (You must have manage_messages permissions to run this)

`/clear <amount>`

Arguments:
* amount - Number of previous messages to clear (default: 1)

### Role Commands
###### (If HuskyBot and the user running the command have proper manage roles permissions and this command still doesn't work, make sure to place HuskyBot's role in the Role Hierarchy of the guild at the top)

### /role add
Adds the user to the specified role. 
###### (You must have manage_users permissions to run this)

`/role add <member> <role>`

Arguments:
* member - The member to add the role to
* role - The role to add the member to

### /role remove
Removes the user from the specified role.
###### (You must have manage_users permissions to run this)

`/role remove <member> <role>`

Arguments:
* member - The member to remove the role from
* role - The role to remove from the user

### File Commands
### /delimited
Creates and uploads a file based on the user's descision.

`/delimited <desired_file_type> <where_to_split> <user_input>`

###### where_to_split - Optional and defaults to splitting on spaces if nothing is provided.

Desired File Types:
* csv - Creates a csv delimited file based on user input 
* line - Creates a line delimited file based on user input
* tab - Creates a tab delimited file based on user input

### Miscellaneous Commands

### /help
If you need assistance with anything related to HuskyBot use this command.

`/help`

### /up
Changes the input provided to uppercase.

`/up <user_input>`

Arguments:
* user_input - Any input given by the user to be changed to uppercase

### /low
Changes the input provided to lowercase.

`/low <user_input>`

Arguments:
* user_input - Any input given by the user to be changed to lowercase

### Syncing slash commands for HuskyBot
### /sync
Syncs slash commands based on choice.
###### (Must be the owner/creator of the API key that HuskyBot is currently using to run this command)

* `/sync`           | Global sync
* `/sync !`         | Sync current guild
* `/sync *`         | Copies all global app commands to current guild and syncs
* `/sync ^`         | Clears all commands from the current guild target and syncs (removes guild commands)
* `/sync id_1 id_2` | Syncs guilds with id 1 and 2

# Creating your own Discord Bot

If you wish to create your own Discord Bot, it needs to work with the Discord API. This section explains how to utilize the discord.py library to work with Discord's API.

## Making a Discord Bot account

* Navigate to: `https://discord.com/developers/applications`
* Click on the "New Application"
* Give your application a name and click "Create"
* Next, create a Bot User by navigating to the tab labeled "Bot", and clicking "Add Bot"
  * Click "Yes, do it" to continue
* If you want your Bot to be able ot join other people's servers, you must ensure that the option "Public Bot" is checked
  * Also, make sure that the option "Require OAuth2 Code Grant" is unchecked unless you are working with or developing a service that needs it.
* Generate your Bot's API Key and copy it

Now that you have that API Key, you can use your program to login to Discord with your new Bot account.

## Inviting your Discord Bot account

So you made your new Bot, but it is not in any server yet. Here are the steps to invite it to any server of your choosing (Assuming you have permission to invite users).

### Firstly, you must create an invite URL for your bot:

* Navigate to: `https://discord.com/developers/applications`
* Click on your Bot's page
* Go to the "OAuth2" tab on the left-hand side
  * Then navigate to the sub-option "OAuth2 URL Generator"
* Tick the "bot" scope checkbox
  * A new list of checkbox options should appear under the scopes section called "Bot Permissions"
* Under this new section, check the boxes matching the permissions that your bot will require when it joins a server to function as intended
  * Make sure that you are aware of the consequences of requiring your bot to have the “Administrator” permission
* The resulting URL that is generated at the bottom of the screen can be copied when all of the required permissions for your Bot have been checked
* Paste the URL into your web browser and choose which server you would like to have your Bot join, and click "Authorize"

Your Bot should now have successfully joined the Discord Server of your choosing.

## Working with your Discord Bot

Now that you have generated your Discord Bot's API Key and you have invited it to the server(s) of your choosing, you probably want to get to work making your Bot function as you wish.

To do this, make sure that you have cloned the HuskyBot files from my GitHub.

* Follow the instructions on the [GitHub docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) if you are unfamiliar with cloning repositories
  * HuskyBot repository Link: `https://github.com/ImChet/NCSA-HuskyBot.git`
* In the newly cloned HuskyBot repository, find the apikeys.py file, navigate to the discordBotAPIKey string definition and place your Discord Bot API Key in it.

You are now ready to use your Discord Bot. 

To do this, run the main.py file to sign onto Discord as your Bot.

You may use the built-in HuskyBot commands and event listeners as examples for your own Bot. If you wish, you can start from scratch and figure your own way around the discord.py library or view their [documentation](https://discordpy.readthedocs.io/en/stable/index.html) as reference.