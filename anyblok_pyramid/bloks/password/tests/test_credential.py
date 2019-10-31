# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from pyramid.httpexceptions import HTTPUnauthorized


@pytest.mark.usefixtures('registry_password')
class TestCredential:

    def init_user(self, registry):
        self.User = registry.User
        self.CredentialStore = registry.User.CredentialStore
        self.User.insert(login='user.1')
        self.CredentialStore.insert(login='user.1', password="P1")

    def test_check_login_ok(self, registry_password):
        self.init_user(registry_password)
        assert self.User.check_login(login="user.1", password="P1") == 'user.1'

    def test_check_login_ko(self, registry_password):
        self.init_user(registry_password)
        with pytest.raises(HTTPUnauthorized):
            self.User.check_login(login="user.1", password="P2")
