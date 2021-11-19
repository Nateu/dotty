from expects import equal, expect
from mamba import before, context, describe, it

from dotty.core import Commands


with describe("Given dotty.core commands.process_message ") as self:
    with before.each:
        self.commands = Commands()

    with context("when you send: usage"):
        with it("should print all commands"):
            expect(self.commands.process_message("usage")).to(
                equal(
                    'These commands are available:\n"Usage" - List all commands and their usage\n"List" - List all substitutions\n" -> " - On the trigger (before) -> Dotty will respond with message (after)\n'
                )
            )

    with context("when you send: list"):
        with it("should return a string starting with These substitutions are set: "):
            expect(self.commands.process_message("list")).to(equal("These substitutions are set: "))

    with context("when you send: rules -> Follow tha rules"):
        with it("should respond with the substitution set"):
            expect(self.commands.process_message("rules -> Follow tha rules")).to(
                equal('When you say: "rules", I say: Follow tha rules')
            )

    with context("when you send have two triggers set: rules and hello"):
        with before.each:
            self.commands.process_message("Hello -> Hello my name is Dotty")
            self.commands.process_message("rules -> Follow tha rules")

        with context("when you send: list"):
            with it("should respond with: These substitutions are set: Hello, rules"):
                expect(self.commands.process_message("list")).to(equal("These substitutions are set: Hello, rules"))

        with context("when you send: hello"):
            with it("should respond with: Hello my name is Dotty"):
                expect(self.commands.process_message("hello")).to(equal("Hello my name is Dotty"))
