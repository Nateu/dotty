from expects import equal, expect, raise_error
from mamba import context, describe, it

from bot.message import Message


with describe("Given a message") as self:
    with context("when two identical messages are compared"):
        with it("should return true"):
            my_message = Message(body="my body", sent_by="me", sent_in="unit test")
            expect(my_message == my_message).to(equal(True))

    with context("when a messages is compared to a str"):
        with it("should raise a type error"):
            my_message = Message(body="my body", sent_by="me", sent_in="unit test")
            expect(lambda: my_message == "some string").to(raise_error(TypeError))
