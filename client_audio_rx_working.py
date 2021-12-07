import socket
import alsaaudio
import threading



host = '172.16.81.92'

port_rx = 3007
port_tx = 3008


client_socket_rx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_tx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)


client_socket_rx.connect((host,port_rx))

client_socket_tx.connect((host,port_tx))



device = 'default'
audio_out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, channels = 1, rate = 44100, format = alsaaudio.PCM_FORMAT_S8, periodsize = 160, device = device)
audio_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels = 1, rate = 44100, format = alsaaudio.PCM_FORMAT_S8,  periodsize = 160, device = device)



def recieve_audio():
    while True:
        
    
        data = client_socket_rx.recv(1024)
 #       print(data)
        audio_out.write(data)
    client_socket_rx.close()



def transmit_audio():
    while True:

        data = audio_in.read()
 #       print(1)
        if len(data)>0:
  #          print(data[1]) 
           client_socket_tx.send(data[1])
#    client_socket_tx.close()


recieve_thread = threading.Thread(target=recieve_audio)
recieve_thread.start()
#recieve_audio()
transmit_audio()


