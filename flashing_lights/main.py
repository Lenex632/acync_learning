from aiohttp import web
import jinja2
import aiohttp_jinja2


@aiohttp_jinja2.template('index.jinja2')
async def index_page(request):
    return {'title': 'Flashing Lights', 'pulls': 3, 'lights': 4}


async def plus_light(request):
    data = await request.json()
    print(data)
    return web.json_response('ok')


async def init_app():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.router.add_static('/static', 'static', name='static')
    app.router.add_get('/', index_page)
    app.router.add_post('/post', plus_light)

    return app


def main():
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
