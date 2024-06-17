import os
from pathlib import Path

import pytest
from eitprocessing.datahandling.loading import load_eit_data

environment = os.environ.get(
    "TEST_DATA",
    Path.resolve(Path(__file__).parent.parent),
)

data_directory = Path(environment) / "tests" / "test_data"
data_path = Path(data_directory) / "Draeger_Test3.bin"


@pytest.fixture(scope="session")
def file_data():
    return load_eit_data(
        data_path,
        vendor="draeger",
        label="selected data",
    )
