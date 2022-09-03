from dotty.chat_bot import ChatBot
from dotty.command_registry import CommandRegistry
from dotty.dotty import Dotty
from dotty.profile_storage import ProfileStorage
from dotty.statics import get_config
from dotty.user_registry import UserRegistry

from kik_unofficial.client import KikClient



class BotSetUp:
    def __init__(self, bot_name: str):
        self.exit_loop = False
        self.config = get_config()
        self.profile_storage = ProfileStorage()
        self.users_registry = UserRegistry(profile_storage=self.profile_storage)
        self.command_registry = CommandRegistry(bot_name=bot_name)
        self.dotty_bot = ChatBot(
            name=bot_name,
            owner_identifier=self.config["owner"]["jid"],
            users_registry=self.users_registry,
            command_registry=self.command_registry,
        )

        self.callback = Dotty(self.dotty_bot)
        self.client = KikClient(
            callback=self.callback, kik_username=self.config["dotty"]["account"], kik_password=self.config["dotty"]["password"]
        )
        self.callback.set_client(self.client)

    def bot_loop(self):
        while not self.exit_loop:
            if self.callback.exit:
                self.exit_loop = True
            if input().casefold() == "bye":
                self.exit_loop = True

    def stop_session(self):
        self.exit_loop = True
        self.client.loop.stop()
        self.client.disconnect()


if __name__ == "__main__":
    bot_set_up = BotSetUp(bot_name="Dotty bot")
    bot_set_up.bot_loop()
    bot_set_up.stop_session()
