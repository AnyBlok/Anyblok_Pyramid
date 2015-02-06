from setuptools import setup, find_packages
version = '0.0.1'

requires = [
    'anyblok',
    'pyramid',
    'pyramid_beaker',
    'pyramid_rpc',
]

setup(
    name="Anyblok Pyramid",
    version=version,
    author="ean-Sébastien Suzanne",
    author_email="jssuzanne@anybox.fr",
    description="Web Server Pyramid for AnyBlok",
    license="MPL2",
    long_description='',
    url="https://bitbucket.org/jsuzanne/anyblok.pyramid",
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
        'License :: OSI Approved :: Mozilla Public License v2',
    ],
    entry_points={
        'AnyBlok': [
            'pyramid=anyblok_pyramid.bloks.pyramid:Pyramid',
        ],
    },
    extras_require={},
)
