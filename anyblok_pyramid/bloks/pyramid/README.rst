.. This file is a part of the AnyBlok / Pyramid project
..
..    Copyright (C) 2020 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.


Pyramid Blok
============

OpenID Connect
--------------

This blok provide an integration with `oic <https://pypi.org/project/oic/>`_
an `OpenID Connect <https://openid.net/specs/openid-connect-core-1_0.htm>`_
library, to make your service an Relying Party (not a provider).

The `api documentation <#oidc-utility>`_.

Requirements
~~~~~~~~~~~~

* install OIDC's extra requirements::

    pip install anyblok_pyramid[oidc]

* confiugre a server session management (we suggest to use
  `anyblok_pyramid_beaker <https://pypi.org/project/anyblok_pyramid_beaker/>`_


Configuration
~~~~~~~~~~~~~

Following settings are available::

  --oidc-provider-issuer OIDC_PROVIDER_ISSUER
                        he OIDC Provider urls (ie: https://gitlab.com)
  --oidc-relying-party-callback OIDC_RELYING_PARTY_CALLBACK
                        The Relaying Party callback, once the user is
                        authenticate on the OIDC provider he will be redirect
                        to that uri to the RP service (ie:
                        http://localhost:8080/callback). In general this value
                        is also configured in your OIDC provider to avoid
                        redirection issues.
  --oidc-relying-party-client-id OIDC_RELYING_PARTY_CLIENT_ID
                        The client id to authenticate the relying party (this
                        application) to the OIDC provider. This information
                        should be provide by your OIDC provider.
  --oidc-relying-party-secret-id OIDC_RELYING_PARTY_SECRET_ID
                        The secret id to authenticate the relying party (this
                        application) to the OIDC provider. This information
                        should be provide by your OIDC provider.
  --oidc-scope OIDC_SCOPE
                        Specify what access privileges are being requested for
                        Access Tokens. `cf Requesting claims using scope
                        values <https://openid.net/specs/openid-connect-
                        core-1_0.html#ScopeClaims`_. a list of claims
                        usingcoma separator.
  --oidc-userinfo-field OIDC_USERINFO_FIELD
                        Specify which field to use from the response of the
                        OIDC provider `userinfo endpoint
                        <https://openid.net/specs/openid-connect-
                        core-1_0.html#UserInfoResponse>`_. To make sure it's a
                        known user
