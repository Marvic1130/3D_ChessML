from flask import Flask, jsonify, request
import socket
import threading
import time

app = Flask(__name__)
servers = {}  # Dictionary to track active servers
lock = threading.Lock()  # Thread lock for managing access to the servers dictionary

def socket_server_thread(server_socket, host, port):
    with lock:
        servers[(host, port)] = {"server": server_socket, "active": True}
    print(f"Socket listening on {host} port {port}")

    while servers[(host, port)]["active"]:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data}")
                client_socket.sendall(data)  # Echo the received data
        except socket.error:
            break

    server_socket.close()
    with lock:
        del servers[(host, port)]
    print(f"Socket server on {host} port {port} stopped")

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 0))  # Bind to a free port
    server_socket.listen(1)
    host, port = server_socket.getsockname()
    threading.Thread(target=socket_server_thread, args=(server_socket, host, port)).start()

def handle_request():
    start_socket_server()

@app.route('/start')
def start():
    thread = threading.Thread(target=handle_request)
    thread.start()
    time.sleep(1)  # Delay to ensure the server starts
    with lock:
        host, port = list(servers.keys())[-1]
    return jsonify({"message": "Server is starting", "host": host, "port": port}), 200

@app.route('/stop', methods=['POST'])
def stop():
    data = request.json
    host, port = data['host'], int(data['port'])
    with lock:
        if (host, port) in servers and servers[(host, port)]["active"]:
            servers[(host, port)]["active"] = False
            return jsonify({"message": "Server stopping"}), 200
        else:
            return jsonify({"error": "Server not found"}), 404

@app.route('/list')
def list_servers():
    with lock:
        active_servers = [{"host": host, "port": port} for (host, port), server in servers.items() if server["active"]]
    return jsonify(active_servers), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)