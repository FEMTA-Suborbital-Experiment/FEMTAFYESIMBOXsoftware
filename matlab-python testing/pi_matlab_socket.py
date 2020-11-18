import socket
import datetime
now = datetime.datetime.now

HOST = '127.0.0.1'
PORT = 65535

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        t1 = now()
        s.bind((HOST,PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by ', addr)
            while True:
                data = conn.recv(1024)
                dat = data.decode()
                if not data:
                    break
                print('Received ', ord(dat))
                conn.sendall(data)
                t2 = now()
                print(t2-t1)
