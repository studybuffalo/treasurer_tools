import pytest

from django.conf import settings

from users.tests.factories import UserDetailsFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir): # pylint: disable=redefined-outer-name
    settings.MEDIA_ROOT = tmpdir.strpath

@pytest.fixture
def user_details():
    return UserDetailsFactory()
