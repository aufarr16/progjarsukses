import socket
import os


def STOR(sock, filename):
    response = sock.recv(1024)
    if response != 'OK':
        print response
    else:
        if os.path.isfile(filename):
            filesize = long(os.path.getsize(filename))
            sock.send(str(filesize))
            with open(filename, 'rb') as f:
                data_sent = f.read(1024)
                sock.send(data_sent)
                while data_sent != "":
                    data_sent = f.read(1024)
                    sock.send(data_sent)
                reply = sock.recv(1024)
                print reply
        else:
            status = '550 File not found'
            print status
            sock.send(status)


def RETR(sock, filename):
    response = sock.recv(1024)
    if str(response)[0] == '(' or str(response)[0] == 'p':
        print response
    else:
        filesize = long(response)
        f = open('new_' + filename, 'wb')
        data = sock.recv(1024)
        data_recieved = len(data)
        f.write(data)
        while data_recieved < filesize:
            data = sock.recv(1024)
            data_recieved = data_recieved + len(data)
            f.write(data)
        print '226 Transfer Complete'


def InputFunc(sock):
    availableCommand = ['DELE', 'USER', 'PASS', 'CWD', 'RETR', 'RMD', 'QUIT', 'STOR', 'MKD', 'HELP', 'PWD', 'LIST', 'RNTO', 'QUIT']
    cmd = raw_input("Enter command: ")
    cmdCheck = cmd.split(" ")[0]
    # print cmd
    if cmdCheck in availableCommand:
        sock.sendall(cmd)
        if cmdCheck == 'RETR':
            cmdArg = cmd.split(" ")[1]
            RETR(sock, cmdArg)
        elif cmdCheck == 'STOR':
            cmdArg = cmd.split(" ")[1]
            STOR(sock, cmdArg)
        elif cmdCheck == 'QUIT':
            sock.close()
            exit()
        else:
            response = sock.recv(1024)
            print response

    else:
        print 'COMMAND NOT FOUND'


def Main():
    host = '127.0.0.1'
    port = 5000
    sock = socket.socket()
    sock.connect((host, port))

    while 1:
        InputFunc(sock)

    #sock.close()


if __name__ == '__main__':
    Main()