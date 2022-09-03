from kik_unofficial.callbacks import KikClientCallback
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

from src.dotty.chat_bot import ChatBot
from src.dotty.message import Message
from src.dotty.statics import get_config


class Dotty(KikClientCallback):
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

