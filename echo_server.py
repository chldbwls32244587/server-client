import socket

HOST = '127.0.0.1'      
PORT = 11111
# 소켓 생성 (IPv4(AF_INET), TCP(SOCK_STREAM) 소켓)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 포트 재사용 옵션 설정 (옵션): 서버를 재시작할 때 주소 사용 중 오류 방지
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 소켓을 지정한 HOST와 PORT에 바인드 (결합)합니다.
server_socket.bind((HOST, PORT))

# 클라이언트의 연결 요청을 받을 준비를 합니다 (리스닝 시작).
server_socket.listen()

print(f"Echo 서버 시작: {HOST}:{PORT}에서 클라이언트 연결 대기중...")

# 클라이언트가 연결을 시도할 때까지 대기합니다.
client_socket, client_addr = server_socket.accept()      # 연결 수락
print(f"{client_addr}와 연결되었습니다.")              # 클라이언트 주소 출력

# 연결된 클라이언트와 데이터 주고받기 (Echo loop)
while True:
    # 클라이언트가 보낸 메시지를 수신합니다.
    data = client_socket.recv(1024)                      # 최대 1024바이트 읽기
    if not data:
        # 수신된 데이터가 없으면 (연결 종료 신호), 루프 종료
        break

    # 수신된 데이터를 문자열로 변환하고 콘솔에 출력합니다.
    received_str = data.decode('utf-8')
    print(f"클라이언트로부터 받은 메시지: {received_str}")

    # 받은 내용을 다시 클라이언트로 전송 (에코)
    client_socket.sendall(data)

# 루프를 나왔으면 클라이언트 연결이 종료된 상태입니다.
print("클라이언트 연결 종료. 서버를 종료합니다.")
server_socket.close()

