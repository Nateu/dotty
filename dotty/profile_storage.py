from typing import List

from boto3.dynamodb.conditions import Key

from dotty.dynamo_storage import DynamoStorage
from dotty.security_level import SecurityLevel
from dotty.user import User


class ProfileStorage(DynamoStorage):
    def __init__(self):
        super().__init__()
        self._table = self._get_table_profiles()

    def create_owner(self, identifier: str) -> None:
        owners = self._get_owners()
        if not owners or identifier not in [owner["identifier"] for owner in owners["Items"]]:
            self._store_profile(identifier=identifier, security_level=SecurityLevel.OWNER)

    def store_profiles(self, users: List[User]) -> None:
        for user in users:
            self._store_profile(identifier=user.get_user_identifier(), security_level=user.get_user_clearance_level())

    def retrieve_profiles(self) -> List[User]:
        response: List[User] = []
        stored_profiles = self._table.scan(AttributesToGet=["identifier", "security_level"], Limit=100)
        if stored_profiles:
            for profile in stored_profiles["Items"]:
                security_level_value = int(profile["security_level"])
                response.append(User(identifier=profile["identifier"], security_level=SecurityLevel(security_level_value)))
        return response

    def _get_table_profiles(self):
        if self._table_exists(table_name="profiles"):
            profiles_table = self._get_table(table_name="profiles")
            if not self._check_for_gsi(table=profiles_table, gsi_name="gsi_security_level"):
                self._create_profile_gsi_security_level()
            return profiles_table
        else:
            new_table = self._dyn_db_resource.create_table(
                TableName="profiles",
                KeySchema=[
                    {"AttributeName": "identifier", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "identifier", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            new_table.wait_until_exists()
            self._create_profile_gsi_security_level()
            return new_table

    def _create_profile_gsi_security_level(self):
        self._dyn_db_client.update_table(
            TableName="profiles",
            AttributeDefinitions=[
                {"AttributeName": "identifier", "AttributeType": "S"},
                {"AttributeName": "security_level", "AttributeType": "N"},
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    "Create": {
                        "IndexName": "gsi_security_level",
                        "KeySchema": [
                            {"AttributeName": "security_level", "KeyType": "HASH"},
                            {"AttributeName": "identifier", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
                    }
                }
            ],
        )

    def _get_owners(self):
        return self._table.query(IndexName="gsi_security_level", KeyConditionExpression=Key("security_level").eq(9))

    def _store_profile(self, identifier: str, security_level: SecurityLevel) -> None:
        self._table.put_item(
            Item={
                "identifier": identifier,
                "security_level": security_level.value,
            }
        )
