import click

from spoke.hubapi import get_api
from spoke.utils import write_dumpfile
from spoke import dumpers


@click.command()
@click.option('-o', '--output', default='engagements.json')
def dump_engagements(output):
    api = get_api()
    write_dumpfile(output, dumpers.dump_engagements(api))


@click.command()
@click.option('-o', '--output', default='contact-lists.json')
def dump_contact_lists(output):
    api = get_api()
    write_dumpfile(output, dumpers.dump_contact_lists(api))


@click.command()
@click.option('-o', '--output', default='contacts.json')
@click.option('-p', '--props-output', default='contact-props.json')
def dump_contacts(output, props_output):
    api = get_api()
    contact_props = dumpers.dump_contact_props(api)
    write_dumpfile(props_output, contact_props)
    write_dumpfile(output, dumpers.dump_contacts(api, contact_props))


@click.command()
@click.option('-o', '--output', default='companies.json')
@click.option('-p', '--props-output', default='company-props.json')
def dump_companies(output, props_output):
    api = get_api()
    company_props = dumpers.dump_company_props(api)
    write_dumpfile(props_output, company_props)
    write_dumpfile(props_output, dumpers.dump_companies(api, company_props))


@click.command()
@click.option('-o', '--output', default='deals.json')
@click.option('-p', '--props-output', default='deal-props.json')
def dump_deals(output, props_output):
    api = get_api()
    deal_props = dumpers.dump_deal_props(api)
    write_dumpfile(props_output, deal_props)
    write_dumpfile(output, dumpers.dump_deals(api, deal_props))


@click.command()
@click.option('-o', '--output', default='owners.json')
def dump_owners(output):
    api = get_api()
    write_dumpfile(output, dumpers.dump_owners(api))
