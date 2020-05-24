import json
import socket
import sys

from coapthon.client.helperclient import HelperClient


def main():
    # JSONメッセージを作成
    client_id = int(sys.argv[1])
    registration_request = {
        "ietf-dots-data-channel:dots-client":
        {
            "client-id": client_id
        }
    }
    data = json.dumps(registration_request)

    # TCPで送信
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', int(sys.argv[3])))
    clientsocket.send(data.encode())
    clientsocket.close()

    # 緩和要請のJSONファイル読み込み
    with open(sys.argv[2], 'r') as f:
        mitigation_request = json.dumps(json.load(f))

    # 緩和要請の送信許可
    while True:
        answer = input('緩和要請を送信しますか？（y/n）：　')
        if answer == 'y':
            break
        elif answer == 'n':
            sys.exit()
        else:
            pass

    # CoAPのPUTメソッドで送信
    host = '127.0.0.1'
    port = int(sys.argv[4])
    path = 'dotsserver'
    payload = mitigation_request

    client = HelperClient(server=(host, port))
    try:
        response = client.put(path, payload)
        print(response.pretty_print())
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()


if __name__ == '__main__':
    main()
