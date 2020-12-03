# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from anyblok.column import Integer, String, Json
from anyblok.relationship import Many2One
from anyblok.field import JsonRelated
from .exceptions import AuthorizationValidationException
from pyramid.security import Allow, Deny, ALL_PERMISSIONS
from sqlalchemy import or_


Pyramid = Declarations.Model.Pyramid


@Declarations.register(Pyramid)
class Authorization:
    """A model to store autorization rules (permissions for users against an
    Anyblok model or a Pyramid resource)"""

    id = Integer(primary_key=True)
    code = String(nullable=True, unique=True, size=256)
    order = Integer(default=100, nullable=False)

    resource = String()
    model = String(
        foreign_key=Declarations.Model.System.Model.use('name').options(
            ondelete="cascade"),
        size=256,
    )
    primary_keys = Json(default={})
    filter = Json(default={})  # next step

    role = Many2One(
        model=Pyramid.Role, foreign_key_options={'ondelete': 'cascade'})
    login = String(
        foreign_key=Pyramid.User.use('login').options(ondelete="cascade"))
    user = Many2One(model=Pyramid.User)
    perms = Json(default={})

    perm_create = JsonRelated(json_column='perms', keys=['create'])
    perm_read = JsonRelated(json_column='perms', keys=['read'])
    perm_update = JsonRelated(json_column='perms', keys=['update'])
    perm_delete = JsonRelated(json_column='perms', keys=['delete'])

    @classmethod
    def get_acl_filter_model(cls):
        """Return the Model to use to check the permission"""
        return {
            'User': cls.registry.Pyramid.User,
            'Role': cls.registry.Pyramid.Role,
        }

    @classmethod
    def get_acl(cls, login, resource, params=None):
        """Return the Pyramid ACL in function of the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        """
        # cache the method
        User = cls.registry.Pyramid.User
        Role = cls.registry.Pyramid.Role

        query = cls.query()
        query = query.filter(
            or_(cls.resource == resource, cls.model == resource))
        query = query.order_by(cls.order)
        Q1 = query.filter(cls.login == login)
        Q2 = query.join(cls.role).filter(Role.name.in_(User.get_roles(login)))
        res = []
        for query in (Q1, Q2):
            for self in query.all():
                allow_perms = []
                deny_perms = []
                perms = list((self.perms or {}).keys())
                perms.sort()
                for perm in perms:
                    p = self.perms[perm]
                    query = User.query()
                    query = query.filter(User.login == login)
                    query = query.join(User.roles)
                    if self.filter:
                        query = query.condition_filter(
                            self.filter,
                            cls.get_acl_filter_model()
                        )

                    if 'condition' in p:
                        query = query.condition_filter(
                            p['condition'],
                            cls.get_acl_filter_model()
                        )

                    ismatched = True if query.count() else False
                    if p.get('matched' if ismatched else 'unmatched') is True:
                        allow_perms.append(perm)
                    elif (
                        p.get('matched' if ismatched else 'unmatched') is False
                    ):
                        deny_perms.append(perm)

                if len(allow_perms):
                    res.append((Allow, login, allow_perms))

                if len(deny_perms):
                    res.append((Deny, login, deny_perms))

        res.append((Deny, login, ALL_PERMISSIONS))
        return res

    @classmethod
    def check_acl(cls, login, resource, type_):
        """Return the Pyramid ACL in function of the resource and user

        :param login: str, login of the user
        :param resource: str, name of the resource
        :param type: str, name of the action
        """
        # cache the method
        User = cls.registry.Pyramid.User
        Role = cls.registry.Pyramid.Role

        query = cls.query()
        query = query.filter(
            or_(cls.resource == resource, cls.model == resource))
        query = query.order_by(cls.order)
        Q1 = query.filter(cls.login == login)
        Q2 = query.join(cls.role).filter(Role.name.in_(User.get_roles(login)))
        for query in (Q1, Q2):
            for self in query.all():
                perms = list((self.perms or {}).keys())
                if type_ not in perms:
                    continue

                p = self.perms[type_]
                query = User.query()
                query = query.filter(User.login == login)
                query = query.join(User.roles, isouter=True)
                if self.filter:
                    query = query.condition_filter(
                        self.filter,
                        cls.get_acl_filter_model()
                    )

                if 'condition' in p:
                    query = query.condition_filter(
                        p['condition'],
                        cls.get_acl_filter_model()
                    )

                ismatched = True if query.count() else False
                if p.get('matched' if ismatched else 'unmatched') is True:
                    return True
                elif (
                    p.get('matched' if ismatched else 'unmatched') is False
                ):
                    return False

        return False

    @classmethod
    def before_insert_orm_event(cls, mapper, connection, target):
        target.check_validity()

    @classmethod
    def before_update_orm_event(cls, mapper, connection, target):
        target.check_validity()

    def check_validity(self):
        """When creating or updating a User.Authorization, check that all rules
        objects exists or return an AuthorizationValidationException

        :exception: AuthorizationValidationException
        """
        if not (self.role or self.login or self.user or self.role_name):
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

    @classmethod
    def ensure_exists(
        cls, code, **kwargs
    ):
        """Ensure role's authorization is present

        :param code: String, authorization code.
        :param kwargs: authorization fields
        """
        if not kwargs:
            kwargs = {}
        # pv: at some point adding index on this criteria may boost things
        # while setting authorizations
        authz = (
            cls.registry.Pyramid.Authorization.query()
            .filter_by(
                code=code,
            )
            .one_or_none()
        )
        if not authz:
            authz = cls.registry.Pyramid.Authorization.insert(
                code=code, **kwargs
            )
        else:
            authz.update(**kwargs)
            jsonfields = {"perms", "primary_keys", "filter"}
            perms_related = {
                "perm_create",
                "perm_read",
                "perm_update",
                "perm_delete"
            }

            modified = (jsonfields | perms_related) & set(kwargs.keys())
            if modified:
                if perms_related & modified:
                    modified = modified | {"perms"}
                authz.flag_modified(*(jsonfields & modified))
        return authz


@Declarations.register(Pyramid)
class Role:

    @classmethod
    def ensure_exists(
        cls, name, authorizations, label=None
    ):
        """Create or update Pyramid.Role with related model's authorization.

        :param name: str, Role name
        :param authorizations: list, `Model.Pyramid.Authorization` data to
            ensure that it exists::

            [
                {
                    # if code is not provide it will raise an exception
                    "code": "Uniq auth code by role",
                    "model": "Model.Test",
                    "perms": merge(
                        PERM_WRITE,
                        "whatever you needs": {"matched": True}
                    },
                    "order": 100,
                    # Any other values present on Model.Pyramid.Authorization
                },
                {
                    # if code is not provide it will raise an exception
                    "code": "Uniq auth code by role",
                    "resource": "a resource",
                    "perms": {
                        "hack_resource": {"matched": True},
                    },
                },
                ...
            ]

        :param label: str, Role label used if role doesn't exits on insert.
                      default: capitalized name.
        :return: Created or updated role
        """
        Pyramid = cls.registry.Pyramid
        role = Pyramid.Role.query().get(name)
        if not role:
            if not label:
                label = name.capitalize()
            role = Pyramid.Role.insert(name=name, label=label)

        for authz in authorizations:
            code = authz.pop("code", None)
            if code is None:
                raise KeyError(
                    f"Missing `code` information to ensure "
                    f"Model.Pyramid.Authorizatoin is present on role "
                    f"{role.name}"
                )
            Pyramid.Authorization.ensure_exists(
                code, role=role, **authz
            )
        return role
