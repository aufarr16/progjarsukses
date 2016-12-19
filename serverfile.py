import socket
import threading
import os
import select

workingDir = ''
user = ['progjar:progjar', 'testing:123']
username = 'progjar'
password = 'progjar'
session = '(not logged in)'
loggedIn = 0


def USER(sock, login):
    global username, password, loggedIn, session
    if login == username:
        session = login
        response = session+'> 331 Password required for '+login
        print response
        sock.send(response)
    else:
        response = session+'> 530 Login or password incorrect'
        print response
        sock.send(response)


def PASS(sock, login):
    global username, password, loggedIn, session
    if login == password and session == username:
        loggedIn = 1
        response = session+'> 230 Logged on'
        print response
        sock.send(response)
    else:
        response = session+'> 530 Login or password incorrect'
        print response
        sock.send(response)


def CWD(sock, dirname):
    global workingDir, loggedIn
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        myDir = dir + workingDir + '\\' + dirname
        if os.path.isdir(myDir):
            workingDir = '\\'+dirname
            status = session+'> 250 Directory changed successfully, new dir: '+workingDir
            print status
            sock.send(status)
        else:
            status = session+'> 550 Directory not found'
            print status
            sock.send(status)


def DELE(sock, filename):
    global loggedIn
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        deleteme = dir+workingDir+'\\'+filename
        if os.path.isfile(deleteme):
            os.remove(deleteme)
            status = session+'> 250 File deleted successfully'
            print status
            sock.send(status)
        else:
            status = session+'> 550 File not found'
            print status
            sock.send(status)


def RMD(sock, dirname):
    global loggedIn
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        deleteme = dir + '\\' + dirname
        if os.path.isdir(deleteme):
            os.rmdir(deleteme)
            status = session+'> 250 Directory deleted successfully'
            print status
            sock.send(status)
        else:
            status = session+'> 550 Directory not found'
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
    elif command == 'USER':
        USER(sock, argument)
    elif command == 'PASS':
        PASS(sock, argument)
    else:
        sock.send('500 Internal server error')


def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print "FTP Server Started."
    while True:
        c, addr = s.accept()
        # print "client connedted ip: " + str(addr)
        t = threading.Thread(target=InputFunc, args=("InputFunction", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()