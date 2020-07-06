import json
import re
import argparse
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from mitigation import Mitigation


class LocalManagerResource(Resource):
    def __init__(self, router, approach, name='LocalManager', coap_server=None):
        super(LocalManagerResource, self).__init__(name, coap_server,
                                                   visible=True, observable=True, allow_children=True)
        self.payload = 'Local Manager'
        self.router = router
        self.approach = approach

    def render_PUT(self, request):
        self.payload = request.payload
        mitigation = Mitigation(self.router)
        mitigationrequest = json.loads(self.payload)
#        mitigationrequest = rewrite(json.loads(self.payload))
        if self.approach == 'drop':
            mitigation.drop(mitigationrequest)
        if self.approach == 'throttle':
            mitigation.throttle(mitigationrequest)
        if request.source[0] != '10.1.0.2':
            client = HelperClient(server=('10.1.0.2', 4646))
            try:
                response = client.put(
                    'globalmanager', self.payload)
                print(response.pretty_print())
            except KeyboardInterrupt:
                pass
            finally:
                client.stop()
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port, router, approach):
        CoAP.__init__(self, (host, port))
        self.add_resource(
            'localmanager/', LocalManagerResource(router, approach))


def main():
    port = 4646

    parser = argparse.ArgumentParser()
    parser.add_argument('--router', '-r')
    parser.add_argument('--approach', '-a')
    args = parser.parse_args()
    server = CoAPServer('0.0.0.0', port, args.router, args.approach)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        server.close()
        print('Exiting...')


if __name__ == '__main__':
    main()
