import time
import zmq
import random


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Microservice


def ran_num_gen(input_int):
    int_str = ''
    num = list()
    int_num = 1
    while int_num <= input_int:
        num.append(int_num)
        int_num += 1

    random.shuffle(num)

    int_str = ','.join(str(x) for x in num)

    return int_str


# Communication piping
while True:
    #  Wait for next request from client
    print('Waiting for messages. To exit press CTRL+C')
    message = socket.recv()

    message_int = int(message)  # change string to integer
    print("[***] Received integer: ", message_int)
    random_num = ran_num_gen(message_int)
    print("[***] Generated random numbers : ", random_num)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client as string
    socket.send_string(random_num)
