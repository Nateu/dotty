from json import dumps

from expects import equal, expect, raise_error
from mamba import context, describe, it

from src.dotty import SecurityLevel


with describe("Given a Security Level") as self:
    with context("when the level is OWNER"):
        with it("should have a value bigger than ADMIN"):
            expect(SecurityLevel.OWNER > SecurityLevel.ADMIN).to(equal(True))

    with context("when the level OWNER is serialized"):
        with it("should have be represented in the number 9"):
            expect(dumps(SecurityLevel.OWNER)).to(equal("9"))

    with context("when the level is ADMIN"):
        with it("should have a value bigger than USER"):
            expect(SecurityLevel.ADMIN > SecurityLevel.USER).to(equal(True))

    with context("when the level ADMIN is serialized"):
        with it("should have be represented in the number 7"):
            expect(dumps(SecurityLevel.ADMIN)).to(equal("7"))

    with context("when the level is USER"):
        with it("should have a value bigger than GUEST"):
            expect(SecurityLevel.USER > SecurityLevel.GUEST).to(equal(True))

    with context("when the level USER is serialized"):
        with it("should have be represented in the number 5"):
            expect(dumps(SecurityLevel.USER)).to(equal("5"))

    with context("when the level is GUEST"):
        with it("should have a value bigger than UNKNOWN"):
            expect(SecurityLevel.GUEST > SecurityLevel.UNKNOWN).to(equal(True))

    with context("when the level GUEST is serialized"):
        with it("should have be represented in the number 3"):
            expect(dumps(SecurityLevel.GUEST)).to(equal("3"))

    with context("when the level UNKNOWN is serialized"):
        with it("should have be represented in the number 1"):
            expect(dumps(SecurityLevel.UNKNOWN)).to(equal("1"))

    with context("when you a Security Level to something else with >"):
        with it("should return NotImplemented"):
            expect(lambda: SecurityLevel.OWNER > "some string").to(raise_error(TypeError))
