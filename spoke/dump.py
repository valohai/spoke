import click

from spoke.hubapi import get_api
from spoke.utils import write_dumpfile


@click.command()
@click.option('-o', '--output', default='engagements.json')
def dump_engagements(output):
    api = get_api()
    engagements = {
        engagement['engagement']['id']: engagement
        for engagement
        in api.load_paged('/engagements/v1/engagements/paged')
    }
    write_dumpfile(output, engagements)


@click.command()
@click.option('-o', '--output', default='contact-lists.json')
def dump_contact_lists(output):
    api = get_api()
    contact_lists = {
        contact_list['listId']: contact_list
        for contact_list
        in api.load_paged('/contacts/v1/lists', results_key='lists')
    }
    write_dumpfile(output, contact_lists)


@click.command()
@click.option('-o', '--output', default='contacts.json')
@click.option('-p', '--props-output', default='contact-props.json')
def dump_contacts(output, props_output):
    api = get_api()
    props = {p['name']: p for p in api.request('get', '/properties/v1/contacts/properties/')}
    write_dumpfile(props_output, props)

    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('property', prop_name) for prop_name in props]
        return api.request(**kwargs)

    contact_iterator = api.load_paged(
        '/contacts/v1/lists/all/contacts/all',
        results_key='contacts',
        offset_key='vid-offset',
        offset_param='vidOffset',
        limit_param='count',
        requestor=requestor,
    )
    contacts = {contact['canonical-vid']: contact for contact in contact_iterator}
    write_dumpfile(output, contacts)


@click.command()
@click.option('-o', '--output', default='companies.json')
@click.option('-p', '--props-output', default='company-props.json')
def dump_companies(output, props_output):
    api = get_api()
    props = {p['name']: p for p in api.request('get', '/properties/v1/companies/properties/')}
    write_dumpfile(props_output, props)

    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('properties', prop_name) for prop_name in props]
        return api.request(**kwargs)

    company_iterator = api.load_paged(
        url='/companies/v2/companies/paged',
        results_key='companies',
        requestor=requestor,
    )
    companies = {company['companyId']: company for company in company_iterator}
    write_dumpfile(output, companies)


@click.command()
@click.option('-o', '--output', default='deals.json')
@click.option('-p', '--props-output', default='deal-props.json')
def dump_deals(output, props_output):
    api = get_api()
    props = {p['name']: p for p in api.request('get', '/properties/v1/deals/properties/')}
    write_dumpfile(props_output, props)

    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('properties', prop_name) for prop_name in props]
        return api.request(**kwargs)

    deal_iterator = api.load_paged(
        url='/deals/v1/deal/paged',
        params={'includeAssociations': 'true'},
        results_key='deals',
        requestor=requestor,
    )
    deals = {deal['dealId']: deal for deal in deal_iterator}
    write_dumpfile(output, deals)


@click.command()
@click.option('-o', '--output', default='owners.json')
def dump_owners(output):
    api = get_api()
    owners = {o['ownerId']: o for o in api.request('get', '/owners/v2/owners/')}
    write_dumpfile(output, owners)
