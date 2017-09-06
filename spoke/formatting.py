import datetime
import html
import re
from itertools import chain


def format_contact(contact):
    try:
        return '{fname} {lname}'.format(
            fname=contact['properties']['firstname']['value'],
            lname=contact['properties']['lastname']['value'],
        )
    except KeyError:
        try:
            return contact['properties']['email']['value']
        except KeyError:
            return 'CONTACT-{}'.format(contact['vid'])


def format_company(company):
    return company['properties']['name']['value']


def format_deal(deal):
    return deal['properties']['dealname']['value']


def format_engagement(cache, eng):
    type = eng['engagement']['type']
    ts = datetime.datetime.fromtimestamp(eng['engagement']['timestamp'] / 1000)
    ts_text = ts.strftime('%Y%m%d')
    owner = cache.get('owners', eng['engagement']['ownerId'])
    owner_name = owner['firstName']
    contacts = cache.get_many('contacts', eng['associations']['contactIds'])
    companies = cache.get_many('companies', eng['associations']['companyIds'])
    deals = cache.get_many('deals', eng['associations']['dealIds'])
    targets = ', '.join(list(chain(
        (':man:' + format_contact(contact) for contact in contacts),
        (':office:' + format_company(company) for company in companies),
        (':moneybag:' + format_deal(deal) for deal in deals),
    )))
    try:
        body = eng['metadata']['body']
        body = re.sub(r'<[^>]+>', ' ', body)
        body = html.unescape(body)
        body = re.sub(r'\s+', ' ', body).strip()
        if len(body) > 500:
            body = body[:497] + '...'
    except KeyError:
        body = None
    if type == 'NOTE':
        return ':notebook: {ts} {targets} by {owner}:\n{body}'.format(
            ts=ts_text,
            targets=targets,
            owner=owner_name,
            body=body,
        )
    if type == 'MEETING':
        return ':speech_balloon: {ts} *{title}* ({targets}) by {owner}:\n{body}'.format(
            ts=ts_text,
            targets=targets,
            owner=owner_name,
            title=eng['metadata']['title'],
            body=body,
        )
    if type == 'EMAIL':
        return ':outbox_tray: {ts} {owner} -> ({targets}): {subject}'.format(
            ts=ts_text,
            owner=owner_name,
            targets=targets,
            subject=eng['metadata']['subject'],
        )
    if type == 'INCOMING_EMAIL':
        return ':inbox_tray: {ts} ({targets}) -> {owner}: {subject}'.format(
            ts=ts_text,
            owner=owner_name,
            targets=targets,
            subject=eng['metadata']['subject'],
        )
    if type == 'TASK':
        return ':pick: {ts} ({targets}) by {owner}: {subject} - {body}'.format(
            ts=ts_text,
            targets=targets,
            owner=owner_name,
            body=body,
            subject=eng['metadata']['subject'],
        )
    return ':question: {type}'.format(type=type)
