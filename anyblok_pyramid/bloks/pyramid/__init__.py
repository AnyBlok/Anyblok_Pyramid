from anyblok.blok import Blok
from anyblok_pyramid.release import version


class Pyramid(Blok):
    version = version

    required = [
        'anyblok-core',
    ]
