from expects import equal, expect
from mamba import before, context, describe, it, fcontext

from src.dotty.command_registry import CommandRegistry
from src.dotty.security_level import SecurityLevel


with describe("Given a command registry") as self:
    with context("when it is created"):
        with it("should 12 commands"):
            command_registry = CommandRegistry()
            count = command_registry.get_command_count()
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

    with context("when searching for the usage command"):
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
