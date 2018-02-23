# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer, String, Json
from anyblok.relationship import Many2One
from .exceptions import AuthorizationValidationException
from pyramid.security import Allow, Deny, ALL_PERMISSIONS
from sqlalchemy import or_


User = Declarations.Model.User


@Declarations.register(User)
class Authorization:

    id = Integer(primary_key=True)
    order = Integer(default=100, nullable=False)

    resource = String()
    model = String(
        foreign_key=Declarations.Model.System.Model.use('name').options(
            ondelete="cascade")
    )
    primary_keys = Json(default={})
    filter = Json(default={})

    role = Many2One(
        model=User.Role, foreign_key_options={'ondelete': 'cascade'})
    login = String(foreign_key=User.use('login').options(ondelete="cascade"))
    user = Many2One(model=User)

    perm_create = Json(default={})
    perm_read = Json(default={})
    perm_update = Json(default={})
    perm_delete = Json(default={})

    @classmethod
    def get_acl(cls, login, resource, **params):
        # cache the method
        query = cls.query()
        query = query.filter(
            or_(cls.resource == resource, cls.model == resource))
        # Authorization = cls.registry.User.Authorization
        # return Authorization.get_acl(login, resource, params)
        res = []
        for self in query.all():
            allow_perms = []
            deny_perms = []
            for perm in ('create', 'read', 'update', 'delete'):
                p = getattr(self, 'perm_' + perm)
                ismatched = True
                if 'condition' in p:
                    # TODO
                    pass

                if p.get('matched' if ismatched else 'unmatched') is True:
                    allow_perms.append(perm)
                elif p.get('matched' if ismatched else 'unmatched') is False:
                    deny_perms.append(perm)

            if len(allow_perms):
                res.append((Allow, login, allow_perms))

            if len(deny_perms):
                res.append((Deny, login, deny_perms))

        res.append((Deny, login, ALL_PERMISSIONS))
        return res

    @classmethod
    def before_insert_orm_event(cls, mapper, connection, target):
        target.check_validity()

    @classmethod
    def before_update_orm_event(cls, mapper, connection, target):
        target.check_validity()

    def check_validity(self):
        if not (self.role or self.login or self.user):
            raise AuthorizationValidationException(
                "No role and login to apply in the authorization (%s)" % self)

        if not (self.resource or self.model):
            raise AuthorizationValidationException(
                "No resource and model to apply in the authorization (%s)" %
                self)

        if not self.model and self.primary_keys:
            raise AuthorizationValidationException(
                "Primary keys without model to apply in the authorization "
                "(%s)" % self)
