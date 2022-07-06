import time
import base64
import socket
import string
import re
import struct
import json

USERNAME = "root"
HOST = "172.17.0.2"
PORT = 8000
TIMEOUT_TIME = 5000
WAIT_TIME = 2500

from const import (
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

    def recv(self):
        try:
            data, address = self.sock.recvfrom(1024)

            print(f'received {data} bytes from {address}')

            dic = json.loads(data)

            self.interpreterRecv(dic, address)
        except socket.timeout:
            # deu timeout
            pass

    def send(self, dic, addr):
        jDic = json.dumps(dic)
        bDic = jDic.encode(encoding='UTF-8', errors='replace')
        self.sock.sendto(bDic, addr)
    
    def interpreterRecv(self, dic, address):

        if dic["method"] == "HELLO":
            #if address[0] not in self.slave_socks:
            tupl = (address[0], 10000)
            if not tupl in self.slave_socks:
                self.slave_socks.append(tupl)
            print(f"added {address} to the list")
            newDic = {"method": "HELLOREP", "work": self.final_counter - self.initial_counter}
            #bNewDic = newDic.encode(encoding='UTF-8', errors='replace')
            print("Hello response to", address)
            self.send(newDic, address)
            #self.sock.sendto(bNewDic, address)

        elif dic["method"] == "STARTINDEXREQ":
            self.final_counter = int((self.initial_counter + self.final_counter)/2)
            newDic = {"method": "STARTINDEXREP", "index": self.final_counter + 1}
            print("Send index", self.final_counter + 1, "to", address)
            self.send(newDic, address)

        elif dic["method"] == "HELLOREP":
            #print("hellorep")
            self.getNewIndex(dic,address)

        elif dic["method"] == "STARTINDEXREP":
            self.initial_counter = dic["index"]
            newDic = {"method": "ENDINDEXREQ", "index": self.initial_counter}
            print("Sending Start Index:", self.initial_counter, "to everyone")
            for addr in self.slave_socks: # enviar para todos os outros pra retornar o menor
                self.send(newDic, addr)

        elif dic["method"] == "ENDINDEXREQ":
            #if self.isAllowedStart:
            newDic = {"method": "ENDINDEXREP", "index": self.initial_counter}
            print("send FINAL INDEX REP (", self.initial_counter, ") to", address)
            self.send(newDic, address)

        elif dic["method"] == "ENDINDEXREP":
            idx = dic["index"]
            self.isAllowedStart = True
            #print("you can start the algorithm now :)")
            if idx > self.initial_counter and idx < self.final_counter:
                self.final_counter = idx
                print("FINAL INDEX updated to", idx)

        elif dic["method"] == "SUCCESS":
            self.endCode()

    def getNewIndex(self, dic, addr):
        work = dic["work"]
        if work > self.workValue:
            self.workValue = work
            self.selectedWork = addr

    def endCode(self):
        #self.server.close()
        #self.sock.close()
        quit()

    def sendPass(self, psw):
        result = USERNAME + ":" + psw
        bResults = result.encode("ascii")

        b64bytes = base64.b64encode(bResults)
        encoded = b64bytes.decode("ascii")

        request = "GET / HTTP/1.1\r\nHost:%s\r\n" % HOST
        request += "Accept: application/json;\r\n"
        request += "Authorization: Basic " + encoded + "\r\n\r\n"
        #print(f"{request=}")
        self.server.send(request.encode())  

    def confirmPass(self, timeout=0.2):
        self.server.setblocking(False)

        total_data=[]
        data=''

        begin=time.time()
        while True:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break

            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break

            #recv something
            try:
                data = self.server.recv(8192)
                if data:
                    total_data.append(data.decode("utf-8"))
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass

        #join all parts to make final string
        final_resp = ''.join(total_data)
        #print(f"{final_resp=}")
        idx = final_resp.find('200 OK')
        #print(f"{idx=}")
        return idx != -1

        # response = self.server.recv(160)
        # #print(f"{response=}")
        # strRes = response.decode("utf-8")
        # idx = strRes.find('Internal Server Error')
        # response2 = self.server.recv(25)
        # strRes2 = response2.decode("utf-8")
        # idx2 = strRes2.find('Internal Server Error')
        # return idx != -1
        # print(f"{strRes=}")
        # print(f"{idx=}")
        # print(f"{strRes2=}")
        # print(f"{idx2=}")
        # return idx != -1




        # try:
        #     resp = re.search(b':"(.*)"', response).group(1)
        #     #print("response1:", response)
        #     print(f"{resp=}")
        # except:
        #     try:
        #         response = sock.recv(4096)
        #         #print("response2:", response)
        #         resp = re.search(b':"(.*)"', response).group(1)
        #         print(f"{resp=}")
        #     except:
        #         print("you just hacked fbi")

    def passCracker(self):
        #TODO: tentativas password algorithm
        while True:
            if self.initial_counter < self.final_counter:
                print("START INDEX:", self.initial_counter)
                print("END INDEX:", self.final_counter)
                print(f"{self.server}")
                tempo = 0
                #print(tempo)    
                contador = 0
                isCorrect = False
                for i in range(self.initial_counter, self.final_counter + 1):
                    if contador >= MIN_TRIES or isCorrect:
                        break
                    psw = ""
                    for n in range(PASSWORD_SIZE - 1, 0, -1):
                        psw += self.chars[(i // self.length**n) % self.length]
                    psw += self.chars[i % self.length]
                    #psw = "K"
                    print(f"{psw=}")
                    self.sendPass(psw) # enviar psw para o http
                    isCorrect = self.confirmPass()
                    contador += 1

                #TODO: receive after  min_tries
                if not isCorrect:
                    tempo = time.time()
                    self.initial_counter += contador

                    while time.time() - tempo < COOLDOWN_TIME/1000: 
                        # enquanto espera o cooldown, verificar o que ta na socket
                        self.recv()
                        pass
                else:
                    print("SENHA (", psw, ") DESCODIFICADA!")
                    newDic = {"method": "SUCCESS"}

                    #TODO guardar imagem

                    for sl in self.slave_socks:
                        self.send(newDic, sl)
                    self.endCode()
            else: 
                # se self.initial_counter >= self.final_counter
                # se eu cheguei aqui, e pq todas as minhas passwords falharam
                # verificar quem esta mais overworked e pedir para dividir
                self.workValue = 0
                self.selectedWork = None
                newDic = {"method": "HELLO"}
                print("HELLO TO EVERYONE")
                for sl in self.slave_socks:
                    self.send(newDic, sl)
                tempo = time.time()
                while time.time() - tempo < WAIT_TIME/1000:
                    #enquanto estiver em um limite de tempo
                    self.recv()
                    # try:
                    #     data, address = self.sock.recvfrom(1024)

                    #     print(f'received {data} bytes from {address}')

                    #     dic = json.loads(data)

                    #     self.interpreterRecv(dic, address)
                    # except socket.timeout:
                    #     # deu timeout
                    #     pass
                # tempo de espera passou, hora de mudar
                if self.selectedWork is None:
                    # alguem morreu, pois todos devem ter acabado e ainda nao deu certo
                    # TODO ver quais index que foram perdidos
                    print("i think that someone just died :(")
                    pass
                else:
                    self.send({"method": "STARTINDEXREQ"}, self.selectedWork)
                    final = self.final_counter
                    while self.initial_counter >= self.final_counter and time.time() - tempo < WAIT_TIME/1000:
                        self.recv()
                    
                    if self.final_counter < self.initial_counter:
                        self.final_counter = self.length ** PASSWORD_SIZE
                        
                    tempo = time.time()
                    while time.time() - tempo < WAIT_TIME/1000:
                        self.recv()

                    self.server.close()
                    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.server.connect((HOST, PORT))

    def __init__(self):

        #self.banned = False
        #self.banned_time = 0
        self.slave_socks = []
        self.initial_counter = 0
        self.chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        self.length = len(self.chars)
        #self.final_counter = (self.length - 1) ** PASSWORD_SIZE
        self.final_counter = self.length ** PASSWORD_SIZE
        #self.original = True
        self.isAllowedStart = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((HOST, PORT))

        print(self.final_counter)
        #message = b'very important data'
        # --------------------- <MULTICAST MAGIC LOL> ------------------------
        self.multicast_group = ('224.3.29.71', 10000)
        self.server_address = ('', 10000)

        # Create the datagram socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        self.sock.settimeout(1) # 1 seg parece ser um tempo bom para as sockets quando run -d
        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        self.sock.bind(self.server_address)
        multicast_group2 = '224.3.29.71'

        group = socket.inet_aton(multicast_group2)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # --------------------- </MULTICAST MAGIC LOL> ------------------------

        self.id = socket.gethostbyname(socket.gethostname())
        print(f"Worker with IP: {self.id}")
        self.workValue = 0
        self.selectedWork = None
        try:
        # Send data to the multicast group
            dic = json.dumps({"method": "HELLO"})
            bDic = dic.encode(encoding='UTF-8', errors='replace')
            sent = self.sock.sendto(bDic, self.multicast_group)

            # Look for responses from all recipients
            
            while True:
                #print('waiting to receive')
                try: # server -> sender
                    data, server = self.sock.recvfrom(1024)
                    if server[0] != self.id and server[0] not in self.slave_socks:
                        print(f"added {server} to the list")
                        self.slave_socks.append(server)
                        self.isAllowedStart = False # precisa verificar os indices antes de comecar
                        #self.original = False # se recebeu mensagem de alguem, nao e o lider

                except socket.timeout:
                    #print('timed out, no more responses')
                    break
                else:
                    if (server[0] != self.id):
                        print(f'received "{data}" from {server}')
                        dic = json.loads(data)
                        #print(f"{dic=}")
                        self.interpreterRecv(dic,server)
                        #if dic["method"] == "HELLOREP":
                        #print("hellorep")
                        #    self.getNewIndex(dic,server)

                    
                    #self.slave_socks.append(server)

        except Exception as e:
            print(e)


        ## ------------------------ RECEIVE MESSAGE ------------------- ##

        finally:

            if self.workValue > 0:
                print("send START INDEX REQUEST to", self.selectedWork)
                self.send({"method": "STARTINDEXREQ"}, self.selectedWork)
            else:
                self.isAllowedStart = True

            #while not self.isAllowedStart:
                # enquanto nao for permitido comecar (ou seja, o index deve ser corrigido, mas ainda nao foi feito)

                #self.sock.settimeout(None)cl; docker run -ti --env PASSWORD_SIZE=1 --name worker2 projecto_final
            print(self.slave_socks)
            print("posso comecar?", self.isAllowedStart)
            while not self.isAllowedStart:
                #print('\nwaiting to receive message')
                self.recv()
                # try:
                #     data, address = self.sock.recvfrom(1024)

                #     #print(f'received {data} bytes from {address}')

                #     dic = json.loads(data)

                #     self.interpreterRecv(dic, address)
                # except socket.timeout:
                #     # deu timeout
                #     pass

            ## Se chegou ate aqui, it's algorithm time 😎

            self.passCracker()

                #print('sending acknowledgement to', address)
                #self.sock.sendto(b'ack', address)
    # def send(self, msg):
    #     self.sock.sendto(msg, self.multicast_group)
    #     print("sent msg:", msg)

    # def loop(self):
    #     while True:
    #         print("hehe")
    #         break;



slave = Slave()


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


