# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import String
from anyblok.relationship import Many2Many
from anyblok.field import Function
from .exceptions import RecursionRoleError, MainException


Pyramid = Declarations.Model.Pyramid


@Declarations.register(Pyramid)
class Role:
    """Role, allow to group some authorization for an user"""

    name = String(primary_key=True, nullable=False)
    label = String(nullable=False)
    children = Many2Many(model='Model.Pyramid.Role', many2many="parents")
    users = Many2Many(model=Pyramid.User, many2many="roles")
    roles_name = Function(fget="get_all_roles_name")

    def get_all_roles_name(self):
        """Return all the name of the roles self and dependencies
        """
        names = [self.name]
        for child in self.children:
            if child.name in names:
                continue

            names.extend(child.roles_name)

        return list(set(names))

    @classmethod
    def before_update_orm_event(cls, mapper, connection, target):
        """Check if the role has not any cyclical dependencies
        """
        try:
            target.get_all_roles_name()
        except MainException:
            raise RecursionRoleError()
