# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.conftest import *  # noqa
from anyblok_pyramid.conftest import *  # noqa


@pytest.fixture(scope="function")
def registry_password(request, testbloks_loaded):
    registry = init_registry_with_bloks(['auth-password'], None)
    request.addfinalizer(registry.close)
    return registry
