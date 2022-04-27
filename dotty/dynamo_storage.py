from boto3 import client, resource


class DynamoStorage:
    def __init__(self):
        self._dyn_db_resource = resource("dynamodb")
        self._dyn_db_client = client("dynamodb")

    def _table_exists(self, table_name: str) -> bool:
        existing_tables = self._dyn_db_client.list_tables()["TableNames"]
        return table_name in existing_tables

    def _get_table(self, table_name: str):
        return self._dyn_db_resource.Table(table_name)

    def _check_for_gsi(self, table, gsi_name: str):
        return table.global_secondary_indexes or gsi_name not in [gsi["IndexName"] for gsi in table.global_secondary_indexes]
