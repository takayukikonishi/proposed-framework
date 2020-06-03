import json
import re
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient
from mitigation import Mitigation


class LocalManager(Resource):
    def __init__(self, router, name='LocalManager', coap_server=None):
        super(LocalManager, self).__init__(name, coap_server,
                                           visible=True, observable=True, allow_children=True)
        self.payload = 'Local Manager'
        self.router = router

    def render_PUT(self, request):
        self.payload = request.payload
        for scope in json.loads(self.payload)['ietf-dots-signal-channel:mitigation-scope']['scope'] :
            for target_prefix in scope['target-prefix'] :
                target_ip = re.sub('/\d*', '', target_prefix)
                print(target_ip)
                mitigation = Mitigation(target_ip, self.router)
                mitigation.firewall()
                if request.source[0] != '192.168.0.10':
                    client = HelperClient(server=('192.168.0.10', 4646))
                    try:
                        response = client.put('globalmanager', self.payload)
                        print(response.pretty_print())
                    except KeyboardInterrupt:
                        pass
                    finally:
                        client.stop()
        return self
