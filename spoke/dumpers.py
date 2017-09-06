def dump_contact_props(api):
    return {p['name']: p for p in api.request('get', '/properties/v1/contacts/properties/')}


def dump_company_props(api):
    return {p['name']: p for p in api.request('get', '/properties/v1/companies/properties/')}


def dump_deal_props(api):
    return {p['name']: p for p in api.request('get', '/properties/v1/deals/properties/')}


def dump_engagements(api):
    return {
        engagement['engagement']['id']: engagement
        for engagement
        in api.load_paged('/engagements/v1/engagements/paged')
    }


def dump_contact_lists(api):
    return {
        contact_list['listId']: contact_list
        for contact_list
        in api.load_paged('/contacts/v1/lists', results_key='lists')
    }


def dump_contacts(api, contact_props):
    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('property', prop_name) for prop_name in contact_props]
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
    return contacts


def dump_companies(api, company_props):
    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('properties', prop_name) for prop_name in company_props]
        return api.request(**kwargs)

    company_iterator = api.load_paged(
        url='/companies/v2/companies/paged',
        results_key='companies',
        requestor=requestor,
    )
    return {company['companyId']: company for company in company_iterator}


def dump_deals(api, deal_props):
    def requestor(**kwargs):
        kwargs['params'] = list(kwargs['params'].items()) + [('properties', prop_name) for prop_name in deal_props]
        return api.request(**kwargs)

    deal_iterator = api.load_paged(
        url='/deals/v1/deal/paged',
        params={'includeAssociations': 'true'},
        results_key='deals',
        requestor=requestor,
    )
    return {deal['dealId']: deal for deal in deal_iterator}


def dump_owners(api):
    return {o['ownerId']: o for o in api.request('get', '/owners/v2/owners/')}
