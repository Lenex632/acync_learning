from aiohttp import web
import jinja2
import aiohttp_jinja2


@aiohttp_jinja2.template('index.jinja2')
async def index_page(request):
    return {'title': 'Flashing Lights', 'pulls': 3, 'lights': 4}


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.router.add_static('/static', 'static', name='static')
    app.router.add_get('/', index_page)

    web.run_app(app)
