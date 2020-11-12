# This file is a part of the AnyBlok project
#
#    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import json
import pytest
from anyblok.config import Configuration
from unittest import mock
from anyblok_pyramid.bloks.pyramid import oidc
from urllib.parse import urlparse, parse_qs


class MockJsonResponse:

    headers = {"content-type": "application/json"}

    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    @property
    def text(self):
        return json.dumps(self.data)


def mock_request(method=None, url=None, *args, **kwargs):
    if url == "http://fake/.well-known/openid-configuration":
        return MockJsonResponse(
            {
                "issuer": "http://fake",
                "authorization_endpoint": "http://fake/oauth/authorize",
                "token_endpoint": "http://fake/oauth/token",
                "revocation_endpoint": "https://fake/oauth/revoke",
                "introspection_endpoint": "https://fake/oauth/introspect",
                "userinfo_endpoint": "https://fake/oauth/userinfo",
                "jwks_uri": "https://fake/oauth/discovery/keys",
                "scopes_supported": ["openid", "profile", "email"],
                "response_types_supported": ["code", "token"],
                "response_modes_supported": ["query", "fragment"],
                "token_endpoint_auth_methods_supported": [
                    "client_secret_basic",
                    "client_secret_post",
                ],
                "subject_types_supported": ["public"],
                "id_token_signing_alg_values_supported": ["RS256"],
                "claim_types_supported": ["normal"],
                "claims_supported": ["name", "email", "profile"],
            },
            200,
        )
    elif url == "http://fake/oauth/token":
        qs = parse_qs(kwargs["data"])
        assert qs["redirect_uri"][0] == "http://localhost/oidc_callback"
        return MockJsonResponse(
            {
                "access_token": "a_test_token"
                if qs["code"][0] == "a-fake-code"
                else "other_token",
                "token_type": "token",
                "scope": ["openid email"],
                "state": qs["state"][0],
                "expires_in": 0,
                "refresh_token": "",
            },
            200,
        )
    elif url == "https://fake/oauth/userinfo":
        qs = parse_qs(kwargs["data"])
        if qs["access_token"][0] == "a_test_token":
            return MockJsonResponse(
                {"custom_userinfo_field": "user@anyblok.org"}, 200
            )
        else:
            return MockJsonResponse(
                {"custom_userinfo_field": "unkwnon_user@anyblok.org"}, 200
            )
    else:
        raise Exception("Unexpected url: {}".format(url))


class TestPyramidBlokBase:
    @pytest.fixture(autouse=True)
    def transact(self, request, registry_testblok, webserver):
        transaction = registry_testblok.begin_nested()

        def try_rollback(*args, **kwargs):
            """Wrap rollback to be silent in case where transaction is
            expectedly already rollback"""

            try:
                transaction.rollback(*args, **kwargs)
            except Exception:
                # if transaction is already rollback do not raise exceptions
                pass

        request.addfinalizer(try_rollback)

    @pytest.fixture(autouse=True)
    def reset_webserver(self, request, registry_testblok, webserver):
        def clear_auth():
            webserver.reset()

        request.addfinalizer(clear_auth)
        return


class TestPyramidBlok(TestPyramidBlokBase):
    def test_current_blok(self, registry_testblok, webserver):
        registry = registry_testblok
        webserver.get("/hello/JS/", status=404)
        registry.upgrade(install=("test-pyramid1",))
        resp = webserver.get("/hello/JS/", status=200)
        assert resp.body.decode("utf8") == "Hello JS !!!"

    def test_simple_crud_security(self, registry_testblok, webserver):
        registry = registry_testblok
        registry.upgrade(install=("test-pyramid2",))
        webserver.get("/bloks", status=403)
        webserver.get("/blok/auth", status=403)
        resp = webserver.post_json(
            "/login", {"login": "viewer", "password": ""}, status=302
        )
        headers = resp.headers
        webserver.get("/bloks", status=200, headers=headers)
        webserver.get("/blok/auth", status=200, headers=headers)
        webserver.put("/blok/auth", {}, status=403, headers=headers)
        resp = webserver.post("/logout", {}, status=302)
        headers = resp.headers
        webserver.get("/bloks", status=403, headers=headers)
        webserver.get("/blok/auth", status=403, headers=headers)
        resp = webserver.post_json(
            "/login", {"login": "admin", "password": ""}, status=302
        )
        headers = resp.headers
        webserver.get("/bloks", status=200, headers=headers)
        webserver.get("/blok/auth", status=200, headers=headers)
        webserver.put("/blok/auth", {}, status=200, headers=headers)

    def test_no_issuer(self, registry_testblok, webserver):
        self.assert_missing_config(registry_testblok, "oidc_provider_issuer")

    def assert_missing_config(self, registry, config):
        registry.upgrade(install=("test-pyramid2",))
        with pytest.raises(ValueError) as ex:
            oidc.get_client()
        assert config in str(
            ex.value
        ), "if no oidc provider issuer is set an exception must raises"

    def test_no_client_id(self, registry_testblok, webserver):
        Configuration.set("oidc_provider_issuer", "http://fake")
        self.assert_missing_config(
            registry_testblok, "oidc_relying_party_client_id"
        )

    def test_no_secret_id(self, registry_testblok, webserver):
        Configuration.set("oidc_provider_issuer", "http://fake")
        Configuration.set("oidc_relying_party_client_id", "abc")
        self.assert_missing_config(
            registry_testblok, "oidc_relying_party_secret_id"
        )

    def test_no_rp_callback(self, registry_testblok, webserver):
        Configuration.set("oidc_provider_issuer", "http://fake")
        Configuration.set("oidc_relying_party_client_id", "abc")
        Configuration.set("oidc_relying_party_secret_id", "efg")
        self.assert_missing_config(
            registry_testblok, "oidc_relying_party_callback"
        )

    def oidc_common(self, registry, webserver):
        Configuration.set("oidc_provider_issuer", "http://fake")
        Configuration.set("oidc_relying_party_client_id", "test_client_id")
        Configuration.set("oidc_relying_party_secret_id", "test_secret_id")
        Configuration.set(
            "oidc_relying_party_callback", "http://localhost/oidc_callback"
        )
        SCOPE = "test1,test2"
        Configuration.set("oidc_scope", SCOPE)
        Configuration.set("oidc_userinfo_field", "custom_userinfo_field")
        registry.upgrade(install=("test-pyramid2",))
        resp = webserver.get("/bloks", status=403)
        webserver.get("/blok/auth", status=403)
        resp = webserver.get("/oidc_login", status=302)
        url = urlparse(resp.headers.get("Location"))
        qs = parse_qs(url.query, strict_parsing=True)
        assert url.hostname == "fake"
        assert url.path == "/oauth/authorize"
        assert qs["client_id"][0] == "test_client_id"
        assert qs["response_type"][0] == "code"
        assert qs["scope"][0] == SCOPE.replace(",", " ")
        assert qs["redirect_uri"][0] == "http://localhost/oidc_callback"
        assert qs["state"][0]
        assert qs["nonce"][0]
        return qs

    @mock.patch("requests.request", side_effect=mock_request)
    def test_oidc_auth(self, mock_oidc, registry_testblok, webserver):
        qs = self.oidc_common(registry_testblok, webserver)
        # user is redirect to OIDC provider in order to do the authentication
        # he comes back to the oidc_callback uri with a code and the current
        # state
        curerent_cookie = webserver.cookies["None"]
        webserver.get(
            "/oidc_callback?code=a-fake-code&state={}".format(qs["state"][0]),
            status=302,
        )
        assert webserver.cookies["None"] != curerent_cookie
        webserver.get("/bloks", status=200)

    @mock.patch("requests.request", side_effect=mock_request)
    def test_unkown_user_oidc_auth(
        self, mock_oidc, registry_testblok, webserver
    ):
        qs = self.oidc_common(registry_testblok, webserver)
        curerent_cookie = webserver.cookies["None"]
        webserver.get(
            "/oidc_callback?code=another-fake-code&state={}".format(
                qs["state"][0]
            ),
            status=401,
        )
        assert webserver.cookies["None"] == curerent_cookie
        webserver.get("/bloks", status=403)


class TestPyramidBlokRestrictQueryByUserId(TestPyramidBlokBase):
    def test_restrict_query_by_user_not_restricted(
        self, registry_testblok, webserver
    ):
        registry = registry_testblok
        registry.upgrade(install=("test-pyramid2",))
        resp = webserver.post_json(
            "/login", {"login": "viewer", "password": ""}, status=302
        )
        headers = resp.headers
        results = webserver.get("/bloks", status=200, headers=headers)
        assert len(results.json) > 1

    def test_restrict_query_by_user_restricted(
        self, registry_testblok, webserver
    ):
        registry = registry_testblok
        registry.upgrade(install=("test-pyramid2",))
        resp = webserver.post_json(
            "/login", {"login": "user2@anyblok.org", "password": ""}, status=302
        )
        headers = resp.headers
        results = webserver.get("/bloks", status=200, headers=headers)
        assert len(results.json) == 1
