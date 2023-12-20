from flask import Flask, jsonify, request
import threading
from websocket_server import WebsocketServer
import time

app = Flask(__name__)
servers = {}  # 서버 인스턴스를 추적하는 딕셔너리

def new_client(client, server):
    print(f"Connected new socket: {client['address']}")

def message_received(client, server, message):
    print(f"Received message from {client['address']}: {message}")
    server.send_message(client, message)

def start_websocket_server():
    host = '127.0.0.1'
    server = WebsocketServer(port=0, host=host)
    server.set_fn_new_client(new_client)  # 새로운 클라이언트 연결 콜백 설정
    server.set_fn_message_received(message_received)

    actual_port = server.server_address[1]  # 실제 할당된 포트 번호
    servers[(host, actual_port)] = server
    server.run_forever()

@app.route('/start')
def start():
    thread = threading.Thread(target=start_websocket_server)
    thread.start()
    time.sleep(1)
    host, port = list(servers.keys())[-1]
    return jsonify({"message": "WebSocket server started", "host": host, "port": port}), 200

@app.route('/stop', methods=['DELETE'])
def stop():
    data = request.json
    host, port = data['host'], int(data['port'])

    if (host, port) in servers:
        server = servers[(host, port)]
        server.server_close()
        del servers[(host, port)]
        return jsonify({"message": "WebSocket server stopped"}), 200
    else:
        return jsonify({"error": "Server not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
