import pytest
from anyblok.tests.conftest import *  # noqa
from anyblok_pyramid.conftest import *  # noqa
from anyblok.tests.conftest import init_registry_with_bloks


@pytest.fixture(scope="function")
def registry_identity(request, testbloks_loaded):
    registry = init_registry_with_bloks(['user-identity'], None)
    request.addfinalizer(registry.close)
    return registry
