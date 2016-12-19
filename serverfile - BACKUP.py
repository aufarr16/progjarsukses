import socket
import threading
import os
import select

workingDir = ''
user = ['progjar:progjar', 'testing:123']
username = 'a'
password = 'a'
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
    global workingDir, loggedIn, session
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        myDir = dir + workingDir + '\\' + dirname
        if os.path.isdir(myDir):
            workingDir = '\\' + dirname
            status = session+'> 250 Directory changed successfully, new dir: '+workingDir
            print status
            sock.send(status)
        else:
            status = session+'> 550 Directory not found'
            print status
            sock.send(status)


def DELE(sock, filename):
    global loggedIn, session
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        deleteme = dir + workingDir + '\\' + filename
        if os.path.isfile(deleteme):
            os.remove(deleteme)
            status = session+'> 250 File deleted successfully'
            print status
            sock.send(status)
        else:
            status = session+'> 550 File not found'
            print status
            sock.send(status)


def STOR(sock, filename):
    global loggedIn, session
    if loggedIn == 0:
        status = session + '> 332 Need account for login'
        print status
        sock.send(status)
    else:
        sock.send('OK')
        response = sock.recv(1024)
        if str(response)[0] == '5':
            print session+'> '+response
        else:
            filesize = long(response)
            f = open(workingDir + "\\" + 'new_' + filename, 'wb')
            data = sock.recv(1024)
            data_recieved = len(data)
            f.write(data)
            while data_recieved < filesize:
                data = sock.recv(1024)
                data_recieved = data_recieved + len(data)
                f.write(data)
            status = session + '> 226 Transfer complete'
            print status
            sock.send(status)


def RETR(sock, filename):
    global loggedIn, session
    if loggedIn == 0:
        status = session + '> 332 Need account for login'
        print status
        sock.send(status)
    else:
        if os.path.isfile(filename) and os.path.exists(filename):
            file_size = long(os.path.getsize(filename))
            sock.send(str(file_size))
            with open(filename, 'rb') as f:
                data_sent = f.read(1024)
                sock.send(data_sent)
                while data_sent != "":
                    data_sent = f.read(1024)
                    sock.send(data_sent)
                status = session+'> 226 Transfer complete'
                print status
                sock.send(status)
        else:
            # print "No such file"
            status = session + '> 550 File not found'
            print status
            sock.send(status)


def RMD(sock, dirname):
    global loggedIn, session
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        deleteme = dir + workingDir + '\\' + dirname
        # deleteme = dir + '\\' + dirname
        if os.path.isdir(deleteme):
            os.rmdir(deleteme)
            status = session+'> 250 Directory deleted successfully'
            print status
            sock.send(status)
        else:
            status = session+'> 550 Directory not found'
            print status
            sock.send(status)


def MKD(sock, dirname):
    global loggedIn, session
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:
        dir = os.getcwd()
        makedir = dir + workingDir + '\\' + dirname
        if os.path.exists(makedir):
            status = session + '> 550 Directory already exists'
            print status
            sock.send(status)
        else:
            os.mkdir(makedir)
            status = session+'> 257 Directory created'
            print status
            sock.send(status)


def PWD(sock):
    global loggedIn, session
    if loggedIn == 0:
        status = session+'> 332 Need account for login'
        print status
        sock.send(status)
    else:

        dir = os.getcwd() + workingDir
        status = session + "> 257 \"" + dir + "\" is current directory"
        print status
        sock.send(status)


def HELP(sock):
    sock.send("214 The Function that you can input are\nUSER\nPASS\nCWD\nQUIT\nRETR\nSTOR\nRNTO\nDELE\nRMD\nMKD\nPWD\nLIST\nHELP")


def RNTO(sock, source, destination):
    global loggedIn, session
    if loggedIn == 0:
        status = session + '> 332 Need account for login'
        print status
        sock.send(status)
    else:
        # cwd = os.getcwd()
        if os.path.isfile(source):
            os.rename(source, destination)
            sock.send("250 File Renamed")
        else:
            sock.send("550 File not found")



def LIST(sock):
    global loggedIn, session
    if loggedIn == 0:
        status = session + '> 332 Need account for login'
        print status
        sock.send(status)
    else:
        cwd = os.getcwd()
        listfile = '\n'
        direct = os.listdir(cwd + '/')
        for files in direct:
            if direct == '':
                break
            listfile = listfile + files + '\n'
        status = session+"> 150 List of file inside " + cwd + listfile + "216 Directory send OK"
        print status
        sock.send(status)


def QUIT():
    global session, loggedIn
    status = session+'> 221 Goodbye'
    print status
    session = '(not logged in)'
    loggedIn = 0


def InputFunc(message, sock):
    message = sock.recv(1024)
    print message
    command = message.split(" ")[0]

    if command == 'DELE':
        argument = message.split(" ")[1]
        DELE(sock, argument)
    elif command == 'RMD':
        argument = message.split(" ")[1]
        RMD(sock, argument)
    elif command == 'CWD':
        argument = message.split(" ")[1]
        CWD(sock, argument)
    elif command == 'USER':
        argument = message.split(" ")[1]
        USER(sock, argument)
    elif command == 'PASS':
        argument = message.split(" ")[1]
        PASS(sock, argument)
    elif command == 'RETR':
        argument = message.split(" ")[1]
        RETR(sock, argument)
    elif command == 'STOR':
        argument = message.split(" ")[1]
        STOR(sock, argument)
    elif command == 'MKD':
        argument = message.split(" ")[1]
        MKD(sock, argument)
    elif command == 'RNTO':
        argument1 = message.split(" ")[1]
        argument2 = message.split(" ")[2]
        RNTO(sock, argument1, argument2)
    elif command == 'HELP':
        HELP(sock)
    elif command == 'PWD':
        PWD(sock)
    elif command == 'LIST':
        LIST(sock)
    elif command == 'QUIT':
        QUIT(sock)
    else:
        status = '500 Internal server error'
        print status
        sock.send(status)


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