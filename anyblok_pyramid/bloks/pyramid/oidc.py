"""This module provide OIDC Relying Party utilities

The service you are developing is the `Relying Party` (RP) in OIDC
terms. This service will delagate the authentication to an OIDC Provider also
called Issuer.

Currently only **Authorization Code Flow** is supported.

According `specifications <https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowSteps>`_

The Authorization Code Flow goes through the following steps::

    * The RP prepares an Authentication Request containing the desired request parameters.
    * User is redirect to the the Authorization Server (OIDC Provider/ Issuer).
    * Authorization Server Authenticates the End-User.
    * Authorization Server obtains End-User Consent/Authorization.
    * Authorization Server sends the End-User back to the RP with an Authorization Code.
    * RP requests a response using the Authorization Code at the Token Endpoint (OIDC Provider/ Issuer).
    * RP receives a response that contains an ID Token and Access Token in the response body.
    * RP validates the ID token and retrieves the End-User's Subject Identifier.

"""
from functools import lru_cache
from anyblok import Declarations
from anyblok.config import Configuration
from oic import rndstr
from oic.oic import Client
from oic.oic.message import (
    AccessTokenResponse,
    AuthorizationResponse,
    RegistrationResponse,
)
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember


@Declarations.register(Declarations.Model)
class Pyramid:

    @classmethod
    @lru_cache(maxsize=512)
    def oidc_get_client(cls):
        """Method that prepare the oidc client.

        This method use lru_cache in order call the OIDC provider once per thread

        Today we only support OIDC providers (ISSUER) that expose a
        /.well-known/openid-configuration route

        At the moment to authenticate the RP to the OIDC provider we only support
        through client_id/secret_ID/rp_callback attributes. 

        You must configure OIDC in AnyBlok configuration:

        * **oidc-provider-issuer**: The OIDC Provider urls (ie: https://gitlab.com)
        * **oidc-relying-party-callback**: The Relaying Party callback, once the user is authenticate
        on the OIDC provider he will be redirect to that uri to the RP service
        (ie: http://localhost:8080/callback). In general this value is also
        configured in your OIDC provider to avoid redirection issues.
        * **oidc-relying-party-client-id**: The client id provide by your OIDC provider
        * **oidc-relying-party-secret-id**: The secret id provide by your OIDC provider
        """

        client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
        provider_info = client.provider_config(
            Configuration.get("oidc_provider_issuer")
        )
        info = {
            "client_id": Configuration.get("oidc_relying_party_client_id"),
            "client_secret": Configuration.get("oidc_relying_party_secret_id"),
            "redirect_uris": [Configuration.get("oidc_relying_party_callback")],
        }
        info.update(provider_info._dict)
        client_reg = RegistrationResponse(**info)

        client.store_registration_info(client_reg)
        return client

    @classmethod
    def oidc_prepare_auth_url(cls, request):
        """Prepare redirect uri to the OIDC provider
        
        You may use it likes this (using cornice)::


            from cornice import Service
            from pyramid.httpexceptions import HTTPFound

            login_route = Service(
                name='login',
                path='/login',
                installed_blok=current_blok()n
            )

            @login_route.get()
            def login(request):
                HTTPFound(
                    location=request.anyblok.registry.Pyramid.oidc_prepare_auth_url(request)
                )

        """
        # s'assurer que request.session est présent quelque soit le mécanisme de
        # session avec pyramid il doit implémenter Idict
        if not getattr(request, "session", None):
            raise RuntimeError(
                "In order to use OIDC Relaying party utility, you must configure a Pyramid"
                "session object https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/sessions.html"
            )
        client = cls.oidc_get_client()
        request.session.update(
            {"oic_state": rndstr(),}
        )

        args = {
            "client_id": client.client_id,
            "response_type": "code",
            # TODO: make scope configurable
            "scope": ["openid", "email"],
            # nonce is a string value used to associate a Client session
            # with an ID Token, and to mitigate replay attacks.
            "nonce": rndstr(),
            "redirect_uri": client.registration_response["redirect_uris"][0],
            "state": request.session["oic_state"],
        }
        auth_req = client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request(client.authorization_endpoint)
        return login_url

    @classmethod
    def oidc_validate_response(cls, response):
        """Make sure response is an instance of an AuthorizationResponse or an ErrorResponse.
        The latter if an error was returned from the OP still is a TODO to implement
        """
        if not isinstance(response, AuthorizationResponse):
            # it should be an ErrorResponse
            raise ValueError(
                "Something goes wrong on the OIDC Provider: {}".format(response)
            )

        return response

    @classmethod
    def oidc_validate_state(cls, request, response):
        """State is generated on the first call before redirection to the OIDC
        provider and must be the same, when user comme back from the OIDC provider.

        It is used to keep track of responses to outstanding requests (state).
        """
        if not response["state"] == request.session["oic_state"]:
            raise ValueError("State must be the same between registration and callback")

    @classmethod
    def oidc_get_access_token(cls, response):
        """Request an access token to retreive user info on OIDC server side
        """
        args = {"code": response["code"]}
        atr = cls.oidc_get_client().do_access_token_request(
            state=response["state"],
            request_args=args,
            authn_method="client_secret_basic",
        )
        if not isinstance(atr, AccessTokenResponse):
            # it should be a TokenErrorResponse
            raise ValueError("OIDC Access token is invalid: {}".format(atr))
        return atr

    @classmethod
    def oidc_get_token(cls, request):
        """Get a token in order to retreive data from the OIDC provider"""
        response = cls.oidc_get_client().parse_response(
            AuthorizationResponse, info=request.query_string, sformat="urlencoded"
        )
        cls.oidc_validate_response(response)
        cls.oidc_validate_state(request, response)
        access_token_response = cls.oidc_get_access_token(response)
        return response, access_token_response

    @classmethod
    def oidc_get_user_info(cls, response):
        """Request to the OIDC provider to get user informations according the
        requested scope"""
        return cls.oidc_get_client().do_user_info_request(state=response["state"])

    @classmethod
    def oidc_log_user(cls, request):
        """Validate OIDC code and request info to validate if user exists

        invalidate current session if Pyramid.check_user_exists doesn't raise
        and return (userinfo, headers)
        """
        response, _ = cls.oidc_get_token(request)
        userinfo = cls.oidc_get_user_info(response)

        # TODO: make this field configurable
        login = userinfo["email"]
        try:
            cls.check_user_exists(login)
        except Exception as e:
            logger.info("Fail check_user_exists: %r", e)
            request.anyblok.registry.rollback()
            request.errors.add("header", "login", "wrong username")
            request.errors.status = 401
            return userinfo, None

        # Renew the Session ID After Privilege Level Change
        # This is fore security reason cf `OWASP cheat sheet <https://cheatsheetseries.owasp.org/
        # cheatsheets/Session_Management_Cheat_Sheet.html
        # #renew-the-session-id-after-any-privilege-level-change`_
        request.session.invalidate()
        return userinfo, remember(request, login)

    @classmethod
    def oidc_login(cls, request):
        """Once OIDC info are retrive, check if users exists according data
        return by the OIDC provider and renew session ID, then redirect
        user to the  Pyramid.User.get_login_location_to definition setting
        session ID cookie"""
        _, headers = cls.oidc_log_user(request)
        location = cls.User.get_login_location_to(login, request)
        return HTTPFound(location=location, headers=headers)
