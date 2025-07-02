import threading
from datetime import datetime
import socket
HTTP2_PREFACE = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'
def handle(client_sock):
    try:
        data = client_sock.recv(8192)
        if data[0] == 0x16:  # Handshake
            version_bytes = data[1:3]
            versions = {
                b'\x03\x00': "SSL 3.0",
                b'\x03\x01': "TLS 1.0", 
                b'\x03\x02': "TLS 1.1",
                b'\x03\x03': "TLS 1.2",
                b'\x03\x04': "TLS 1.3"
            }
            version = versions.get(version_bytes, f"UNKNOWN_{version_bytes.hex()}")
            print(f'tls handshake, tls version: {version}')
        if data.startswith(HTTP2_PREFACE):
            print('HTTP/2 without tls')
        print(f'data len: {len(data)}')
        request = data.decode('utf-8', errors='ignore')
        print(f'\n\nrequest prefix\n{request[:1000]}')
        with open('request.txt', 'w') as f:
            f.write(request)
    except Exception as e:
        print(f"handle: parse http/https request: {e}")
    return

if __name__ == "__main__":
    host, port = '0.0.0.0', 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    max_pending = 10 # max length of the queue for pending connections
    server.bind((host, port))
    server.listen(max_pending) # listening
    print(f'server runs on {host}:{port}')
    while True:
        client_sock, client_address = server.accept() # waiting for client request
        print(f"<- {client_address} {str(datetime.now())}")
        t = threading.Thread(target=handle, args=(client_sock,))
        t.daemon = True
        t.start()