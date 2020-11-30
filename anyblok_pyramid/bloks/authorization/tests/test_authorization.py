# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok_pyramid import merge, PERM_READ, PERM_WRITE
from sqlalchemy.orm.exc import MultipleResultsFound


@pytest.mark.usefixtures("rollback_registry")
class TestAuthorization:
    @pytest.fixture(scope="function", autouse=True)
    def setUp(self, rollback_registry):
        self.registry = rollback_registry
        self.Authorization = self.registry.Pyramid.Authorization

    def assert_authz(self):
        test = self.registry.Pyramid.Role.query().get("test")
        assert test is not None
        assert test.label == "Test"
        assert self.Authorization.query().filter_by(role=test).count() == 2
        authz_blok = (
            self.Authorization.query()
            .filter_by(role=test, model="Model.System.Blok")
            .one()
        )
        assert authz_blok.order == 4
        assert authz_blok.perm_create is None
        assert authz_blok.perm_read == {"matched": True}
        assert authz_blok.perm_update is None
        assert authz_blok.perm_delete is None
        assert authz_blok.perms["custom_perm"] == {"matched": True}
        authz_user = (
            self.Authorization.query()
            .filter_by(role=test, model="Model.Pyramid.User")
            .one()
        )
        assert authz_user.perms == {
            "create": {"matched": True},
            "read": {"matched": True},
            "update": {"matched": True},
            "delete": {"matched": True},
        }

    def test_ensure_role_without_code(self):
        self.registry.Pyramid.User.insert(login="test")
        self.Authorization.ensure_exists(
            None, resource="test", login="test"
        )
        self.Authorization.insert(resource="test 2", login="test")
        with pytest.raises(MultipleResultsFound):
            self.Authorization.ensure_exists(
                None, resource="test", login="test"
            )

    def test_no_code_provide(self):
        with pytest.raises(KeyError) as err:
            self.registry.Pyramid.Role.ensure_exists(
                "test",
                [
                    {
                        "code": "test-blok-read",
                        "model": "Model.System.Blok",
                        "perms": merge(
                            PERM_READ, {"custom_perm": {"matched": True}}
                        ),
                        "order": 4,
                    },
                    {
                        "model": "Model.Pyramid.User",
                        "perms": PERM_WRITE,
                    },
                ],
                label="Test",
            )
        assert (
            "'Missing `code` information to ensure "
            "Model.Pyramid.Authorizatoin is present on role "
            "test'"
        ) == str(err.value)

    def test_ensure_role_insert(self):
        assert self.registry.Pyramid.Role.query().get("test") is None
        self.registry.Pyramid.Role.ensure_exists(
            "test",
            [
                {
                    "code": "test-blok-read",
                    "model": "Model.System.Blok",
                    "perms": merge(
                        PERM_READ, {"custom_perm": {"matched": True}}
                    ),
                    "order": 4,
                },
                {
                    "code": "test-user-write",
                    "model": "Model.Pyramid.User",
                    "perms": PERM_WRITE,
                },
            ],
            label="Test",
        )
        self.assert_authz()

    def test_update(self):
        count_before = self.Authorization.query().count()
        self.registry.Pyramid.Role.ensure_exists(
            "test",
            [
                {
                    "code": "test-blok-read",
                    "model": "Model.System.Blok",
                    "perms": merge(
                        PERM_WRITE, {"custom_perm": {"matched": True}}
                    ),
                    "order": 4,
                },
                {
                    "code": "test-user-write",
                    "model": "Model.Pyramid.User",
                    "perms": PERM_WRITE,
                },
            ],
        )
        assert self.Authorization.query().count() == count_before + 2
        self.registry.Pyramid.Role.ensure_exists(
            "test",
            [
                {
                    "code": "test-blok-read",
                    "model": "Model.System.Blok",
                    "perms": merge(
                        PERM_READ, {"custom_perm": {"matched": True}}
                    ),
                    "order": 4,
                },
            ],
        )
        assert self.Authorization.query().count() == count_before + 2
        self.assert_authz()

    def test_update2(self):
        self.registry.Pyramid.Role.ensure_exists(
            "test",
            [
                {
                    "code": "test-blok-read",
                    "model": "Model.System.Blok",
                    "perms": merge(
                        PERM_READ, {"custom_perm": {"matched": True}}
                    ),
                    "order": 4,
                },
                {
                    "code": "test-user-write",
                    "model": "Model.Pyramid.User",
                    "perms": PERM_READ,
                },
            ],
        )
        self.registry.Pyramid.Role.ensure_exists(
            "test",
            [
                {
                    "code": "test-user-write",
                    "model": "Model.Pyramid.User",
                    "perm_create": {"matched": True},
                    "perm_update": {"matched": True},
                    "perm_delete": {"matched": True},
                }
            ],
        )
        self.assert_authz()
