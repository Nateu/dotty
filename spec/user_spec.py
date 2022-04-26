from json import dumps

from expects import equal, expect
from mamba import context, describe, it

from dotty.security_level import SecurityLevel
from dotty.user import User


with describe("Given a user pascal with security level OWNER") as self:
    with context("when get_user_identifier is called"):
        with it("should return 'pascal'"):
            my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
            expect(my_user.get_user_identifier()).to(equal("pascal"))

    with context("when get_user_clearance_level is called"):
        with it("should return '9'"):
            my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
            expect(my_user.get_user_clearance_level().value).to(equal(9))

    with context("when set_security_level is called with a SecurityLevel"):
        with it("should update the security level to the new setting"):
            my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
            my_user.set_security_level(SecurityLevel.GUEST)
            expect(my_user.get_user_clearance_level().value).to(equal(3))

    with context("when it is serialized"):
        with it("should return a object with identifier = pascal and security level = 9"):
            my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
            expect(dumps(my_user)).to(equal('{"identifier": "pascal", "security level": 9}'))

# with describe("Given ") as self:
#     with context("when get_user_identifier is called"):
#         with it("should return 'pascal'"):
#             my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
#             expect(my_user.get_user_identifier()).to(equal("pascal"))
