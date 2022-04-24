from typing import Optional

from expects import equal, expect
from mamba import before, context, describe, it

from dotty.core import ChatBot, Message
from dotty.storage import Storage
from dotty.user import UserRegistry


class FakeStorage(Storage):
    def __init__(self):
        self._data: str = ""

    def store_in(self, data: str, storage_name: str):
        self._data = data

    def retrieve_data(self, storage_name: str) -> Optional[str]:
        return self._data


with describe("Given dotty.core ChatBot.process_message") as self:
    with before.each:
        user_storage = FakeStorage()
        users_registry = UserRegistry(user_storage)
        self.chat_bot = ChatBot(name="Dotty", owner_identifier="@owner", users_registry=users_registry)

    with context("when a guest sends a message"):
        with it("should not respond at all"):
            input_message = Message("stuff from a guest", "@guest", "#group")
            expect(self.chat_bot.process_message(input_message)).to(equal(None))

    with context("when you send a non command"):
        with it("should not respond at all"):
            input_message = Message("stuff that will never be a command", "@owner", "#group")
            expect(self.chat_bot.process_message(input_message)).to(equal(None))

    with context("when you grant @admin Security level Admin"):
        with it('should say "User registered"'):
            input_message = Message("Grant Admin @admin", "@owner", "#group")
            expect(self.chat_bot.process_message(input_message)).to(equal("User registered"))

    with context("and you grant @someone Security level Owner"):
        with it('should say "User registered"'):
            input_message = Message("Grant Owner @someone", "@owner", "#group")
            expect(self.chat_bot.process_message(input_message)).to(equal("User registered"))

    with context("when you send: usage"):
        with it("should print all commands"):
            input_message = Message("usage", "@owner", "#group")
            expect(self.chat_bot.process_message(input_message)).to(
                equal(
                    'These commands are available:\n"Usage" - List all commands and their usage\n"List" - List all '
                    'substitutions\n" -> " - On the trigger (before) -> Dotty will respond with message (after) ['
                    'USERS]\n" => " - On the trigger (before) => Dotty will respond with message (after) ['
                    'ADMINS]\n"Theme" - This will give back the current theme\n"Set Theme " - This will set a theme, '
                    'anything after "set theme " will be the theme\n"Grant User " - Command to grant a member user '
                    'status\n"Grant Admin " - Command to grant a member admin status\n"Grant Owner " - Command to '
                    'grant a member owner status\n"Revoke Owner " - Command to revoke a member owner status\n"Revoke '
                    'Admin " - Command to revoke a member admin status\n"Revoke User " - Command to revoke a member '
                    "user status\n"
                )
            )

    with context("when an admin speaks"):
        with before.each:
            input_message = Message("Grant Admin @admin", "@owner", "#group")
            self.chat_bot.process_message(input_message)

        with context("and they sent: usage"):
            with it("should print all commands"):
                input_message = Message("usage", "@admin", "#group")
                expect(self.chat_bot.process_message(input_message)).to(
                    equal(
                        'These commands are available:\n"Usage" - List all commands and their usage\n"List" - List '
                        'all substitutions\n" -> " - On the trigger (before) -> Dotty will respond with message ('
                        'after) [USERS]\n" => " - On the trigger (before) => Dotty will respond with message (after) '
                        '[ADMINS]\n"Theme" - This will give back the current theme\n"Set Theme " - This will set a '
                        'theme, anything after "set theme " will be the theme\n"Grant User " - Command to grant a '
                        'member user status\n"Revoke User " - Command to revoke a member user status\n'
                    )
                )

        with context("and they send: rules -> Follow tha rules"):
            with it("should respond with the substitution set"):
                input_message = Message("rules -> Follow tha rules", "@admin", "#group")
                expect(self.chat_bot.process_message(input_message)).to(
                    equal('When you say: "rules", I say: Follow tha rules')
                )

        with context("and they send: set theme Avatar, the last Airbender"):
            with it("should respond with: theme set to: Avatar, the last Airbender"):
                input_message = Message("set theme Avatar, the last Airbender", "@admin", "#group")
                expect(self.chat_bot.process_message(input_message)).to(
                    equal("Theme set to: Avatar, the last Airbender")
                )

        with context("and they send: Admin => The best people around!"):
            with it('should respond with: When you say: "Admin", I say: The best people around!'):
                input_message = Message("Admin => The best people around!", "@admin", "#group")
                expect(self.chat_bot.process_message(input_message)).to(
                    equal('When you say: "Admin", I say: The best people around!')
                )

        with context("and they grant @user Security level User"):
            with it('should say "User registered"'):
                input_message = Message("Grant User @user", "@admin", "#group")
                expect(self.chat_bot.process_message(input_message)).to(equal("User registered"))

        with context("and @user has the Security level User"):
            with before.each:
                input_message = Message("Grant User @user", "@admin", "#group")
                self.chat_bot.process_message(input_message)

            with context("and they grant @user Security level User for the second time"):
                with it('should say "User already registered"'):
                    input_message = Message("Grant User @user", "@admin", "#group")
                    expect(self.chat_bot.process_message(input_message)).to(equal("User already registered"))

    with context("when an user speaks"):
        with before.each:
            input_message = Message("Grant User @user", "@owner", "#group")
            self.chat_bot.process_message(input_message)

        with context("and they send: list"):
            with it("should return a string starting with These substitutions are set: "):
                input_message = Message("list", "@user", "#group")
                expect(self.chat_bot.process_message(input_message)).to(equal("These substitutions are set: "))

        with context("and they send: Theme"):
            with it("should respond with: No theme set"):
                input_message = Message("Theme", "@user", "#group")
                expect(self.chat_bot.process_message(input_message)).to(equal("No theme set"))

        with context("and they send: Grant Owner @me"):
            with it("should not respond"):
                input_message = Message("Grant Owner @me", "@user", "#group")
                expect(self.chat_bot.process_message(input_message)).to(equal(None))

        with context('and the theme "Avatar, the last Airbender" set'):
            with before.each:
                input_message = Message("set theme Avatar, the last Airbender", "@owner", "#group")
                self.chat_bot.process_message(input_message)

            with context("and they send: Theme"):
                with it("should respond with: Avatar, the last Airbender"):
                    input_message = Message("Theme", "@user", "#group")
                    expect(self.chat_bot.process_message(input_message)).to(equal("Avatar, the last Airbender"))

        with context("and there are two triggers set: rules (user) and hello (admin)"):
            with before.each:
                input_message = Message("Hello => Hello my name is Dotty", "@owner", "#group")
                self.chat_bot.process_message(input_message)
                input_message.body = "rules -> Follow tha rules"
                self.chat_bot.process_message(input_message)

            with context("and they send: list"):
                with it("should respond with: These substitutions are set: rules"):
                    input_message = Message("list", "@user", "#group")
                    expect(self.chat_bot.process_message(input_message)).to(equal("These substitutions are set: rules"))

            with context("and they send: rules"):
                with it("should respond with: Follow tha rules"):
                    input_message = Message("rules", "@user", "#group")
                    expect(self.chat_bot.process_message(input_message)).to(equal("Follow tha rules"))

            with context("and they send: hello"):
                with it("should not respond as it's an Admin substitution"):
                    input_message = Message("hello", "@user", "#group")
                    expect(self.chat_bot.process_message(input_message)).to(equal(None))
