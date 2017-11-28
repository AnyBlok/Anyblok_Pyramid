# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup, find_packages
import os
version = '0.8.1'

requires = [
    'anyblok>=0.9.0',
    'pyramid',
    'pyramid_tm',
    'zope.sqlalchemy',
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as readme:
    README = readme.read()

with open(
    os.path.join(here, 'doc', 'FRONT.rst'), 'r', encoding='utf-8'
) as front:
    FRONT = front.read()

with open(
    os.path.join(here, 'doc', 'CHANGES.rst'), 'r', encoding='utf-8'
) as change:
    CHANGE = change.read()

console_scripts = [
    'anyblok_pyramid=anyblok_pyramid.scripts:wsgi',
    'gunicorn_anyblok_pyramid=anyblok_pyramid.scripts:gunicorn_wsgi',
]

anyblok_pyramid_includeme = [
    'pyramid_tm=anyblok_pyramid.pyramid_config:pyramid_tm',
    'static_paths=anyblok_pyramid.pyramid_config:static_paths',
]
anyblok_init = [
    'anyblok_pyramid_config=anyblok_pyramid:anyblok_init_config',
]

setup(
    name="anyblok_pyramid",
    version=version,
    author="Jean-Sébastien Suzanne",
    author_email="jssuzanne@anybox.fr",
    description="Web Server Pyramid for AnyBlok",
    license="MPL2",
    long_description=README + '\n' + FRONT + '\n' + CHANGE,
    url="http://docs.anyblok-pyramid.anyblok.org/" + version,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + ['nose', 'WebTest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'console_scripts': console_scripts,
        'anyblok_pyramid.settings': [
            'pyramid_settings=anyblok_pyramid.pyramid_config:pyramid_settings',
        ],
        'anyblok_pyramid.includeme': anyblok_pyramid_includeme,
        'anyblok.init': anyblok_init,
        'test_bloks': [
            'test-pyramid-blok1=anyblok_pyramid.test_bloks.test_pyramid_blok1:'
            'TestPyramidBlok',
        ]
    },
    extras_require={},
)
