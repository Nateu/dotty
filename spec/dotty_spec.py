from expects import equal, expect
from mamba import before, context, describe, it
from dotty.core import Commands, Message

base_message = Message("replace me", "@user", "#group")

with describe("Given dotty.core commands.process_message ") as self:
    with before.each:
        self.commands = Commands()

    with context("when you send a non command"):
        with it("should not respond at all"):
            base_message.body = "stuff that will never be a command"
            expect(self.commands.process_message(base_message)).to(equal(None))

    with context("when you send: usage"):
        with it("should print all commands"):
            base_message.body = "usage"
            expect(self.commands.process_message(base_message)).to(
                equal(
                    'These commands are available:\n"Usage" - List all commands and their usage\n"List" - List all substitutions\n" -> " - On the trigger (before) -> Dotty will respond with message (after)\n"Theme" - This will give back the current theme\n"Set Theme " - This will set a theme, anything after "set theme " will be the theme\n'
                )
            )

    with context("when you send: list"):
        with it("should return a string starting with These substitutions are set: "):
            base_message.body = "list"
            expect(self.commands.process_message(base_message)).to(equal("These substitutions are set: "))

    with context("when you send: rules -> Follow tha rules"):
        with it("should respond with the substitution set"):
            base_message.body = "rules -> Follow tha rules"
            expect(self.commands.process_message(base_message)).to(
                equal('When you say: "rules", I say: Follow tha rules')
            )

    with context("when you send: Theme"):
        with it("should respond with: No theme set"):
            base_message.body = "Theme"
            expect(self.commands.process_message(base_message)).to(equal("No theme set"))

    with context("when you send: set theme Avater, the last Airbender"):
        with it("should respond with: theme set to: Avater, the last Airbender"):
            base_message.body = "set theme Avater, the last Airbender"
            expect(self.commands.process_message(base_message)).to(equal("Theme set to: Avater, the last Airbender"))

    with context('when you send have the theme "Avater, the last Airbender" set'):
        with before.each:
            base_message.body = "set theme Avater, the last Airbender"
            self.commands.process_message(base_message)

        with context("when you send: Theme"):
            with it("should respond with: Avater, the last Airbender"):
                base_message.body = "Theme"
                expect(self.commands.process_message(base_message)).to(equal("Avater, the last Airbender"))

    with context("when you send have two triggers set: rules and hello"):
        with before.each:
            base_message.body = "Hello -> Hello my name is Dotty"
            self.commands.process_message(base_message)
            base_message.body = "rules -> Follow tha rules"
            self.commands.process_message(base_message)

        with context("when you send: list"):
            with it("should respond with: These substitutions are set: Hello, rules"):
                base_message.body = "list"
                expect(self.commands.process_message(base_message)).to(
                    equal("These substitutions are set: Hello, rules")
                )

        with context("when you send: hello"):
            with it("should respond with: Hello my name is Dotty"):
                base_message.body = "hello"
                expect(self.commands.process_message(base_message)).to(equal("Hello my name is Dotty"))
