from cProfile import run
import sys
import zmq
import os
import time


def run_client(data):

    try:
        context = zmq.Context()

        # Socket to talk to server
        # print("Connecting to server(receiver) …")
        socket = context.socket(zmq.REQ)
        # socket.connect("tcp://localhost:5555")
        socket.connect("tcp://192.168.86.30:5555")

        # send a message
        # data = "7"
        socket.send_string(str(data))
        # print("[***] Sent message to server(receiver): ", data)

        # Get the reply.
        message = socket.recv()
        # print(f"Received reply from server(receiver) confirming: \n"
        #       f"Received the message: "
        #       f"{message.decode('utf-8')}")
        time.sleep(1)
    except KeyboardInterrupt:
        socket.close()
    finally:
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        context.term()

    decoded_msg = message.decode('utf-8')
    print(decoded_msg, end='')
    # return decoded_msg


def main(data):
    answer = run_client(data)
    return answer


if __name__ == "__main__":

    input = sys.argv[1]
    run_client(input)
    #     os._exit(0)
