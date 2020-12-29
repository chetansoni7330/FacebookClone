import socket
import os
import subprocess
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

global s
global host
global port

def create_socket():
    global s
    global host
    global port
    s = socket.socket()
    host = '192.168.43.246'
    port = 9999

def connection():
    global host
    global port
    s.connect((host, port))

def recv_commands():
    global s
    while True:
        data = s.recv(1024)

        if len(data) > 0:
            print(data[:].decode("utf-8"))

        

def send_commands():
    global s
    while True:
        inp = input('turtle> ')
        s.send(str.encode(inp))


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            connection()
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