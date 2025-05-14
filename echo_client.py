import socket

HOST = '127.0.0.1'       # 접속할 서버 주소 (localhost)
PORT = 11111             # 접속할 서버의 포트 번호 (서버와 동일하게 설정)

# 소켓 생성 (IPv4, TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결 요청
client_socket.connect((HOST, PORT))
print(f"서버 {HOST}:{PORT}에 연결되었습니다.")

try:
    while True:
        msg = input("서버로 보낼 메시지 입력 (종료는 quit): ")
        if not msg:
            continue        # 빈 문자열이면 다시 입력
        if msg.lower() == 'quit':
            print("quit 명령을 받아 클라이언트를 종료합니다.")
            break

        # 입력한 문자열을 서버로 전송
        client_socket.sendall(msg.encode('utf-8'))

        # 서버로부터 응답 수신
        data = client_socket.recv(1024)
        if not data:
            # 서버가 연결을 종료함
            print("서버와의 연결이 종료되었습니다.")
            break

        # 수신한 바이트를 문자열로 변환하여 출력
        received_str = data.decode('utf-8')
        print(f"서버로부터 응답: {received_str}")

finally:
    # 소켓 닫기
    client_socket.close()

