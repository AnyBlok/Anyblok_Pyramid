# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations


@Declarations.register(Declarations.Model.Pyramid)
class User:

    @classmethod
    def get_acl(cls, login, resource, params=None):
        """Overwrite the method to return the ACL for the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        """
        Authorization = cls.registry.Pyramid.Authorization
        return Authorization.get_acl(login, resource, params=params)

    @classmethod
    def check_acl(cls, login, resource, type_):
        """Overwrite the method to return the ACL for the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        :param type: str, name of the action
        """
        Authorization = cls.registry.Pyramid.Authorization
        return Authorization.check_acl(login, resource, type_)
