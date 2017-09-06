import click
from importlib import import_module

import os

import spoke.dump


class PluginCLI(click.MultiCommand):
    command_map = {
        'dump-companies': spoke.dump.dump_companies,
        'dump-contact-lists': spoke.dump.dump_contact_lists,
        'dump-contacts': spoke.dump.dump_contacts,
        'dump-deals': spoke.dump.dump_deals,
        'dump-engagements': spoke.dump.dump_engagements,
        'dump-owners': spoke.dump.dump_owners,
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
