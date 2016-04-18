from pyramid.view import view_config
from pyramid.response import Response
from anyblok_pyramid import current_blok


@view_config(route_name='hello', installed_blok=current_blok())
def say_hello(request):
    return Response('Hello %(name)s !!!' % request.matchdict)
