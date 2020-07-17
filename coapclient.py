import json
import sys

from coapthon.client.helperclient import HelperClient


def main():
    host = sys.argv[1]
    port = 4646
    path = 'localmanager'

    file_path = sys.argv[2]
    with open(file_path, 'r') as f:
        payload = json.dumps(json.load(f))
    client = HelperClient(server=(host, port))
    try:
        response = client.put(path, payload)
        print(response.pretty_print())
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()


if __name__ == '__main__':
    main()
