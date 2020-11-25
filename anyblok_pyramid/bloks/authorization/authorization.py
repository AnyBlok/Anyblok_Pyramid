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
    def ensure_authorizations_exists(
        cls, role, model, authorizatoions
    ):
        """Ensure role's models authorizations are present in an
        idempotent way
        """
        if not authorizatoions:
            authorizatoions = {}
        authz = (
            cls.registry.Pyramid.Authorization.query()
            .filter_by(
                role=role,
                model=model,
            )
            .one_or_none()
        )
        if not authz:
            authz = cls.registry.Pyramid.Authorization.insert(
                role=role,
                model=model,
            )
        authz.update(
            perms=authorizatoions.get("perms", {}),
            manual=False,
            **authorizatoions.get("extra_authz_params", {})
        )
        authz.flag_modified("perms")
        return authz


@Declarations.register(Pyramid)
class Role:

    @classmethod
    def ensure_role_exists(
        cls, name, config, label=None
    ):
        """Create or update Pyramid.Role with related model's authorization
        in an idempotent way.

        :param name: str, Role name
        :param config: dict, per model authorizations configuration likes::

            {
                "Model.Test": {
                    perms: {
                        "create": {"matched": True},
                        "read": {"matched": True},
                        "update": {"matched": True},
                        "delete": {"matched": True}
                        "whatever you needs": {"matched": True}
                    },
                    extra_authz_params: {
                        "order": 100,
                    }
                }
            }

        As a convention we suggest to provid a class method to return
        this configuration that let other blok to easly improuve roles.


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

        for model, authz in config.items():
            Pyramid.Authorization.ensure_authorizations_exists(
                role, model, authz
            )
        Pyramid.Authorization.query().filter_by(role=role).filter(
            ~Pyramid.Authorization.model.in_(config.keys())
        ).delete(synchronize_session="fetch")
        return role


@Declarations.register(Pyramid.Authorization)
class Configuration:
    """Utility class in order to easly manage role and authorizatoin
    setups.

    As a convention we add class method that configure  role's  models
    authorizations. This aims to let other Bloks to improve roles by adding
    or complete models authorizations. For instance if a Blok `A` define a
    role ``role_a`` that give read only access on ``Model.System.Blok``
    and write access to ``Model.Pyramid.User``::

        from anyblok import Declarations

        Pyramid = Declarations.Model.Pyramid

        @Declarations.register(Pyramid.Authorization)
        class Configuration:

            @classmethod
            def setup_authorization(cls):
                super().setup_authorization()
                cls.registry.Pyramid.Role.ensure_role_exists(
                    "role_a",
                    cls.get_role_A_models_authorization(),
                    label= "Role A"
                )


            @classmethod
            def get_role_A_models_authorization(cls):
                return {
                    "Model.Pyramid.User": cls.ACCESS_WRITE,
                    "Model.System.Blok": cls.ACCESS_READ,
                }


    An other blok `B` could overload this configuration to gives `install`
    (that would gives access to an exposed method that is allowed
    to install a blok) permission on ``Model.System.Blok`` and add
    read-only access to an other model ``Model.pyramid.Role``. Also it's
    good place if you want to set role inheriance, in the following example
    a user linked to `role_b` will get `role_a`'s permissions::

        from anyblok import Declarations
        from anyblok_pyramid import merge

        Pyramid = Declarations.Model.Pyramid


        @Declarations.register(Pyramid.Authorization)
        class Configuration:

            @classmethod
            def setup_authorization(cls):
                super().setup_authorization()
                roleb = cls.registry.Pyramid.Role.ensure_role_exists(
                    "role_b", cls.get_role_B_models_authorization,
                    label= "Administrator"
                )
                rolea = cls.registry.Pyramid.Role.query.get("role_a")
                roleb.children.append(rolea)

            @classmethod
            def get_role_A_models_authorization(cls):
                return merge(
                    super().get_role_A_models_authorization()
                    {
                        "Model.Pyramid.Role": cls.ACCESS_READ,
                        "Model.System.Blok": merge(
                            cls.ACCESS_WRITE,
                            dict(perms=dict(install=dict(matched=True))
                        ),
                    }
                )

            @classmethod
            def get_role_B_models_authorization(cls):
                '''return models authorizations config for role B'''

    """
    ACCESS_CRUD = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=100,
        ),
    )
    ACCESS_CRU_ = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=110,
        ),
    )
    ACCESS_CR_D = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=120,
        ),
    )
    ACCESS__RUD = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=130,
        ),
    )
    ACCESS_C_UD = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=140,
        ),
    )
    ACCESS_CR__ = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=150,
        ),
    )
    ACCESS__RU_ = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=160,
        ),
    )
    ACCESS__R_D = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=170,
        ),
    )
    ACCESS___UD = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=180,
        ),
    )
    ACCESS_C_U_ = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=190,
        ),
    )
    ACCESS_C__D = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=200,
        ),
    )
    ACCESS__R__ = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=True,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=210,
        ),
    )
    ACCESS_C___ = dict(
        perms=dict(
            create=dict(
                matched=True,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=220,
        ),
    )
    ACCESS___U_ = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=True,
            ),
            delete=dict(
                matched=False,
            ),
        ),
        extra_authz_params=dict(
            order=230,
        ),
    )
    ACCESS____D = dict(
        perms=dict(
            create=dict(
                matched=False,
            ),
            read=dict(
                matched=False,
            ),
            update=dict(
                matched=False,
            ),
            delete=dict(
                matched=True,
            ),
        ),
        extra_authz_params=dict(
            order=240,
        ),
    )

    # alias
    ACCESS_READ = ACCESS__R__
    ACCESS_WRITE = ACCESS_CRUD
    ACCESS_UPDATE = ACCESS__RU_

    @classmethod
    def setup_authorization(cls):
        """A unique entry point that let setup role's  models
        authorizations.

        The intent of this method is to be called from the latest blok update
        method. and over load from bloks that needs to add configurations
        (please read class doctstring).

        .. note::

            Even a dependent blok call it in its update blok method you
            should call this method again in your update blok method because
            the update method is called once blok is installed and before next
            blok to be installed.

            So you should take care to writte idempotent code while
            overloading this method
        """
