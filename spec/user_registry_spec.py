from expects import equal, expect
from mamba import before, context, describe, it

from dotty.security_level import SecurityLevel
from dotty.user_registry import UserRegistry
from spec.fakes import FakeProfileStorage


with describe("Given a user registry") as self:
    with context("when you register user"):
        with before.each:
            self.profile_storage = FakeProfileStorage()
            self.user_registry = UserRegistry(profile_storage=self.profile_storage)
            self.user_registry.register_user(identifier="@Pascal", role=SecurityLevel.OWNER)

        with it("should save it in storage"):
            check = "@Pascal" in [profile.get_user_identifier() for profile in self.profile_storage.all_profiles]
            expect(check).to(equal(True))

        with context("and you register the same user again"):
            with it("should save it's new SecurityLevel"):
                self.user_registry.register_user(identifier="@Pascal", role=SecurityLevel.USER)
                check = [
                    profile.get_user_clearance_level()
                    for profile in self.profile_storage.all_profiles
                    if profile.get_user_identifier() == "@Pascal"
                ].pop()
                expect(check).to(equal(SecurityLevel.USER))

        with context("and you request the get_user_listing"):
            with it("should return the users registered and their Security Level"):
                expect(self.user_registry.get_user_listing()).to(equal("@Pascal: OWNER"))
