import json

from coapthon.client.helperclient import HelperClient
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP


class GlobalManagerResource(Resource):
    def __init__(self, name='GlobalManager', coap_server=None):
        super(
            GlobalManagerResource,
            self).__init__(
            name,
            coap_server,
            visible=True,
            observable=True,
            allow_children=True)
        self.payload = 'Global Manager'

    def render_PUT(self, request):
        self.payload = request.payload
        print(json.loads(self.payload))
        client = HelperClient(server=('10.2.0.2', 4646))
        try:
            response = client.put('localmanager', self.payload)
            print(response.pretty_print())
        except KeyboardInterrupt:
            pass
        finally:
            client.stop()
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('globalmanager/', GlobalManagerResource())


def main():
    port = 4646

    server = CoAPServer('0.0.0.0', port)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        server.close()
        print('Exiting...')


if __name__ == '__main__':
    main()
