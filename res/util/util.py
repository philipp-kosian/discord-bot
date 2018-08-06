class Utility:
    
    def __init__(self, client):
        self.client = client


    async def is_command(self, msg_content):
        if msg_content.startswith(self.client.config.general['cmd_ident']):
            return True


    # Returns the x part seperated by spaces in content
    async def get_content_part(self, content, part_num, max_parts=10):

        # remove command letter
        content = content[len(self.client.config.general['cmd_ident']):]

        # split message at the next spaces in maximum maxS+1 parts
        parts = content.split(' ', max_parts)

        # check if message has enough parts to return requested part
        if len(parts) >= part_num:
            return parts[part_num - 1]
        else:
            return None
    
    # Send info message
    async def info_message(self, channel, content):
        await self.client.send_message(
            channel,
            "Info: " + content
        )

    # Sends an error message
    async def error_message(self, channel, content):
        await self.client.send_message(
            channel, 
            "Error: " + content + "\nType `!help [command]` to list all possible commands or add a command to get more information."
        )

    # Sends different help messages depending on second argument
    async def help_message(self, channel, cmd=None):

        out = ""

        if cmd is None:                    # If the help command is not specified, output a list of all possible commands.

            out += "Help menu: List of all possible commands: \n"

            counter = 0
            for key in self.client.config.cmd_fct.keys():               # Iteration through all keys, adding them to output string
                out += "`!" + key + "`"
                if counter < len(self.client.config.cmd_fct) - 1:         # Adds comma when not last element
                    out += ", "
                counter += 1

            out += "\nSpecify by typing `!help [command]`."

        # displays help for specific command if it is in cmd_list
        elif cmd in self.client.config.cmd_fct:

            if cmd in self.client.config.cmd_info:
                if self.client.config.cmd_info[cmd] is not None and self.client.config.cmd_info[cmd] != '':
                    out += "Help menu for `!" + cmd + "`:\n"
                    out += self.client.config.cmd_info[cmd] + "\n"
            else:
                out += "Help menu for `!" + cmd + "`:\nSorry, there's no help available for this command yet."

        # Default if command is not found
        else:
            out += "Command `!" + cmd + "` does not exist."

        await self.client.send_message(channel, out)