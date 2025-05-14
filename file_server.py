#!/usr/bin/env python3
import socket
import os

HOST, PORT = '0.0.0.0', 9999  # 모든 IP에서 접속 허용, 포트 9999 사용

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        # 포트 재사용 옵션 설정
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 주소와 포트 바인드
        srv.bind((HOST, PORT))
        # 클라이언트 1명 대기
        srv.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT}")

        # 클라이언트 연결 수락
        conn, addr = srv.accept()
        with conn:
            print(f"[Server] Connection from {addr}")

            # 1) 클라이언트 요청 받기 (예: "GET filename\n")
            req = b''
            while not req.endswith(b'\n'):
                chunk = conn.recv(1)
                if not chunk:
                    return  # 연결 끊김
                req += chunk

            # 2) 요청 파싱
            _, filename = req.decode().strip().split()

            # 3) 파일 존재 여부 확인 및 열기
            if not os.path.isfile(filename):
                conn.sendall(b"ERROR File not found\n")
                return

            data = open(filename, 'rb').read()

            # 4) OK 헤더 전송
            header = f"OK {len(data)}\n".encode()
            conn.sendall(header)

            # 5) 파일 본문 전송
            conn.sendall(data)

            print(f"[Server] Sent {filename} ({len(data)} bytes)")

if __name__ == '__main__':
    main()

