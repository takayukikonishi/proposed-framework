import json
import sys

import cbor2
from coapthon.client.helperclient import HelperClient


class DOTSClient():
    SIGNALCHANNEL_PORT = 4646

    def __init__(self, host):
        self.host = host
        self.path = None
        self.payload = None
        self.client = HelperClient(
            server=(self.host, DOTSClient.SIGNALCHANNEL_PORT))

    def PUT(self, path, payload):
        self.path = path
        self.payload = payload
        try:
            response = self.client.put(self.path, cbor2.dumps(self.payload))
            print(response.pretty_print())
        except KeyboardInterrupt:
            pass
        finally:
            self.client.stop()


def main():
    with open('Test.json', 'r') as f:
        mitigation_request = json.dumps(json.load(f))

    dots_client = DOTSClient(sys.argv[1])
    dots_client.PUT('dotsserver', mitigation_request)


if __name__ == '__main__':
    main()
