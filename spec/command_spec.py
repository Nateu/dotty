from expects import equal, expect
from mamba import context, describe, it

from src.dotty.command import Command, ContainsCommand, ExactCommand, StartsWithCommand, SubstitutionCommand
from src.dotty.command_identifier import CommandIdentifier
from src.dotty import SecurityLevel


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
