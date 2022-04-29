from json import loads

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

from dotty.command_registry import CommandRegistry
from dotty.core import ChatBot
from dotty.message import Message
from dotty.profile_storage import ProfileStorage
from dotty.user_registry import UserRegistry


friends = {}
client = None
bot_name = "Dotty bot"


def jid_to_username(jid):
    return jid.split("@")[0][0:-4]


def get_kik_account():
    with open("kik_account.json") as account_file:
        return loads(account_file.read())


def ago(timestamp: int) -> str:
    from datetime import datetime

    then = datetime.utcfromtimestamp(int(timestamp) / 1000)
    now = datetime.utcnow()
    diff = now - then
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


class InteractiveChatClient(KikClientCallback):
    def __init__(self, chat_bot: ChatBot):
        self.chat_bot = chat_bot
        self._groups = []
        self._users = []

    def on_authenticated(self):
        print(f"Authenticated as {client.username} ({client.kik_node})")
        client.request_roster()

    def _add_user(self, user: User):
        self._users.append({"display_name": user.display_name, "username": user.username, "user_jid": user.jid})
        self.chat_bot.update_user(user_jid=user.jid)

    def _add_group_member(self, group_member: GroupMember):
        self._users.append({"user_jid": group_member.jid})
        self.chat_bot.update_user(user_jid=group_member.jid)

    def on_roster_received(self, response: FetchRosterResponse):
        for peer in response.peers:
            if peer.__class__ == Group:
                self._groups.append({"name": peer.name, "group_jid": peer.jid})
                for member in peer.members:
                    self._add_group_member(member)
            elif peer.__class__ == User:
                self._add_user(peer)

    def on_group_message_received(self, response: IncomingGroupChatMessage):
        incoming_message = Message(body=response.body, sent_by=response.from_jid, sent_in=response.group_jid)
        answer = self.chat_bot.process_message(message=incoming_message)
        if answer and client:
            client.send_chat_message(peer_jid=response.group_jid, message=answer)
        client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("Connection failed")

    def on_video_received(self, response: IncomingVideoMessage):
        print(f"Video sent on {response.metadata.timestamp} url: {response.video_url}")
        client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_image_received(self, response: IncomingImageMessage):
        print(f"Image sent on {response.metadata.timestamp} url: {response.image_url}")
        client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id, group_jid=response.group_jid)

    def on_chat_message_received(self, response: IncomingChatMessage):
        print(f"DM sent on {response.metadata.timestamp} by: {response.from_jid}")
        client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id)

    def on_status_message_received(self, response: IncomingStatusResponse):
        print(f"Status {response.status} sent on {response.metadata.timestamp} by: {response.from_jid}")
        client.send_read_receipt(peer_jid=response.from_jid, receipt_message_id=response.message_id)

    def on_group_status_received(self, response: IncomingGroupStatus):
        print(f"Status {response.status} sent on {response.metadata.timestamp} in: {response.group_jid}")


if __name__ == "__main__":
    kik_account = get_kik_account()
    profile_storage = ProfileStorage()
    users_registry = UserRegistry(profile_storage=profile_storage)
    command_registry = CommandRegistry(bot_name=bot_name)
    dotty_bot = ChatBot(
        name=bot_name, owner_identifier=kik_account["owner"]["jid"], users_registry=users_registry, command_registry=command_registry
    )

    callback = InteractiveChatClient(dotty_bot)
    client = KikClient(
        callback=callback,
        kik_username=kik_account["bot"]["account"],
        kik_password=kik_account["bot"]["password"],
        kik_node=kik_account["bot"]["kik_node"],
    )

    exit_loop = False
    while not exit_loop:
        message = input()
        if message.casefold() == "bye":
            exit_loop = True

    client.loop.stop()
    client.disconnect()
