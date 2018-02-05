# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import BlokTestCase


class TestQuery(BlokTestCase):

    def test_empty(self):
        query = self.registry.System.Blok.query().condition_filter({}, {})
        self.assertEqual(
            self.registry.System.Blok.query().count(),
            query.count()
        )

    def test_equal_condition(self):
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.name',
                operator='==',
                right_value='authorization',
            ),
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertEqual(query.count(), 1)

    def test_not_equal_contition(self):
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.name',
                operator='!=',
                right_value='authorization',
            ),
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertEqual(
            self.registry.System.Blok.query().count() - 1,
            query.count()
        )

    def test_not_equal_contition_2(self):
        query = self.registry.System.Blok.query().condition_filter(
            {
                'not': dict(
                    left_condition='Blok.name',
                    operator='==',
                    right_value='authorization',
                )
            },
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertEqual(
            self.registry.System.Blok.query().count() - 1,
            query.count()
        )

    def test_like_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.name',
                operator='like',
                right_value='%auth%',
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.name.like('%auth%')).count(),
            query.count()
        )

    def test_ilike_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.name',
                operator='ilike',
                right_value='auth',
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.name.ilike('auth')).count(),
            query.count()
        )

    def test_lt_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.order',
                operator='<',
                right_value=2,
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.order < 2).count(),
            query.count()
        )

    def test_lte_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.order',
                operator='<=',
                right_value=2,
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.order <= 2).count(),
            query.count()
        )

    def test_gt_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.order',
                operator='>',
                right_value=2,
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.order > 2).count(),
            query.count()
        )

    def test_gte_condition(self):
        Blok = self.registry.System.Blok
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.order',
                operator='>=',
                right_value=2,
            ),
            {
                'Blok': Blok
            }
        )
        self.assertEqual(
            Blok.query().filter(Blok.order >= 2).count(),
            query.count()
        )

    def test_or_condition(self):
        query = self.registry.System.Blok.query().condition_filter(
            {
                'or': [
                    dict(
                        left_condition='Blok.name',
                        operator='==',
                        right_value='authorization',
                    ),
                    dict(
                        left_condition='Blok.name',
                        operator='==',
                        right_value='auth',
                    )
                ],
            },
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertEqual(query.count(), 2)

    def test_and_condition_1(self):
        query = self.registry.System.Blok.query().condition_filter(
            {
                'and': [
                    dict(
                        left_condition='Blok.name',
                        operator='==',
                        right_value='authorization',
                    ),
                    dict(
                        left_condition='Blok.order',
                        operator='==',
                        right_value=0,
                    )
                ],
            },
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertFalse(query.count())

    def test_and_condition_2(self):
        query = self.registry.System.Blok.query().condition_filter(
            {
                'and': [
                    dict(
                        left_condition='Blok.name',
                        operator='==',
                        right_value='authorization',
                    ),
                    dict(
                        left_condition='Blok.order',
                        operator='!=',
                        right_value=0,
                    )
                ],
            },
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertTrue(query.count())

    def test_in_condition(self):
        query = self.registry.System.Blok.query().condition_filter(
            dict(
                left_condition='Blok.name',
                operator='in',
                right_value=['auth', 'authorization'],
            ),
            {
                'Blok': self.registry.System.Blok
            }
        )
        self.assertEqual(query.count(), 2)

    def test_with_relationship(self):
        user = self.registry.User.insert(login="jssuzanne", first_name="js",
                                         last_name="suzanne")
        role = self.registry.User.Role.insert(name='admin', label="Admin")
        role.users.append(user)
        authorization = self.registry.User.Authorization.insert(
            resource='test', role=role)
        query = self.registry.User.Authorization.query().condition_filter(
            dict(
                left_condition='Authorization.role.users.name',
                operator='=',
                right_value='jssuzanne',
            ),
            {
                'Authorization': self.registry.User.Authorization
            }
        )
        self.assertEqual(query.count(), 1)
        self.assertIs(query.one(), authorization)
