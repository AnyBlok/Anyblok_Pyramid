# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.


def group_finder(userid, request):
    """Return groups from user ID

    :param userid: the user id (login)
    :param request: request from pyramid
    """
    if hasattr(request, 'anyblok') and request.anyblok:
        return request.anyblok.registry.User.get_groups(userid)

    return userid


def check_user(userid, password, request):
    """Return groups from user ID

    :param userid: the user id (login)
    :param request: request from pyramid
    """
    if hasattr(request, 'anyblok') and request.anyblok:
        return request.anyblok.registry.User.check_login(
            login=userid, password=password
        )

    return None
