# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest


@pytest.mark.usefixtures('registry_identity')
class TestUserIdentity:

    def test_user_identity(self, registry_identity):

        registry = registry_identity

        user = registry.User.insert(
            login="johnny_dowey", first_name="John", last_name="Doe")

        assert user.name == "John DOE"
