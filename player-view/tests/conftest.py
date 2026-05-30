import pytest
from pathlib import Path

from player_view.models.voice_profile import ProfileStore


@pytest.fixture
def tmp_profile_dir(tmp_path):
    return tmp_path / 'profiles'


@pytest.fixture
def profile_store(tmp_profile_dir):
    return ProfileStore(tmp_profile_dir)
