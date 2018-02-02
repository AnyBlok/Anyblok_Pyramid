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


User = Declarations.Model.User


@Declarations.register(User)
class Role:

    name = String(primary_key=True, nullable=False)
    label = String(nullable=False)
    children = Many2Many(model='Model.User.Role', many2many="parents")
    users = Many2Many(model=User, many2many="roles")
    roles_name = Function(fget="get_all_roles_name")

    def get_all_roles_name(self):
        names = [self.name]
        for child in self.children:
            if child.name in names:
                continue

            names.extend(child.roles_name)

        return list(set(names))

    @classmethod
    def before_update_orm_event(cls, mapper, connection, target):
        try:
            target.get_all_roles_name()
        except MainException:
            raise RecursionRoleError()
