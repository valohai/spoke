import time

import click
import requests

from spoke.cache import HubCache
from spoke.formatting import format_engagement
from spoke.hubapi import get_api


@click.command()
@click.option('--cache-file', '-c', default='spoke.sqlite3')
@click.option('--cutoff', '-t', type=int, default=86400)
@click.option('--emails/--no-emails', '-e/-E', default=False)
@click.option('--meetings/--no-meetings', '-m/-M', default=True)
@click.option('--notes/--no-notes', '-n/-N', default=False)
@click.option('--tasks/--no-tasks', '-t/-T', default=False)
@click.option('--slack-webhook-url')
def list_new_engagements(cache_file, cutoff, emails, meetings, notes, tasks, slack_webhook_url):
    api = get_api()
    cache = HubCache(api, filename=cache_file)
    cutoff_ts = time.time() - cutoff
    response = api.request('GET', '/engagements/v1/engagements/recent/modified', params={'count': 100})
    #with open('foo.json', 'r') as inf:
    #    response = json.load(inf)
    sess = requests.Session()
    for eng in filter_engagements(
        response,
        cutoff_ts=cutoff_ts,
        emails=emails, meetings=meetings, notes=notes, tasks=tasks
    ):
        formatted = format_engagement(cache, eng)
        print(formatted)
        if slack_webhook_url:
            sess.post(slack_webhook_url, json={
                'text': formatted,
            })


def filter_engagements(resp, *, cutoff_ts, emails, meetings, notes, tasks):
    engagements = [eng for eng in resp['results'] if (float(eng['engagement']['timestamp']) / 1000) > cutoff_ts]
    for eng in engagements:
        type = eng['engagement']['type']
        if type in ('EMAIL', 'INCOMING_EMAIL') and not emails:
            continue
        if type == 'MEETING' and not meetings:
            continue
        if type == 'TASK' and not tasks:
            continue
        if type == 'NOTE' and not notes:
            continue
        yield eng
