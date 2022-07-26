import json


def make_json_readable(filepath, new_filepath=None):

    with open(filepath) as f:
        data = json.loads(f.read())

    with open(filepath if new_filepath is None else new_filepath, 'w') as f:
        f.write(json.dumps(data, indent=4))


if __name__ == '__main__':
    s_filepath = r"C:\Users\jboun\AppData\Roaming\.minecraft\assets\indexes\1.19.json"
    o_filepath = r"C:\Users\jboun\AppData\Roaming\.minecraft\assets\indexes\1.19.Readable.json"
    make_json_readable(s_filepath, o_filepath)
