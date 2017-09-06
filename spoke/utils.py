import json


def write_dumpfile(filename, data):
    with open(filename, 'w') as outf:
        json.dump(data, outf, indent=2, sort_keys=True)
        outf.flush()
        print('Wrote {filename}: {n} entries, {len} bytes'.format(
            filename=filename,
            n=len(data),
            len=outf.tell(),
        ))
