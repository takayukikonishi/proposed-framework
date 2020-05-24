from http import server
import pymongo
import json


class HTTPRequestHandler(server.BaseHTTPRequestHandler):
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)
        data = file_content.decode()
        print(type(data))
        client = pymongo.MongoClient("localhost", 27017)
        db = client.test_database
        collection = db.test_collection
        result = collection.insert_one(json.loads(data))
        print(result)

        self.send_response(200)
        self.end_headers()


def main():
    handler = HTTPRequestHandler
    with server.HTTPServer(("", 8080), handler) as dotsserver:
        dotsserver.serve_forever()


if __name__ == '__main__':
    main()
