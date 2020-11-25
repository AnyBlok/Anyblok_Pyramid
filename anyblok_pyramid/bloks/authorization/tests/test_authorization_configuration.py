# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from anyblok_pyramid import merge


@pytest.mark.usefixtures("rollback_registry")
class TestSetupACL:
    @pytest.fixture(scope="function", autouse=True)
    def setUp(self, rollback_registry):
        self.registry = rollback_registry
        self.Authorization = self.registry.Pyramid.Authorization
        self.Config = self.Authorization.Configuration

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
        assert authz_blok.perm_create == {"matched": False}
        assert authz_blok.perm_read == {"matched": True}
        assert authz_blok.perm_update == {"matched": False}
        assert authz_blok.perm_delete == {"matched": False}
        assert authz_blok.perms["custom_perm"] == {"matched": True}
        authz_user = (
            self.Authorization.query()
            .filter_by(role=test, model="Model.Pyramid.User")
            .one()
        )
        assert (
            authz_user.order
            == self.Config.ACCESS_WRITE["extra_authz_params"]["order"]
        )
        assert authz_user.perms == {
            "create": {"matched": True},
            "read": {"matched": True},
            "update": {"matched": True},
            "delete": {"matched": True},
        }

    def test_ensure_role_insert(self):
        assert self.registry.Pyramid.Role.query().get("test") is None
        self.registry.Pyramid.Role.ensure_role_exists(
            "test",
            {
                "Model.System.Blok": merge(
                    self.Config.ACCESS_READ,
                    {
                        "perms": {"custom_perm": {"matched": True}},
                        "extra_authz_params": {"order": 4},
                    },
                ),
                "Model.Pyramid.User": self.Config.ACCESS_WRITE,
            },
            label="Test",
        )
        self.assert_authz()

    def test_ensure_remove_authz(self):
        count_before = self.Authorization.query().count()
        self.registry.Pyramid.Role.ensure_role_exists(
            "test",
            {
                "Model.System.Blok": merge(
                    self.Config.ACCESS_READ,
                    {
                        "perms": {"custom_perm": {"matched": True}},
                    },
                ),
                "Model.Pyramid.User": self.Config.ACCESS_WRITE,
                "Model.Pyramid.Role": self.Config.ACCESS_READ,
            },
        )
        assert self.Authorization.query().count() == count_before + 3
        self.registry.Pyramid.Role.ensure_role_exists(
            "test",
            {
                "Model.System.Blok": merge(
                    self.Config.ACCESS_READ,
                    {
                        "perms": {"custom_perm": {"matched": True}},
                        "extra_authz_params": {"order": 4},
                    },
                ),
                "Model.Pyramid.User": self.Config.ACCESS_WRITE,
            },
            label="Test ignored label",
        )
        assert self.Authorization.query().count() == count_before + 2
        self.assert_authz()
