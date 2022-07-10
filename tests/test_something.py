from dotty.security_level import SecurityLevel
from dotty.user import User


def test_given_user_pascal_security_level_OWNER_when_get_user_identifier_then_it_should_return_pascal():
    my_user = User(identifier="pascal", security_level=SecurityLevel.OWNER)
    assert my_user.get_user_identifier() == "pascal"
