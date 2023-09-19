from aiohttp import web
import jinja2
import aiohttp_jinja2
import asyncio

tasks = []


@aiohttp_jinja2.template('index.jinja2')
async def index_page(request):
    pulls = 3
    lights = 2
    return {'title': 'Flashing Lights', 'pulls': pulls, 'lights': lights}


async def add_light(request):
    data = await request.json()
    print(data)
    return web.json_response('ok')


async def add_setting(request):
    return web.json_response('ok')


async def init_app():
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    app.router.add_static('/static', 'static', name='static')
    app.router.add_get('/', index_page)
    app.router.add_post('/add_light', add_light)
    app.router.add_post('/add_setting', add_setting)

    return app


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app)


if __name__ == '__main__':
    main()
