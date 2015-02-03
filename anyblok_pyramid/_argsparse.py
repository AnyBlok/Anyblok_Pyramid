from anyblok._argsparse import ArgsParseManager


@ArgsParseManager.add('wsgi')
def define_wsgi_option(parser, configuration):
    parser.add_argument('--databases', dest='dbnames', default='',
                        help='List of the database allow to be load')
