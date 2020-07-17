import argparse
import json

from coapthon.client.helperclient import HelperClient
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

from mitigation import Mitigation


class LocalManagerResource(Resource):
    def __init__(
            self,
            router,
            approach,
            framework,
            name="LocalManager",
            coap_server=None):
        super(
            LocalManagerResource,
            self).__init__(
            name,
            coap_server,
            visible=True,
            observable=True,
            allow_children=True)
        self.payload = "Local Manager"
        self.router = router
        self.approach = approach
        self.framework = framework

    def render_PUT(self, request):
        self.payload = request.payload
        mitigation = Mitigation(self.router)
        mitigationrequest = json.loads(self.payload)
        # mitigationrequest = rewrite(json.loads(self.payload))
        if self.approach == "drop":
            mitigation.drop(mitigationrequest)
        elif self.approach == "shaping":
            mitigation.shaping(mitigationrequest)
        elif self.approach == "pass":
            pass
        else:
            print(
                f"Error: {self.approach} is a non-existent argument")
            exit
        if self.framework == "on" and request.source[0] != "10.1.0.2":
            client = HelperClient(server=("10.1.0.2", 4646))
            try:
                response = client.put("globalmanager", self.payload)
                print(response.pretty_print())
            except KeyboardInterrupt:
                pass
            finally:
                client.stop()
        elif self.framework == "off":
            pass
        else:
            print(
                f"Error: {self.framework} is a non-existent argument")
            exit
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port, router, approach, framework):
        CoAP.__init__(self, (host, port))
        self.add_resource(
            "localmanager/", LocalManagerResource(router, approach, framework)
        )


def main():
    port = 4646

    parser = argparse.ArgumentParser()
    parser.add_argument("router")
    parser.add_argument("--approach", "-a", default="drop")
    parser.add_argument("--framework", "-f", default="on")
    args = parser.parse_args()
    server = CoAPServer(
        "0.0.0.0",
        port,
        args.router,
        args.approach,
        args.framework)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")


if __name__ == "__main__":
    main()
