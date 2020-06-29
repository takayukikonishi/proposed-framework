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
        mitigation = Mitigation(self.router)
        for scope in json.loads(self.payload)['ietf-dots-signal-channel:mitigation-scope']['scope'] :
            for target_prefix in scope['target-prefix'] :
                target_ip = re.sub('/\d*', '', target_prefix)
                print(target_ip)
                for target_port_range in scope['target-port-range'] :
                    target_lower_port = target_port_range['lower-port']
                    for target_protocol in scope['target-protocol'] :
                        if target_protocol == 6 :
                            target_protocol = 'tcp'
                        elif target_protocol == 17 :
                            target_protocol = 'udp'
                        mitigation.firewall(target_ip, target_lower_port, target_protocol)
                        if request.source[0] != '10.1.0.2':
                            client = HelperClient(server=('10.1.0.2', 4646))
                            try:
                                response = client.put('globalmanager', self.payload)
                                print(response.pretty_print())
                            except KeyboardInterrupt:
                                pass
                            finally:
                                client.stop()
        return self
