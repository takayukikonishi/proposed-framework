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


class ManagementServerResource(Resource):
    def __init__(self, name='ManagementServerResource', coap_server=None):
        super(ManagementServerResource, self).__init__(
            name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = 'Management Server Resource'

    def render_PUT(self, request):
        self.payload = request.payload

        # JSONメッセージを変数に
        # 辞書型に変換
        json_dict = json.loads(self.payload)
        print('DOTSサーバから緩和要請を受信しました．')
        pprint.pprint(json_dict)

        # 要素を変数に格納
        c_id = json_dict['mitigation-scope']['client-id']

        # データベースと接続
        conn = sqlite3.connect('IdentityManagement.db')
        # カーソル作成
        c = conn.cursor()
        # テーブル作成
        c.execute(
            'CREATE TABLE IF NOT EXISTS identity_management_0(client_id PRIMARY KEY, time, port)')
        c.execute(
            'SELECT COUNT(*) FROM identity_management_0 WHERE client_id = ?', [c_id, ])
        result = c.fetchall()
        if result[0][0] >= 1:
            # 識別子を自身のものに変更
            json_dict['mitigation-scope']['client-id'] = 0
            # 識別子ごとに送信
            c.execute(
                'SELECT port FROM identity_management_0 WHERE NOT client_id = ?', [c_id, ])
            for row in c:
                # CoAPで送信
                host = '127.0.0.1'
                port = row[0]
                path = 'print'
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


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('managementserver/', ManagementServerResource())


def func1():
    try:
        # TCPサーバ
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('127.0.0.1', 50000))
        while True:
            serversocket.listen()
            clientsocket, clientaddress = serversocket.accept()
            print(clientaddress)
            payload = clientsocket.recv(1024)
            dict_payload = json.loads(payload.decode())
            print()
            clientsocket.close()

            # 識別子を変数に格納
            c_id = dict_payload['ietf-dots-data-channel:dots-client']['client-id']
            port = dict_payload['ietf-dots-data-channel:dots-client']['signal-channel-port']
            # 識別子管理データベース
            # データベースと接続
            conn = sqlite3.connect('IdentityManagement.db')
            # カーソル作成
            c = conn.cursor()
            # テーブル作成
            c.execute(
                'CREATE TABLE IF NOT EXISTS identity_management_0(client_id PRIMARY KEY, time, port)')
            # プレースホルダ
            p = 'INSERT INTO identity_management_0(client_id, time, port) VALUES(?, ?, ?)'
            # 現在時刻取得
            now = datetime.datetime.now()
            # データ追加
            c.execute(p, (c_id, now, port))
            # コミット
            conn.commit()
            # データを全て出力
            c.execute('SELECT * FROM identity_management_0')
            print(c.fetchall())
            # 接続終了
            conn.close()
    except KeyboardInterrupt:
        serversocket.close()


def func2():
    # CoAPサーバ
    server = CoAPServer('127.0.0.1', 50010)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print('Server Shutdown')
        server.close()
        print('Exiting...')


def main():
    # マルチスレッド
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_2.start()
    thread_1.start()


if __name__ == '__main__':
    main()
