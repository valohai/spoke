import os
from importlib import import_module

import click

from spoke.commands.dump_commands import (
    dump_companies,
    dump_contact_lists,
    dump_contacts,
    dump_deals,
    dump_engagements,
    dump_owners,
)


class PluginCLI(click.MultiCommand):
    command_map = {
        'dump-companies': dump_companies,
        'dump-contact-lists': dump_contact_lists,
        'dump-contacts': dump_contacts,
        'dump-deals': dump_deals,
        'dump-engagements': dump_engagements,
        'dump-owners': dump_owners,
    }

    def list_commands(self, ctx):
        return self.command_map.keys()

    def get_command(self, ctx, name):
        cmd = self.command_map.get(name)
        if not cmd:
            return None
        if isinstance(cmd, str):
            module, _, cls = cmd.rpartition('.')
            module = import_module(module)
            cmd = getattr(module, cls)
        return cmd


@click.command(cls=PluginCLI)
@click.option('--hapikey', '-k', envvar='HAPIKEY', required=True)
def cli(hapikey):
    os.environ['HAPIKEY'] = hapikey
