# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok import Declarations
from sqlalchemy import or_, and_
from dateutil.parser import parse


def condition_filter(query, conditions, objects):
    if 'or' in conditions:
        query, compiled = sub_condition_filter(
            query, conditions['or'], objects)
        return query, or_(*compiled)
    elif 'and' in conditions:
        query, compiled = sub_condition_filter(
            query, conditions['and'], objects)
        return query, and_(*compiled)
    elif 'not' in conditions:
        query, compiled = sub_condition_filter(
            query, [conditions['not']], objects)
        return query, ~ compiled[0]

    return condition_filter_leaf(query, conditions, objects)


def sub_condition_filter(query, conditions, objects):
    compileds = []
    for condition in conditions:
        query, compiled = condition_filter(query, condition, objects)
        compileds.append(compiled)

    return query, compileds


def get_value_for(query, conditions, key_value, key_condition, key_adapter,
                  objects):
    if key_value in conditions:
        value = conditions[key_value]
        if key_adapter in conditions:
            value = adapt_value(conditions[key_adapter], value)

        return query, value

    if key_condition in conditions:
        value = conditions[key_condition].split('.')
        entry = objects[value[0]]
        keys = value[1:]
        if len(keys) > 1:
            return query, get_value_for_relationship(query, entry, keys)

        return query, getattr(entry, keys[0])

    return query, None


def get_value_for_relationship(query, entry, keys):
    res = getattr(entry, keys[0], None)
    if len(keys) == 1:
        return query, res

    if hasattr(entry, '__registry_name__'):
        Model = query.registry.get(entry.__registry_name__)
        if entry is Model:
            query = query.join(res)

    return query, get_value_for_relationship(query, res, keys[1:])


def adapt_value(adapter, value):
    if adapter == 'datetime':
        return parse(value)


def condition_filter_leaf(query, conditions, objects):  # noqa
    query, left = get_value_for(
        query, conditions, 'left_value', 'left_condition', 'left_adapter',
        objects)
    query, right = get_value_for(
        query, conditions, 'right_value', 'right_condition', 'right_adapter',
        objects)
    operator = conditions.get('operator')

    if operator == '==':
        return query, left == right
    if operator == '!=':
        return query, left != right
    if operator == 'in':
        return query, left.in_(right)
    if operator == 'not in':
        return query, left.notin(right)
    if operator == '<':
        return query, left < right
    if operator == '<=':
        return query, left <= right
    if operator == '>':
        return query, left > right
    if operator == '>=':
        return query, left >= right
    if operator == 'like':
        return query, left.like(right)
    if operator == 'not like':
        return query, ~ left.like(right)
    if operator == 'ilike':
        return query, left.ilike(right)
    if operator == 'not ilike':
        return query, ~ left.ilike(right)

    return query, None


@Declarations.register(Declarations.Core)
class Query:

    def condition_filter(self, conditions, objects):
        query, compiled = condition_filter(self, conditions, objects)
        if compiled is None:
            return self

        return query.filter(compiled)
