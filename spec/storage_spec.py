from unittest.mock import Mock, mock_open, patch

from expects import equal, expect
from mamba import context, describe, it

from dotty.storage import Storage


with describe("Given a Storage solution") as self:
    with context("when data and storage is provided"):
        with it("should store the data in the storage"):
            with patch(
                "builtins.open",
                new=mock_open(read_data='[{"name": "A", "score": 5, "comment": "T"}, {"name": "B", "score": 7, "comment": "T"}]'),
            ) as mocked_open:
                Storage().store_in(data="[{'some': 'data'}]", storage_name="my_storage.json")
            mocked_open.return_value.write.assert_called_once_with("[{'some': 'data'}]")

    with context("when a storage is provided"):
        with it("should retrieve the data contained within"):
            with patch("builtins.open", new=mock_open(read_data="[{'some': 'data'}]")) as mocked_open:
                data = Storage().retrieve_data(storage_name="my_storage.json")
            expect(data).to(equal("[{'some': 'data'}]"))

    with context("when a non existing storage is provided"):
        with it("should return nothing"):
            with patch(
                "builtins.open",
                new=Mock(side_effect=FileNotFoundError()),
            ) as mocked_open:
                Storage().retrieve_data("my_storage.json")
            expect(isinstance(mocked_open.side_effect, FileNotFoundError)).to(equal(True))
