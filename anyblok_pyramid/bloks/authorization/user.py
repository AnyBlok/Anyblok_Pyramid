# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations


@Declarations.register(Declarations.Model)
class User:

    @classmethod
    def get_acl(cls, login, resource, params):
        """Overwrite the method to return the ACL for the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        """
        Authorization = cls.registry.User.Authorization
        return Authorization.get_acl(login, resource, params)
