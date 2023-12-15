import socket
import json
import requests

# Flask 앱의 /start 엔드포인트를 호출하여 서버를 시작
response = requests.get("http://127.0.0.1:5000/start")
data = response.json()

host = data["host"]
port = data["port"]
print(f"Connecting to server at {host} port {port}")

# 소켓 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# 데이터 전송 및 응답 수신
test_message = "Hello, Server!"
client_socket.sendall(test_message.encode())

received_data = client_socket.recv(1024).decode()
print(f"Received: {received_data}")

# 소켓 닫기
client_socket.close()
post_data = {"host": host, "port": port}
response = requests.post("http://127.0.0.1:5000/stop", json=post_data)
print(response.json())
# 서버의 응답이 전송한 데이터와 일치하는지 확인
assert test_message == received_data, "Echoed message does not match the sent message"
print("Test Passed: Sent and received messages match.")