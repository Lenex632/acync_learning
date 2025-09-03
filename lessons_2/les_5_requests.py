import asyncio
import logging
import re
import sys
import pathlib
import urllib.parse
import urllib.error

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    response = await session.request(method='GET', url=url, **kwargs)
    response.raise_for_status()
    logger.info(f'Got response [{response.status}] for url: {url}.')
    html = await response.text()
    return html


async def parse(url: str, session: ClientSession, **kwargs) -> set:
    found = set()
    try:
        html = await fetch_html(url, session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http.HttpProcessingError,
    ) as e:
        logger.error(f'aiohttp exception for {url} {getattr(e, "status", None)}: {getattr(e, "message", None)}.')
        return found
    except Exception as e:
        logger.exception(f'Non-aiohttp exception occured: {getattr(e, "__dict__", {})}.')
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception(f'Error parsing URL: {link}.')
                pass
            else:
                found.add(abslink)
        logger.info(f'Fount {len(found)} for {url}.')
        return found


async def write_one(file: pathlib.Path, url: str, session: ClientSession, **kwargs) -> None:
    res = await parse(url, session, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, 'a') as f:
        for p in res:
            await f.write(f'{url}\t{p}\n')
        logger.info(f'Wrote result for URL: {url}')


async def bulk_crawl_and_write(file: pathlib.Path, urls: set, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(write_one(file, url, session, **kwargs))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    here = pathlib.Path(__file__).parent

    with open(here.joinpath('urls.txt')) as infile:
        urls = set(map(str.strip, infile))

    outpath = here.joinpath('foundurls.txt')
    with open(outpath, 'w') as outfile:
        outfile.write('source_url\tparsed_url\n')

    asyncio.run(bulk_crawl_and_write(outpath, urls))

