# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2020 Pierre Verkest <pierreverkest84@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from sqlalchemy.sql.elements import BooleanClauseList

from anyblok.column import String
from anyblok.declarations import Declarations
from anyblok.tests.conftest import init_registry_with_bloks

from anyblok_pyramid.bloks.pyramid.restrict import restrict_query_by_user

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@pytest.fixture
def setup_registry(request, bloks_loaded):
    def setup(bloks, function, **kwargs):
        registry = init_registry_with_bloks(bloks, function, **kwargs)
        request.addfinalizer(registry.close)
        return registry

    return setup


def add_in_registry_inherited(with_super=False):
    @register(Mixin)
    class MTest:
        @restrict_query_by_user()
        def my_restrict_query_by_user_method(cls, query, user):
            return query.filter_by(name="overriden")

        @restrict_query_by_user()
        def my_mixin_restrict_query_by_user_method(cls, query, user):
            return query.filter_by(name="mixin")

    @register(Model)
    class RestrictedModel(Mixin.MTest):

        name = String(primary_key=True, nullable=False)

        @restrict_query_by_user()
        def my_restrict_query_by_user_method(cls, query, user):
            return query.filter_by(name="base")

    @register(Model)  # noqa: F811
    class RestrictedModel:  # noqa: F811
        @restrict_query_by_user()
        def my_restrict_query_by_user_method(cls, query, user):
            if with_super:
                query = super().my_restrict_query_by_user_method(query, user)
            return query.filter_by(name="child")

        @restrict_query_by_user()
        def my_other_restrict_query_by_user_method(cls, query, user):
            return query.filter_by(name="other")


def get_filters_values(query):
    """Method that return a list of right clauses filters from a SQLAlechemy
    query"""
    right_clauses = []
    for c in query.clauses:
        if isinstance(c, BooleanClauseList):
            right_clauses.extend(get_filters_values(c))
        else:
            right_clauses.append(c.right.value)
    return sorted(right_clauses)


def test_restrict_query_by_user_inheritance(setup_registry):
    registry = setup_registry(
        ["pyramid", "anyblok-test"],
        add_in_registry_inherited,
        with_super=False,
    )
    query = registry.Pyramid.restrict_query_by_user(
        registry.RestrictedModel.query(), "test",
    )
    assert get_filters_values(query.whereclause) == ["child", "mixin", "other"]


def test_restrict_query_by_user_inheritance_calling_parent(setup_registry):
    registry = setup_registry(
        ["pyramid", "anyblok-test"], add_in_registry_inherited, with_super=True
    )
    query = registry.Pyramid.restrict_query_by_user(
        registry.RestrictedModel.query(), "test",
    )
    assert get_filters_values(query.whereclause) == [
        "base", "child", "mixin", "other",
    ]
