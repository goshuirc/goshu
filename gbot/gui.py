#!/usr/bin/env python3
# Goshubot IRC Bot
# written by Daniel Oaks <daniel@danieloaks.net>
# licensed under the BSD 2-clause license


class GuiManager:
    """Handles the goshu terminal display."""

    def __init__(self, bot):
        self.bot = bot

    # Input functions
    def get_input(self, prompt, password=False):
        # Todo: if password, obscure chars
        line = input(prompt)
        return line

    # Update
    def update_info(self):
        line = 'Goshubot - '
        for server in self.bot.irc.servers:
            line += self.bot.irc.servers[server].info['name'] + ': '
            line += str(len(self.bot.irc.servers[server].info['channels'])) + ' Channels, '
            line += str(len(self.bot.irc.servers[server].info['users'])) + ' Users ; '
        print(line[:-3])

    def put_line(self, line):
        """Output the given line."""
        print(line)
