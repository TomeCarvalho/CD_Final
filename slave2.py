import time
import base64
import socket
import string
import re
import selectors
import struct

USERNAME = "root"
HOST = "172.17.0.2"
PORT = 8000

from server.const import (
    BANNED_TIME,
    COOLDOWN_TIME,
    NEW_PENALTY,

    MIN_VALIDATE,
    MAX_VALIDATE,

    MIN_TRIES,
    MAX_TRIES,

    PASSWORD_SIZE,

    CHARS
)

class Slave:
    def __init__(self, id: int):
        self.id = id
        
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        sock.sendto('Hello World!', (MCAST_GRP, MCAST_PORT))





        # Create the datagram socket
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # # Set a timeout so the socket does not block indefinitely when trying
        # # to receive data.
        # self.sock.settimeout(0.2)
        # # Set the time-to-live for messages to 1 so they do not go past the
        # # local network segment.
        # ttl = struct.pack('b', 1)
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        # self.sel = selectors.DefaultSelector()
        # self.sel.register(self.sock, selectors.EVENT_READ, self.read)
        # self.sock.sendto(b"amougs", self.multicast_group)
        # self.loop()

    
    def read(self, msg):
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            #break
        else:
            print('received "%s" from %s' % (data, server))

    def send(self, msg):
        self.sock.sendto(msg, self.multicast_group)
        print("sent msg:", msg)

    def loop(self):
        while True:
            events = self.sel.select()

            for key, _ in events:
                callback = key.data

                callback(key.fileobj)


if __name__ == "__main__":
    slave = Slave(1)


# while True:
#     print("all your base are belong to us")
#     time.sleep(1)

#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect((HOST, PORT))
#     psw = "j"
#     #TODO metodo para fazer as passwords
    


#     # ---------------- Enviar o pedido para o server -----------------
#     # Codificacao USERNAME + PASSWORD em base 64 para o protocolo HTTP
#     result = USERNAME + ":" + psw
#     bResults = result.encode("ascii")

#     b64bytes = base64.b64encode(bResults)
#     encoded = b64bytes.decode("ascii")

#     request = "GET / HTTP/1.1\r\nHost:%s\r\n" % HOST
#     request += "Accept: application/json;\r\n"
#     request += "Authorization: Basic " + encoded + "\r\n\r\n"
#     print(f"{request=}")
#     sock.send(request.encode())  
 
#     # response = sock.recv(4096)
#     # http_response = repr(response)
#     # http_response_len = len(http_response)

#     # request += "Authorization: Basic " + encoded + "\r\n\r\n"
#     # print(f"{request=}")
#     # sock.send(request.encode())  
 
#     response = sock.recv(4096)
#     print(f"{response=}")
#     try:
#         resp = re.search(b':"(.*)"', response).group(1)
#         #print("response1:", response)
#         print(f"{resp=}")
#     except:
#         try:
#             response = sock.recv(4096)
#             #print("response2:", response)
#             resp = re.search(b':"(.*)"', response).group(1)
#             print(f"{resp=}")
#         except:
#             print("you just hacked fbi")
    
#     #display the response
#     # print("[RECV] - length: %d" % http_response_len)
#     # print(http_response)

#     # response = sock.recv(4096)
#     # http_response = repr(response) # Na maioria das vezes retorna o json... maioria das vezes
#     # http_response_len = len(http_response)
    
#     #display the response
#     # print("[RECV] - length: %d" % http_response_len)
#     # print(http_response)
#     # print(f"{response=}")
#     # final = "Authorization: Basic " + encoded + "/r/n/r/n"
#     # print(f"{final=}")
#     # final_bytes = str.encode(final)
#     # print(f"{final_bytes=}")
#     # #sock.sendto(b64bytes,(HOST, PORT))
#     # sock.send(final_bytes)
#     # time.sleep(1)
#     #sock.close()
#     break;


