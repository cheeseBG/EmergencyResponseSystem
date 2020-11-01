import socket
import re
from gesture import define_gesture, find_gesture, handedness, calculate

# Dictionary of gesture
# gesture_dict = {[1, 0, 1, 1, 1]: "one"}

# Local host address
HOST = '127.0.0.1'

# Port num
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, addr = server_socket.accept()

print('Connected by', addr)

while True:
    data = client_socket.recv(2048)
    idx = 1

    landmark = []
    landmark_list = []

    if not data:
        break

    for i in data.decode().split():
        is_num = bool(re.findall('\d+', i))
        if is_num is True:
            landmark.append(float(i))

        if len(landmark) == 3:
            landmark_list.append(landmark)
            landmark = []
    #print("*************\n", data.decode())
    print(define_gesture(landmark_list))
    print(find_gesture(define_gesture(landmark_list)))
    print(handedness(landmark_list[0], landmark_list[1]))
    #print(calculate(landmark_list))

client_socket.close()
server_socket.close()