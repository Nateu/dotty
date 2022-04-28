from expects import equal, expect
from mamba import before, context, describe, it

from dotty.command import (
    Command,
    CommandRegistry,
    ContainsCommand,
    ExactCommand,
    StartsWithCommand,
    SubstitutionCommand,
)
from dotty.command_identifier import CommandIdentifier
from dotty.security_level import SecurityLevel


with describe("Given the a chat bot command") as self:
    with context("when it is created with CommandIdentifier GET_THEME"):
        with it("should have a CommandIdentifier"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.identifier).to(equal(CommandIdentifier.GET_THEME))

        with it("should have a trigger"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.get_trigger()).to(equal("Theme"))

        with it("should provide a lower case version of the trigger"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.get_trigger_lower_case()).to(equal("Theme".casefold()))

        with it("should provide a lower case version of the trigger"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.is_substitution()).to(equal(False))

        with it("should provide a lower case version of the trigger"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.get_security_level()).to(equal(SecurityLevel.USER))

        with it("should give its trigger and description when printed"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.__repr__()).to(equal('"Theme" - A command to retrieve the current theme'))

    with context("when it is created with the Security Level USER"):
        with it("should be cleared for use by a USER"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.has_clearance(requested_by=SecurityLevel.USER)).to(equal(True))

        with it("should not be cleared for use by a GUEST"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.has_clearance(requested_by=SecurityLevel.GUEST)).to(equal(False))

        with it("should be cleared for use by a ADMIN"):
            my_command = Command(
                identifier=CommandIdentifier.GET_THEME,
                trigger="Theme",
                description="A command to retrieve the current theme",
                security_level=SecurityLevel.USER,
            )
            expect(my_command.has_clearance(requested_by=SecurityLevel.ADMIN)).to(equal(True))

    with context("when it is created with CommandType STARTS_WITH"):
        with context("and a message starts with 'Set Theme '"):
            with it("should have a match"):
                my_command = StartsWithCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="Set Theme ",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.has_match(message="set theme Hello", user_security_level=SecurityLevel.ADMIN)).to(equal(True))

            with context("and the sender has a SecurityLevel lower than the commands'"):
                with it("should not have a match"):
                    my_command = StartsWithCommand(
                        identifier=CommandIdentifier.SET_THEME,
                        trigger="Set Theme ",
                        description="A command to set a new theme",
                        security_level=SecurityLevel.USER,
                    )
                    expect(my_command.has_match(message="set theme Hello", user_security_level=SecurityLevel.UNKNOWN)).to(equal(False))

        with context("and a message starts with 'Set nothing '"):
            with it("should not have a match"):
                my_command = StartsWithCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="Set Theme ",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.has_match(message="set nothing Hello", user_security_level=SecurityLevel.ADMIN)).to(equal(False))

    with context("when it is created with CommandType CONTAINS"):
        with context("and a message contains ' containing words '"):
            with it("should have a match"):
                my_command = ContainsCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger=" containing words ",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(
                    my_command.has_match(
                        message_body="This message has containing words in itself.",
                        user_security_level=SecurityLevel.ADMIN,
                    )
                ).to(equal(True))

            with context("and the sender has a SecurityLevel lower than the commands'"):
                with it("should not have a match"):
                    my_command = ContainsCommand(
                        identifier=CommandIdentifier.SET_THEME,
                        trigger=" containing words ",
                        description="A command to set a new theme",
                        security_level=SecurityLevel.USER,
                    )
                    expect(my_command.has_match(message_body="set theme Hello", user_security_level=SecurityLevel.UNKNOWN)).to(equal(False))

        with context("and a does not contain: ' containing words '"):
            with it("should not have a match"):
                my_command = ContainsCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger=" containing words ",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.has_match(message_body="set nothing Hello", user_security_level=SecurityLevel.ADMIN)).to(equal(False))

    with context("when it is created with CommandType EXACT"):
        with context("and a message matches 'This Trigger'"):
            with it("should have a match"):
                my_command = ExactCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="This Trigger",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(
                    my_command.has_match(
                        message_body="This Trigger",
                        user_security_level=SecurityLevel.ADMIN,
                    )
                ).to(equal(True))

            with context("and the sender has a SecurityLevel lower than the commands'"):
                with it("should not have a match"):
                    my_command = ExactCommand(
                        identifier=CommandIdentifier.SET_THEME,
                        trigger="This Trigger",
                        description="A command to set a new theme",
                        security_level=SecurityLevel.USER,
                    )
                    expect(my_command.has_match(message_body="set theme Hello", user_security_level=SecurityLevel.UNKNOWN)).to(equal(False))

        with context("and a does not match: 'This Trigger'"):
            with it("should not have a match"):
                my_command = ExactCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="This Trigger",
                    description="A command to set a new theme",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.has_match(message_body="set nothing Hello", user_security_level=SecurityLevel.ADMIN)).to(equal(False))

    with context("when it is created with CommandType SUBSTITUTION"):
        with context("and a message matches 'This Trigger'"):
            with it("should have a match"):
                my_command = SubstitutionCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="This Trigger",
                    substitution="Will become just this",
                    security_level=SecurityLevel.USER,
                )
                expect(
                    my_command.has_match(
                        message_body="This Trigger",
                        user_security_level=SecurityLevel.ADMIN,
                    )
                ).to(equal(True))

            with context("and the sender has a SecurityLevel lower than the commands'"):
                with it("should not have a match"):
                    my_command = SubstitutionCommand(
                        identifier=CommandIdentifier.SET_THEME,
                        trigger="This Trigger",
                        substitution="Will become just this",
                        security_level=SecurityLevel.USER,
                    )
                    expect(my_command.has_match(message_body="This Trigger", user_security_level=SecurityLevel.UNKNOWN)).to(equal(False))

        with context("and a does not match: 'This Trigger'"):
            with it("should not have a match"):
                my_command = SubstitutionCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="This Trigger",
                    substitution="Will become just this",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.has_match(message_body="set nothing Hello", user_security_level=SecurityLevel.ADMIN)).to(equal(False))

        with context("and it is printed"):
            with it("should respond with 'Will become just this'"):
                my_command = SubstitutionCommand(
                    identifier=CommandIdentifier.SET_THEME,
                    trigger="This Trigger",
                    substitution="Will become just this",
                    security_level=SecurityLevel.USER,
                )
                expect(my_command.__repr__()).to(equal("Will become just this"))

with describe("Given a command registry") as self:
    with context("when it is created"):
        with it("should 12 commands"):
            command_registry = CommandRegistry()
            count = len(command_registry._all_commands)
            expect(command_registry.get_commands_string(user_security_level=SecurityLevel.OWNER).count("\n")).to(equal(count))

        with it("should have no substitutions"):
            command_registry = CommandRegistry()
            expect(command_registry.get_substitution_listing(user_security_level=SecurityLevel.OWNER)).to(equal(""))

    with context("when searching for a command that doesn't exists"):
        with it("should return None"):
            command_registry = CommandRegistry()
            expect(command_registry.get_matching_command(message="no such command", user_security_level=SecurityLevel.OWNER)).to(
                equal(None)
            )

    with context("when searching for teh usage command"):
        with it("should return the command"):
            command_registry = CommandRegistry()
            expect(
                command_registry.get_matching_command(message="usage", user_security_level=SecurityLevel.OWNER).get_trigger_lower_case()
            ).to(equal("usage"))

    with context("when registering a new substitution"):
        with before.each:
            self.command_registry = CommandRegistry()
            self.response = self.command_registry.register_substitution(
                trigger="trigger", substitution="This is a better text", security_level=SecurityLevel.ADMIN
            )

        with it("should return the new substitution command"):
            expect(self.response.get_trigger_lower_case()).to(equal("trigger"))

        with context("and a higher level substitution exists"):
            with it("should return nothing"):
                expect(
                    self.command_registry.register_substitution(
                        trigger="trigger", substitution="This is an even better text", security_level=SecurityLevel.USER
                    )
                ).to(equal(None))

        with context("and a you try to register the same trigger and security level combo again"):
            with it("should replace the command"):
                expect(
                    self.command_registry.register_substitution(
                        trigger="trigger", substitution="This is an even better text", security_level=SecurityLevel.ADMIN
                    ).__repr__()
                ).to(equal("This is an even better text"))
