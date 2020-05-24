import json

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from mitigation import Mitigation


class DOTSServerResource(Resource):
    def __init__(self, name='DOTSServerResource', coap_server=None):
        super(DOTSServerResource, self).__init__(name, coap_server,
                                                 visible=True, observable=True, allow_children=True)
        self.payload = 'DOTS Server Resource'

    def render_PUT(self, request):
        self.payload = json.loads(request.payload)
        print(self.payload)
        mitigation = Mitigation(self.payload['mitigation-scope']['scope']['target-ip'])
        mitigation.firewall()
        return self


class DOTSServer(CoAP):
    SIGNALCHANNEL_PORT = 4646

    def __init__(self):
        CoAP.__init__(self, ('0.0.0.0', DOTSServer.SIGNALCHANNEL_PORT))
        self.add_resource('dotsserver/', DOTSServerResource())


def main():
    dots_server = DOTSServer()
    try:
        dots_server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        dots_server.close()
        print('Exiting...')


if __name__ == '__main__':
    main()
