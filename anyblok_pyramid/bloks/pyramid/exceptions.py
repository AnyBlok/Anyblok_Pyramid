# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.controllers import PyramidException


class PyramidInvalidFunction(PyramidException):
    """ Sub class of Pyramid Exception """


class PyramidInvalidView(PyramidException):
    """ Sub class of Pyramid Exception """


class PyramidInvalidMethod(PyramidException):
    """ Sub class of Pyramid Exception """


class PyramidInvalidProperty(PyramidException):
    """ Sub class of Pyramid Exception """
