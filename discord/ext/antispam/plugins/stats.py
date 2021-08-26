import discord
import typing
from discord.ext.antispam import AntiSpamHandler  # noqa

from discord.ext.antispam.base_plugin import BasePlugin


class Stats(BasePlugin):
    """
    A simplistic approach to aggregating statistics
    across the anti spam package.

    Do note however, it assumes plugins do not error out.
    If a plugin errors out, this will be inaccurate.

    This does play with internals a bit,
    however, it is distributed within the
    library I am oki modifying the base package
    to make this work even better.
    """

    injectable_nonce = "Issa me, Mario!"  # For our `propagate` check

    def __init__(self, anti_spam_handler: AntiSpamHandler):
        super().__init__(is_pre_invoke=False)

        self.data = {
            "pre_invoke_calls": {},
            "after_invoke_calls": {},
            "propagate_calls": 0,
            "guilds": {},
            "members": {},
        }
        self.handler = anti_spam_handler

    async def propagate(
        self, message: discord.Message, data: typing.Optional[dict] = None
    ) -> dict:
        for invoker in self.handler.pre_invoke_extensions.keys():
            try:
                self.data["pre_invoke_calls"][invoker]["calls"] += 1
            except KeyError:
                self.data["pre_invoke_calls"][invoker] = {}
                self.data["pre_invoke_calls"][invoker]["calls"] = 1

        for invoker in self.handler.after_invoke_extensions.keys():
            try:
                self.data["after_invoke_calls"][invoker]["calls"] += 1
            except KeyError:
                self.data["after_invoke_calls"][invoker] = {}
                self.data["after_invoke_calls"][invoker]["calls"] = 1

        self.data["propagate_calls"] += 1

        if message.guild.id not in self.data["guilds"]:
            self.data["guilds"][message.guild.id] = {"calls": 0, "messages_punished": 0}

        self.data[message.guild.id]["calls"] += 1

        if message.author.id not in self.data["members"]:
            self.data["members"][message.author.id] = {"calls": 0, "times_punished": 0}

        self.data["members"][message.author.id]["calls"] += 1

        if data["should_be_punished_this_message"]:
            self.data["members"][message.author.id]["times_punished"] += 1
            self.data["guilds"][message.guild.id]["times_punished"] += 1

        return {"status": "Updated stats!"}
