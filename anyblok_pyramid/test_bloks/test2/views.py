from pyramid.view import view_config, view_defaults
from anyblok_pyramid import current_blok


@view_defaults(installed_blok=current_blok())
class Bloks:
    def __init__(self, request):
        self.request = request
        self.registry = request.anyblok.registry

    @view_config(route_name='bloks', renderer="json",
                 request_method='GET', permission="read")
    def get_all(self):
        return self.registry.System.Blok.query().all().to_dict(
                'name', 'author', 'version')

    @view_config(route_name='blok', renderer="json",
                 request_method='GET', permission="read")
    def get_one(self):
        return self.registry.System.Blok.query().filter_by(
            name=self.request.matchdict['name']).one().to_dict(
                'name', 'author', 'version')

    @view_config(route_name='blok', renderer="json",
                 request_method='PUT', permission="write")
    def put_one(self):
        return self.registry.System.Blok.query().filter_by(
            name=self.request.matchdict['name']).one().to_dict(
                'name', 'author', 'version')
