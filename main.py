import socket
import threading

sock = socket.socket()



def connect(s, cn_l):
    while True:
        try:
            data = s.recv(1024)
            if data:
                print("info from " + str(addr) + ' message: ' + data.decode('utf-8'))
            for cn in cn_l:
                cn.send(data.upper())
        except Exception as e:
            print("Vse pizda")
            break

sock.bind(('', 9090))
sock.listen(2)
conn_list = []
cn_l = []
while True:
    conn, addr = sock.accept()
    cn_l.append(conn)
    t = threading.Thread(target=connect, args=(conn, cn_l))
    t.start()

t.join()
conn.close()
