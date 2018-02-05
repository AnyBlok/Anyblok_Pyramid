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
        compiled = sub_condition_filter(query, conditions['or'], objects)
        return or_(*compiled)
    elif 'and' in conditions:
        compiled = sub_condition_filter(query, conditions['and'], objects)
        return and_(*compiled)
    elif 'not' in conditions:
        compiled = sub_condition_filter(query, [conditions['not']], objects)
        return ~ compiled[0]

    return condition_filter_leaf(query, conditions, objects)


def sub_condition_filter(query, conditions, objects):
    compiled = []
    for condition in conditions:
        compiled.append(condition_filter(query, condition, objects))

    return compiled


def get_value_for(query, conditions, key_value, key_condition, key_adapter,
                  objects):
    if key_value in conditions:
        value = conditions[key_value]
        if key_adapter in conditions:
            value = adapt_value(conditions[key_adapter], value)

        return value

    if key_condition in conditions:
        value = conditions[key_condition].split('.')
        entry = objects[value[0]]
        keys = value[1:]
        if len(keys) > 1:
            return get_value_for_relationship(query, entry, keys)

        return getattr(entry, keys[0])


def get_value_for_relationship(query, entry, keys):
    res = getattr(entry, keys[0], None)
    if len(keys) == 1:
        return res

    if hasattr(entry, '__registry_name__'):
        Model = query.registry.get(entry.__registry_name__)
        if entry is Model:
            query.join(res)

    return get_value_for_relationship(query, res, keys[1:])


def adapt_value(adapter, value):
    if adapter == 'datetime':
        return parse(value)


def condition_filter_leaf(query, conditions, objects):  # noqa
    left = get_value_for(
        query, conditions, 'left_value', 'left_condition', 'left_adapter',
        objects)
    right = get_value_for(
        query, conditions, 'right_value', 'right_condition', 'right_adapter',
        objects)
    operator = conditions.get('operator')

    if operator == '==':
        return left == right
    if operator == '!=':
        return left != right
    if operator == 'in':
        return left.in_(right)
    if operator == 'not in':
        return left.notin(right)
    if operator == '<':
        return left < right
    if operator == '<=':
        return left <= right
    if operator == '>':
        return left > right
    if operator == '>=':
        return left >= right
    if operator == 'like':
        return left.like(right)
    if operator == 'not like':
        return ~ left.like(right)
    if operator == 'ilike':
        return left.ilike(right)
    if operator == 'not ilike':
        return ~ left.ilike(right)

    return None


@Declarations.register(Declarations.Core)
class Query:

    def condition_filter(self, conditions, objects):
        compiled = condition_filter(self, conditions, objects)
        if compiled is None:
            return self

        return self.filter(compiled)
