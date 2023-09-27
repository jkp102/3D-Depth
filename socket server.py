import socket

def run_server():
    # 호스트와 포트를 지정합니다.
    HOST = '172.16.1.99'  # 로컬 호스트
    PORT = 6000  # 사용할 포트 번호

    # 소켓 객체를 생성합니다.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 포트에 바인딩합니다.
    server_socket.bind((HOST, PORT))

    # 클라이언트의 접속을 대기합니다.
    server_socket.listen(1)
    print('클라이언트 연결 대기 중...')

    # 클라이언트의 연결 요청을 수락합니다.
    client_socket, addr = server_socket.accept()
    print('클라이언트가 연결되었습니다:', addr)

    while True:
        # 클라이언트로부터 데이터를 받습니다.
        data = client_socket.recv(1024)
        if not data:
            break

        # 수신한 데이터를 출력합니다.
        print('수신한 데이터:', data.decode())

        # 데이터를 클라이언트로 전송합니다.
        message = "1111111"
        client_socket.sendall(message.encode())
        print('송신한 데이터:', message)
    # 소켓을 닫습니다.
    client_socket.close()
    server_socket.close()

# 서버를 계속해서 실행하도록 합니다.
while True:
    run_server()
