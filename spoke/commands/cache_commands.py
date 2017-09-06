import click

from spoke.cache import HubCache
from spoke.hubapi import get_api


@click.command()
@click.option('--cache-file', '-f', default='spoke.sqlite3')
def update_cache(cache_file):
    api = get_api()
    cache = HubCache(api, cache_file)
    cache.update()
