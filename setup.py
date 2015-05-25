# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup, find_packages
import os
version = '0.3.2'

requires = [
    'anyblok',
    'pyramid',
    'pyramid_beaker',
    'pyramid_rpc',
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(here, 'doc', 'FRONT.rst')) as front:
    FRONT = front.read()

with open(os.path.join(here, 'doc', 'CHANGES.rst')) as change:
    CHANGE = change.read()

console_scripts = [
    'anyblok_pyramid=anyblok_pyramid.scripts:wsgi',
]

setup(
    name="anyblok_pyramid",
    version=version,
    author="ean-Sébastien Suzanne",
    author_email="jssuzanne@anybox.fr",
    description="Web Server Pyramid for AnyBlok",
    license="MPL2",
    long_description=README + '\n' + FRONT + '\n' + CHANGE,
    url="https://bitbucket.org/jsuzanne/anyblok_pyramid",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + ['nose', 'WebTest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'console_scripts': console_scripts,
        'bloks': [
            'pyramid=anyblok_pyramid.bloks.pyramid:Pyramid',
        ],
    },
    extras_require={},
)
