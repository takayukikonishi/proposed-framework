import datetime
import json
import pprint
import socket
import sqlite3
import sys
import threading

from coapthon.client.helperclient import HelperClient
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP


class DOTSServerResource(Resource):
    def __init__(self, name='DOTSServerResource', coap_server=None):
        super(DOTSServerResource, self).__init__(name, coap_server,
                                                 visible=True, observable=True, allow_children=True)
        self.payload = 'DOTS Server Resource'

    def render_PUT(self, request):
        self.payload = request.payload

        # JSONメッセージを変数に
        # 辞書型に変換
        json_dict = json.loads(self.payload)
        print('DOTSクライアントから緩和要請を受信しました．')
        pprint.pprint(json_dict)
        # 要素を変数に格納
        c_id = json_dict['mitigation-scope']['client-id']

        # データベースと接続
        conn = sqlite3.connect(sys.argv[4])
        # カーソル作成
        c = conn.cursor()
        # テーブル作成
        c.execute(
            'CREATE TABLE IF NOT EXISTS identity_management(client_id PRIMARY KEY, time)')
        c.execute(
            'SELECT COUNT(*) FROM identity_management WHERE client_id = ?', [c_id, ])
        result = c.fetchall()
        if result[0][0] >= 1:
            # 識別子を自身のものに変更
            json_dict['mitigation-scope']['client-id'] = int(sys.argv[1])
            # CoAPで送信
            host = '127.0.0.1'
            port = 50010
            path = 'managementserver'
            payload = json.dumps(json_dict)
            print(payload)
            client = HelperClient(server=(host, port))
            try:
                response = client.put(path, payload)
                print(response.pretty_print())
                client.stop()
            except KeyboardInterrupt:
                client.stop()
        else:
            pass
        # 接続終了
        conn.close()
        return self


class PrintResource(Resource):
    def __init__(self, name='PrintResource', coap_server=None):
        super(PrintResource, self).__init__(name, coap_server,
                                            visible=True, observable=True, allow_children=True)
        self.payload = 'Print Resource'

    def render_PUT(self, request):
        self.payload = request.payload

        # 辞書型に変換
        json_dict = json.loads(self.payload)

        print('攻撃情報管理サーバから緩和要請を受信しました．')
        pprint.pprint(json_dict)

        return self


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('dotsserver/', DOTSServerResource())
        self.add_resource('print/', PrintResource())


def func1():
    try:
        # TCPサーバ
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('127.0.0.1', int(sys.argv[2])))
        while True:
            serversocket.listen()
            clientsocket, clientaddress = serversocket.accept()
            print(clientaddress)
            clientipaddress, clientport = clientaddress
            payload = clientsocket.recv(1024)
            dict_payload = json.loads(payload.decode())
            print()
            clientsocket.close()

            # 識別子を変数に格納
            c_id = dict_payload['ietf-dots-data-channel:dots-client']['client-id']

            # 識別子管理データベース
            # データベースと接続
            conn = sqlite3.connect(sys.argv[4])
            # カーソル作成
            c = conn.cursor()
            # テーブル作成
            c.execute(
                'CREATE TABLE IF NOT EXISTS identity_management(client_id PRIMARY KEY, time)')
            # プレースホルダ
            p = 'INSERT INTO identity_management(client_id, time) VALUES(?, ?)'
            # 現在時刻取得
            now = datetime.datetime.now()
            # データ追加
            c.execute(p, (c_id, now))
            # コミット
            conn.commit()
            # データを全て出力
            c.execute('SELECT * FROM identity_management')
            print(c.fetchall())
            # 接続終了
            conn.close()
    except KeyboardInterrupt:
        serversocket.close()


def func2():
    # CoAPサーバ
    server = CoAPServer('127.0.0.1', int(sys.argv[3]))
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        server.close()
        print('Exiting...')


def main():
    # JSONメッセージを作成
    client_id = int(sys.argv[1])
    port = int(sys.argv[3])
    registration_request = {
        "ietf-dots-data-channel:dots-client":
        {
            "client-id": client_id,
            "signal-channel-port": port
        }
    }
    data = json.dumps(registration_request)

    # TCPで送信
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', 50000))
    clientsocket.send(data.encode())
    clientsocket.close()

    # マルチスレッド
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_2.start()
    thread_1.start()


if __name__ == '__main__':
    main()
