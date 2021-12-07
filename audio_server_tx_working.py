#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import alsaaudio
import threading


print('started')
host = '' # for connection to any ip
port_tx = 3007 # initiate port no above 1024
port_rx = 3008


#SOCK_STREAM - TCP
#SOCK_DGRAM - UDP
server_socket_tx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_rx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket_tx.bind((host, port_tx))  # bind host address and port together
server_socket_tx.listen(1)


server_socket_rx.bind((host, port_rx))  # bind host address and port together
server_socket_rx.listen(1)


conn_tx, address_tx = server_socket_tx.accept()  # accept new connection
conn_rx, address_rx = server_socket_rx.accept()




print("Connection from: " + str(address_tx))



device = 'default'
audio_out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, channels=1, rate=44100,
                          format=alsaaudio.PCM_FORMAT_S8, periodsize=160, device=device)


audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK,
                         channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_S8, 
                         periodsize=160, device=device)




def transmit_audio():
    while True:
        data = audio_in.read()
#        print(data)
#        if len(data[1])>0:
        conn_tx.send(data[1])  # send data to the client

    conn_tx.close()  # close the connection




def recieve_audio():
    while True:
        data  = conn_rx.recv(1024)
#        print(data)
        audio_out.write(data)

    conn_rx.close()



#recieve_audio()
recieve_thread = threading.Thread(target = recieve_audio)
recieve_thread.start()
transmit_audio()
