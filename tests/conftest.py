import pytest
from unittest.mock import patch


@pytest.fixture
def file_path(faker):
    return faker.file_path()


@pytest.fixture
def os_path_exists_mock():
    with patch('os.path.exists') as mock:
        yield mock


@pytest.fixture
def os_remove_mock():
    with patch('os.remove') as mock:
        yield mock


@pytest.fixture
def youtube_mock():
    with patch('youtube.downloader.YouTube') as mock:
        yield mock
