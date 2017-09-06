from spoke.kv import KVDB
from spoke import dumpers


class HubCache:
    types = {'companies', 'company_props', 'contact_props', 'contacts', 'deal_props', 'deals', 'engagements', 'owners'}

    def __init__(self, api, filename):
        self.api = api
        self.db = KVDB(filename)

    def get(self, type, id, default=None):
        assert type in self.types
        return self.db.get(type, str(id), default)

    def get_many(self, type, ids):
        assert type in self.types
        return [ent for ent in (self.get(type, id) for id in ids) if ent is not None]

    def update(self):
        company_props = dumpers.dump_company_props(self.api)
        companies = dumpers.dump_companies(self.api, company_props)
        self.db.update('company_props', company_props)
        self.db.update('companies', companies)

        contact_props = dumpers.dump_contact_props(self.api)
        contacts = dumpers.dump_contacts(self.api, contact_props)
        self.db.update('contact_props', contact_props)
        self.db.update('contacts', contacts)

        deal_props = dumpers.dump_deal_props(self.api)
        deals = dumpers.dump_deals(self.api, deal_props)
        self.db.update('deal_props', deal_props)
        self.db.update('deals', deals)

        self.db.update('engagements', dumpers.dump_engagements(self.api))
        self.db.update('owners', dumpers.dump_owners(self.api))
