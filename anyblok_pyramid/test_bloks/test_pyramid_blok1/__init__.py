# This file is a part of the AnyBlok project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok


class TestPyramidBlok(Blok):

    version = '1.0.0'

    @classmethod
    def pyramid_load_config(cls, config):
        config.add_route('hello', '/hello/{name}/')
        config.scan(cls.__module__ + '.views')
