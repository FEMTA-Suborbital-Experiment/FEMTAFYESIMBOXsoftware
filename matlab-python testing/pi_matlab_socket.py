# Test of inter-process communication on the Pi.
# This script opens a socket, and once the Matlab script connects, this script
# listens, prints the data received, and sends back its own data.
# Currently sending arrays of integers back and forth.
# TODO: Make it work consistently; adapt to whatever datatype we need.

import socket
import datetime
#now = datetime.datetime.now

HOST = '127.0.0.1'
PORT = 65535

to_send = [28,29,30,31,32] #must be uint8 at the moment

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Python connected to by', addr)
            #t1 = now()
            data = conn.recv(1024)
            #t2 = now()
            print('Python received', " ".join([str(b) for b in data]))
            conn.sendall(bytes(to_send))
            #print(t2-t1)
