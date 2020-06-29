import json
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient


class GlobalManager(Resource):
    def __init__(self, name='GlobalManager', coap_server=None):
        super(GlobalManager, self).__init__(name, coap_server,
                                            visible=True, observable=True, allow_children=True)
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
