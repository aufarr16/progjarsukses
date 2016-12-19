import socket
import threading
import os

workingDir = ''


def CWD(sock, dirname):
    global workingDir
    dir = os.getcwd()
    myDir = dir + workingDir + '\\' + dirname
    if os.path.exists(myDir):
        workingDir = '\\'+dirname
        status = '250 Directory changed successfully, new dir: '+workingDir
        print status
        sock.send(status)
    else:
        status = '550 Directory not found'
        print status
        sock.send(status)


def DELE(sock, filename):
    dir = os.getcwd()
    deleteme = dir+workingDir+'\\'+filename
    if os.path.exists(deleteme):
        os.remove(deleteme)
        status = '250 File deleted successfully'
        print status
        sock.send(status)
    else:
        status = '550 File not found'
        print status
        sock.send(status)


def RMD(sock, dirname):
    dir = os.getcwd()
    deleteme = dir + '\\' + dirname
    if os.path.exists(deleteme):
        os.rmdir(deleteme)
        status = '250 Directory deleted successfully'
        print status
        sock.send(status)
    else:
        status = '550 Directory not found'
        print status
        sock.send(status)


def InputFunc(message, sock):
    message = sock.recv(1024)
    print message
    command = message.split(" ")[0]
    argument = message.split(" ")[1]

    if command == 'DELE':
        DELE(sock, argument)
    elif command == 'RMD':
        RMD(sock, argument)
    elif command == 'CWD':
        CWD(sock, argument)
    else:
        sock.send('UNKNOWN COMMAND')


def Main():
    host = '127.0.0.1'
    port = 21

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print "FTP Server Started."
    while True:
        c, addr = s.accept()
        print "client connedted ip: " + str(addr)
        t = threading.Thread(target=InputFunc, args=("InputFunction", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()