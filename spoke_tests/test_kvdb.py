from spoke.kv import KVDB


def test_kvdb():
    k = KVDB(':memory:')
    k.set('foo', 123, 'bar')
    assert k.get('foo', 123) == 'bar'
