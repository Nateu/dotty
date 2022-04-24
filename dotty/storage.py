from typing import Optional


class Storage:
    def store_in(self, data: str, storage_name: str):
        with open(file=storage_name, mode="w") as file:
            file.write(data)

    def retrieve_data(self, storage_name: str) -> Optional[str]:
        try:
            with open(file=storage_name, mode="r") as file:
                return file.read()
        except FileNotFoundError:
            return
