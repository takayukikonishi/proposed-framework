import json
import  argparse
from coapthon.server.coap import CoAP
from localmanager import LocalManager
from globalmanager import GlobalManager


class CoAPServer(CoAP):
    def __init__(self, host, port, router):
        CoAP.__init__(self, (host, port))
        self.add_resource('localmanager/', LocalManager(router))
        self.add_resource('globalmanager/', GlobalManager())


def main():
    port = 4646

    parser = argparse.ArgumentParser()
    parser.add_argument('--router', '-r')
    args = parser.parse_args()
    server = CoAPServer('0.0.0.0', port, args.router)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        server.close()
        print('Exiting...')


if __name__ == '__main__':
    main()
