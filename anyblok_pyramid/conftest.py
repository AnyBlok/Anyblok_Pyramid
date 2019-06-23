# This file is a part of the AnyBlok project
#
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok.conftest import *  # noqa
from webtest import TestApp  # noqa
from anyblok_pyramid.pyramid_config import Configurator  # noqa


@pytest.fixture(scope="class")
def webserver(request, init_session):
    config = Configurator()
    config.include_from_entry_point()
    config.load_config_bloks()
    app = config.make_wsgi_app()
    return TestApp(app)