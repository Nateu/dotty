from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.peers import Group, GroupMember, User
from kik_unofficial.datatypes.xmpp.chatting import (
    IncomingChatMessage,
    IncomingGroupChatMessage,
    IncomingGroupStatus,
    IncomingImageMessage,
    IncomingStatusResponse,
    IncomingVideoMessage,
)
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse

from bot.chat_bot import ChatBot
from bot.command_registry import CommandRegistry
from bot.message import Message
from bot.profile_storage import ProfileStorage
from bot.statics import get_config
from bot.user_registry import UserRegistry


class InteractiveChatClient(KikClientCallback):
    def __init__(self, chat_bot: ChatBot):
        self.chat_bot = chat_bot
        self._groups = []
        self._users = []
        self._user_info = []
        self.client = None
        self.exit = False

    def update_users(self):
        users = [u["user_jid"] for u in self._users]
        self.client.xiphias_get_users(users)

    def set_client(self, client):
        self.client = client

    def on_authenticated(self):
        print(f"Authenticated as {self.client.username} ({self.client.kik_node})")
        self.client.request_roster()

    # def on_xiphias_get_users_response(self, response: Union[UsersResponse, UsersByAliasResponse]):
    def on_xiphias_get_users_response(self, response):
        from json import dumps
        print(response.users)
        self._user_info = response.users
        for u in self._user_info:
            print(dumps(u))

    def on_roster_received(self, response: FetchRosterResponse):
        for peer in response.peers:
            if peer.__class__ == Group:
                self._groups.append({"name": peer.name, "group_jid": peer.jid})
                for member in peer.members:
                    self._add_group_member(member)
            elif peer.__class__ == User:
                self._add_user(peer)
        self.update_users()

    def on_group_message_received(self, response: IncomingGroupChatMessage):
        incoming_message = Message(body=response.body, sent_by=response.from_jid, sent_in=response.group_jid)
        answer = self.chat_bot.process_message(message=incoming_message)
        if answer and self.client:
            self.client.send_chat_message(peer_jid=response.group_jid, message=answer)
        self.client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print(f"Connection failed: {response.message}")

    def on_video_received(self, response: IncomingVideoMessage):
        print(f"Video sent on {response.metadata.timestamp} url: {response.video_url}")
        self.client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_image_received(self, response: IncomingImageMessage):
        print(f"Image sent on {response.metadata.timestamp} url: {response.image_url}")
        self.client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_chat_message_received(self, response: IncomingChatMessage):
        print(f"DM sent on {response.metadata.timestamp} by: {response.from_jid}")
        self.client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id)
        config = get_config()
        if response.body.casefold() == "please stop running" and response.from_jid == config["owner"]["jid"]:
            self.exit = True

    def on_status_message_received(self, response: IncomingStatusResponse):
        print(f"Status {response.status} sent on {response.metadata.timestamp} by: {response.from_jid}")
        self.client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id)

    def on_group_status_received(self, response: IncomingGroupStatus):
        print(f"Status {response.status} sent on {response.metadata.timestamp} in: {response.group_jid}")

    def _add_user(self, user: User):
        self._users.append({"display_name": user.display_name, "username": user.username, "user_jid": user.jid})
        self.chat_bot.update_user(user_jid=user.jid)

    def _add_group_member(self, group_member: GroupMember):
        self._users.append({"user_jid": group_member.jid})
        self.chat_bot.update_user(user_jid=group_member.jid)


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

        self.callback = InteractiveChatClient(self.dotty_bot)
        self.client = KikClient(
            callback=self.callback, kik_username=self.config["bot"]["account"], kik_password=self.config["bot"]["password"]
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
