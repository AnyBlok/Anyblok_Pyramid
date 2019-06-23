# This file is a part of the AnyBlok project
#
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok.conftest import *  # noqa
from .testing import init_web_server


@pytest.fixture(scope="class")
def webserver(request, configuration_loaded):
    return init_web_server()
