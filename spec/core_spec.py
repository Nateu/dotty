from expects import equal, expect
from mamba import context, describe, it

from dotty.chat_bot import ChatBot
from dotty.command_identifier import CommandIdentifier
from dotty.message import Message
from dotty.security_level import SecurityLevel
from spec.fakes import FakeCommand, FakeCommandRegistry, FakeUser, FakeUserRegistry


with describe("Given the dotty ChatBot") as self:
    with context("when processing a message send by a guest"):
        with it("should not respond at all"):
            # Set Up
            self.command_registry = FakeCommandRegistry()
            self.users_registry = FakeUserRegistry()
            self.users_registry.is_registered_user_outcome = False
            self.chat_bot = ChatBot(
                name="Dotty",
                owner_identifier="@owner",
                users_registry=self.users_registry,
                command_registry=self.command_registry,
            )
            # Run
            input_message = Message("stuff from a guest", "@guest", "#group")
            # Assertion
            expect(self.chat_bot.process_message(input_message)).to(equal(None))

    with context("when someone with clearance speaks"):
        with context("and they don't trigger a command"):
            with it("should not respond at all"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.OWNER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("stuff that will never be a command", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal(None))

        with context("and the command doesn't exist"):
            with it("should not respond at all"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.UNSET
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.OWNER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("stuff that will never be a command", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal(None))

        with context("and they list all commands"):
            with it("should print 'These commands are available:\nThese are all the commands'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.LIST_COMMANDS
                self.command_registry.get_matching_command_response.get_trigger_response = "Usage"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.command_registry.get_commands_string_response = "These are all the commands"
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("usage", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("These commands are available:\nThese are all the commands"))

        with context("and they set a new USER substitution"):
            with it("should print 'When you say: \"substitute\", I say: this is a substitution text'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_USER_SUBSTITUTION
                self.command_registry.get_matching_command_response.get_trigger_response = "substitute"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.command_registry.register_substitution_response = FakeCommand()
                self.command_registry.register_substitution_response.repr_response = "this is a substitution text"
                self.command_registry.register_substitution_response.get_trigger_response = "substitute"
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("substitute", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(
                    equal('When you say: "substitute", I say: this is a substitution text')
                )

        with context("and they set a new USER substitution"):
            with context("and this can not be done"):
                with it("should do nothing"):
                    # Set Up
                    self.command_registry = FakeCommandRegistry()
                    self.command_registry.get_matching_command_response = FakeCommand()
                    self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_USER_SUBSTITUTION
                    self.command_registry.get_matching_command_response.get_trigger_response = "substitute"
                    self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                    self.command_registry.get_matching_command_response.has_match_response = True
                    self.users_registry = FakeUserRegistry()
                    self.users_registry.is_registered_user_outcome = True
                    self.users_registry.get_user_response = FakeUser()
                    self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                    self.chat_bot = ChatBot(
                        name="Dotty",
                        owner_identifier="@owner",
                        users_registry=self.users_registry,
                        command_registry=self.command_registry,
                    )
                    # Run
                    input_message = Message("substitute", "@owner", "#group")
                    # Assertion
                    expect(self.chat_bot.process_message(input_message)).to(equal(None))

        with context("and they set a new ADMIN substitution"):
            with it("should print 'When you say: \"substitute\", I say: this is a substitution text'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_ADMIN_SUBSTITUTION
                self.command_registry.get_matching_command_response.get_trigger_response = "substitute"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.command_registry.register_substitution_response = FakeCommand()
                self.command_registry.register_substitution_response.repr_response = "this is a substitution text"
                self.command_registry.register_substitution_response.get_trigger_response = "substitute"
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("substitute", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(
                    equal('When you say: "substitute", I say: this is a substitution text')
                )

        with context("and they list all substitutions"):
            with it("should print 'These substitutions are set: this, that, something'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.LIST_SUBSTITUTIONS
                self.command_registry.get_matching_command_response.get_trigger_response = "List"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.command_registry.get_substitution_listing_response = "this, that, something"
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("usage", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("These substitutions are set: this, that, something"))

        with context("and they trigger a substitution"):
            with it("should print 'this is a substitution text'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.GET_SUBSTITUTION
                self.command_registry.get_matching_command_response.get_trigger_response = "substitute"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.command_registry.get_matching_command_response.repr_response = "this is a substitution text"
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("substitute", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("this is a substitution text"))

        with context("and they set a new theme"):
            with it("should print 'Theme set to: Alibaba'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_THEME
                self.command_registry.get_matching_command_response.get_trigger_response = "Set theme "
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Set theme Alibaba", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("Theme set to: Alibaba"))

        with context("and they get the current theme"):
            with it("should print 'Alibaba'"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.GET_THEME
                self.command_registry.get_matching_command_response.get_trigger_response = "theme"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                self.chat_bot._theme = "Alibaba"
                # Run
                input_message = Message("theme", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("Alibaba"))

        with context("and they grant a GUEST Security Level of OWNER"):
            with it('should say "User registered"'):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_ROLE_OWNER
                self.command_registry.get_matching_command_response.get_trigger_response = "Grant Owner "
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Grant Owner @someone", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("User registered"))

        with context("and they revoke the Security Level of OWNER"):
            with context("and this can be done"):
                with it('should say "User registered"'):
                    # Set Up
                    self.command_registry = FakeCommandRegistry()
                    self.command_registry.get_matching_command_response = FakeCommand()
                    self.command_registry.get_matching_command_response.identifier = CommandIdentifier.REMOVE_ROLE_OWNER
                    self.command_registry.get_matching_command_response.get_trigger_response = "Revoke Owner Pietje"
                    self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                    self.command_registry.get_matching_command_response.has_match_response = True
                    self.users_registry = FakeUserRegistry()
                    self.users_registry.is_registered_user_outcome = True
                    self.users_registry.get_user_response = FakeUser()
                    self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.OWNER

                    self.chat_bot = ChatBot(
                        name="Dotty",
                        owner_identifier="@owner",
                        users_registry=self.users_registry,
                        command_registry=self.command_registry,
                    )
                    # Run
                    input_message = Message("Grant Owner @someone", "@owner", "#group")
                    # Assertion
                    expect(self.chat_bot.process_message(input_message)).to(equal("Rights revoked"))

            with context("and this can not be done"):
                with it('should say "User registered"'):
                    # Set Up
                    self.command_registry = FakeCommandRegistry()
                    self.command_registry.get_matching_command_response = FakeCommand()
                    self.command_registry.get_matching_command_response.identifier = CommandIdentifier.REMOVE_ROLE_OWNER
                    self.command_registry.get_matching_command_response.get_trigger_response = "Revoke Owner Pietje"
                    self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                    self.command_registry.get_matching_command_response.has_match_response = True
                    self.users_registry = FakeUserRegistry()
                    self.users_registry.is_registered_user_outcome = True
                    self.users_registry.get_user_response = FakeUser()
                    self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                    self.chat_bot = ChatBot(
                        name="Dotty",
                        owner_identifier="@owner",
                        users_registry=self.users_registry,
                        command_registry=self.command_registry,
                    )
                    # Run
                    input_message = Message("Grant Owner @someone", "@owner", "#group")
                    # Assertion
                    expect(self.chat_bot.process_message(input_message)).to(equal("Rights already revoked"))

        with context("and they grant a GUEST Security Level of ADMIN"):
            with it('should say "User registered"'):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_ROLE_ADMIN
                self.command_registry.get_matching_command_response.get_trigger_response = "Grant Admin "
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.GUEST

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Grant Admin @admin", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("User registered"))

        with context("and they revoke the Security Level of ADMIN"):
            with it('should say "Rights revoked"'):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.REMOVE_ROLE_ADMIN
                self.command_registry.get_matching_command_response.get_trigger_response = "Grant Admin "
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.OWNER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Grant Admin @admin", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("Rights revoked"))

        with context("and they grant a GUEST Security Level of USER"):
            with context("and this can not be done"):
                with it('should say "User already registered"'):
                    # Set Up
                    self.command_registry = FakeCommandRegistry()
                    self.command_registry.get_matching_command_response = FakeCommand()
                    self.command_registry.get_matching_command_response.identifier = CommandIdentifier.SET_ROLE_USER
                    self.command_registry.get_matching_command_response.get_trigger_response = "Revoke Owner Pietje"
                    self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                    self.command_registry.get_matching_command_response.has_match_response = True
                    self.users_registry = FakeUserRegistry()
                    self.users_registry.is_registered_user_outcome = True
                    self.users_registry.get_user_response = FakeUser()
                    self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                    self.chat_bot = ChatBot(
                        name="Dotty",
                        owner_identifier="@owner",
                        users_registry=self.users_registry,
                        command_registry=self.command_registry,
                    )
                    # Run
                    input_message = Message("Grant Owner @someone", "@owner", "#group")
                    # Assertion
                    expect(self.chat_bot.process_message(input_message)).to(equal("User already registered"))

        with context("and they revoke the Security Level of USER"):
            with it('should say "Rights revoked"'):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.REMOVE_ROLE_USER
                self.command_registry.get_matching_command_response.get_trigger_response = "Grant Admin "
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.USER

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Grant Admin @admin", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("Rights revoked"))

        with context("and they list all users"):
            with it("should list all users"):
                # Set Up
                self.command_registry = FakeCommandRegistry()
                self.command_registry.get_matching_command_response = FakeCommand()
                self.command_registry.get_matching_command_response.identifier = CommandIdentifier.LIST_USERS
                self.command_registry.get_matching_command_response.get_trigger_response = "Users"
                self.command_registry.get_matching_command_response.get_security_level_response = SecurityLevel.OWNER
                self.command_registry.get_matching_command_response.has_match_response = True
                self.users_registry = FakeUserRegistry()
                self.users_registry.is_registered_user_outcome = True
                self.users_registry.get_user_response = FakeUser()
                self.users_registry.get_user_response.get_user_clearance_level_response = SecurityLevel.OWNER
                self.users_registry.get_user_listing_response = "Pascal"

                self.chat_bot = ChatBot(
                    name="Dotty",
                    owner_identifier="@owner",
                    users_registry=self.users_registry,
                    command_registry=self.command_registry,
                )
                # Run
                input_message = Message("Users", "@owner", "#group")
                # Assertion
                expect(self.chat_bot.process_message(input_message)).to(equal("The current users\nPascal"))
