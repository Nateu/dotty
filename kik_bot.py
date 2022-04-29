from json import loads

from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.peers import Group, Peer, User, GroupMember
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage
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


class InteractiveChatClient(KikClientCallback):
    def __init__(self, chat_bot: ChatBot):
        self.chat_bot = chat_bot
        self._groups = []
        self._users = []

    def on_authenticated(self):
        print("Authenticated!")
        client.request_roster()

    def _add_user(self, user: User):
        self._users.append({
            "display_name": user.display_name,
            "username": user.username,
            "user_jid": user.jid
        })
        self.chat_bot.update_user(user_jid=user.jid)

    def _add_group_member(self, group_member: GroupMember):
        self._users.append({
            "user_jid": group_member.jid
        })
        self.chat_bot.update_user(user_jid=group_member.jid)

    def on_roster_received(self, response: FetchRosterResponse):
        for peer in response.peers:
            if peer.__class__ == Group:
                self._groups.append({
                    "name": peer.name,
                    "group_jid": peer.jid
                })
                for member in peer.members:
                    self._add_group_member(member)
            elif peer.__class__ == User:
                self._add_user(peer)

    def on_group_message_received(self, chat_message: IncomingGroupChatMessage):
        incoming_message = Message(body=chat_message.body, sent_by=chat_message.from_jid, sent_in=chat_message.group_jid)
        answer = self.chat_bot.process_message(message=incoming_message)
        if answer and client:
            client.send_chat_message(peer_jid=chat_message.group_jid, message=answer)
        client.send_read_receipt(
            peer_jid=chat_message.from_jid, receipt_message_id=chat_message.message_id, group_jid=chat_message.group_jid
        )

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("Connection failed")

    # def on_chat_message_received(self, chat_message: IncomingChatMessage):
    #     incoming_message = Message(body=chat_message.body, sent_by=chat_message.from_jid, sent_in=chat_message.group_jid)
    #     answer = self.chat_bot.process_message(message=incoming_message)
    #     if answer and client:
    #         client.send_chat_message(peer_jid=chat_message.group_jid, message=answer)
    #     client.send_read_receipt(
    #         peer_jid=chat_message.from_jid, receipt_message_id=chat_message.message_id, group_jid=chat_message.group_jid
    #     )

#         print("{}: {}".format(jid_to_username(chat_message.from_jid), chat_message.body))
#
#         if chat_message.from_jid not in friends:
#             print("New friend: {}".format(jid_to_username(chat_message.from_jid)))
#             client.send_chat_message(chat_message.from_jid, "Hi!")
#             time.sleep(1)
#             client.add_friend(chat_message.from_jid)
#             client.request_roster()
#
#
#     def on_status_message_received(self, response: IncomingStatusResponse):
#         print(response.status)
#         client.add_friend(response.from_jid)
#
#     def on_group_status_received(self, response: IncomingGroupStatus):
#         client.request_info_of_users(response.status_jid)


def jid_to_username(jid):
    return jid.split("@")[0][0:-4]


def get_kik_account():
    with open("kik_account.json") as account_file:
        return loads(account_file.read())


if __name__ == "__main__":
    kik_account = get_kik_account()
    profile_storage = ProfileStorage()
    users_registry = UserRegistry(profile_storage=profile_storage)
    command_registry = CommandRegistry(bot_name=bot_name)
    dotty_bot = ChatBot(
        name=bot_name, owner_identifier=kik_account["owner"]["jid"], users_registry=users_registry, command_registry=command_registry
    )

    # set up logging
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    # logger.addHandler(stream_handler)
    #
    # # create the client
    # callback.set_client(kik_client=client)

    callback = InteractiveChatClient(dotty_bot)
    client = KikClient(callback=callback, kik_username=kik_account["bot"]["account"],
                       kik_password=kik_account["bot"]["password"])

    exit_loop = False
    while not exit_loop:
        message = input()
        if message.casefold() == "bye":
            exit_loop = True

    client.loop.stop()
    client.disconnect()
