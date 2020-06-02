import json
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from mitigation import Mitigation


class LocalManager(Resource):
    def __init__(self, name='LocalManager', coap_server=None):
        super(LocalManager, self).__init__(name, coap_server,
                                           visible=True, observable=True, allow_children=True)
        self.payload = 'Local Manager'

    def render_PUT(self, request):
        self.payload = json.loads(request.payload)
        print(self.payload)
        mitigation = Mitigation(
            self.payload['mitigation-scope']['scope']['target-ip'])
        mitigation.firewall()
        if request.client_address != '192.168.0.10':
            client = HelperClient(server=('192.168.0.10', 4646))
            try:
                response = client.put('globalmanager', self.payload)
                print(response.pretty_print())
            except KeyboardInterrupt:
                pass
            finally:
                client.stop()
        return self
