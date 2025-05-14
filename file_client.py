#!/usr/bin/env python3
import socket

HOST, PORT = '127.0.0.1', 9999  # 서버 주소 및 포트

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((HOST, PORT))

        # 1) 다운로드 요청 보내기
        filename = 'downloaded.bin'  # 요청할 파일명
        cli.sendall(f"GET {filename}\n".encode())
        print(f"[Client] Sent request: GET {filename}")

        # 2) 헤더 읽기 (한 줄)
        header = b''
        while not header.endswith(b'\n'):
            chunk = cli.recv(1)
            if not chunk:
                print("[Client] No response from server.")
                return
            header += chunk

        line = header.decode().rstrip('\n')
        # status 와 rest (메시지 또는 길이) 분리
        status, rest = line.split(' ', 1)

        # 3) 서버 응답 처리
        if status == 'OK':
            # 파일 길이 파싱
            length = int(rest)
            print(f"[Client] Server OK, length = {length}")

            # 4) 본문 읽기
            data = b''
            while len(data) < length:
                data += cli.recv(length - len(data))

            # 5) 파일로 저장
            out_name = 'downloaded_' + filename
            with open(out_name, 'wb') as f:
                f.write(data)
            print(f"[Client] Saved {out_name} ({length} bytes)")

        elif status == 'ERROR':
            # 서버 에러 메시지 출력
            print(f"[Client] Download failed: {rest}")

        else:
            # 알 수 없는 응답 처리
            print(f"[Client] Unknown response: {line}")

if __name__ == '__main__':
    main()

