from anyblok_pyramid._argsparse import (define_wsgi_option,
                                        define_beaker_option,
                                        define_wsgi_debug_option)
from anyblok.tests.testcase import TestCase
from anyblok.tests.test_argsparse import MockArgumentParser


class TestArgsParseOption(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestArgsParseOption, cls).setUpClass()
        cls.parser = MockArgumentParser()
        cls.group = cls.parser.add_argument_group('label')
        cls.configuration = {}
        cls.function = {
            'define_wsgi_option': define_wsgi_option,
            'define_beaker_option': define_beaker_option,
            'define_wsgi_debug_option': define_wsgi_debug_option,
        }

    def test_define_wsgi_option(self):
        self.function['define_wsgi_option'](self.parser, self.configuration)

    def test_define_beaker_option(self):
        self.function['define_beaker_option'](self.parser, self.configuration)

    def test_define_wsgi_debug_option(self):
        self.function['define_wsgi_debug_option'](self.parser,
                                                  self.configuration)
