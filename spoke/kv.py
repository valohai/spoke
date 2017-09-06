import json
import sqlite3

from collections import defaultdict


class KVDB:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cache = defaultdict(dict)

    def set(self, table, key, value):
        try:
            if isinstance(value, (list, dict, tuple)):
                type = 'json'
                e_value = json.dumps(value)
            else:
                type = 'str'
                e_value = value

            self.db.execute(
                'INSERT OR REPLACE INTO {table} (key, type, value) VALUES (?, ?, ?)'.format(table=table),
                (key, type, e_value)
            )
            self.cache[table][key] = value
        except sqlite3.OperationalError as oe:
            if 'no such table' in str(oe):
                self._create_table(table)
                return self.set(table, key, value)
            raise

    def get(self, table, key, default=None):
        if key in self.cache[table]:
            return self.cache[table][key]

        cur = self.db.cursor()
        cur.execute(
            'SELECT key, type, value FROM {table} WHERE key=? LIMIT 1'.format(table=table),
            (key,)
        )
        row = cur.fetchone()
        if not row:
            value = default
        else:
            key, type, value = row
            if type == 'json':
                value = json.loads(value)
        self.cache[table][key] = value
        return value

    def update(self, table, dict):
        with self.db:  # in transaction
            for key, value in dict.items():
                self.set(table, key, value)

    def _create_table(self, table):
        self.db.execute('CREATE TABLE {table} (key TEXT PRIMARY KEY, type TEXT, value TEXT)'.format(table=table))
