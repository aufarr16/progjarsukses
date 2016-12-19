import socket


def InputFunc(sock):
    availableCommand = ['DELE', 'PWD', 'USER', 'PASS' ,'CWD', 'RETR', 'DELE', 'RMD']
    cmd = raw_input("Enter command: ")
    cmdCheck = cmd.split(" ")[0]

    if cmdCheck in availableCommand:
        sock.send(cmd)
        response = sock.recv(1024)
        print response

    else:
        print 'COMMAND NOT FOUND'
        InputFunc(sock)


def Main():
    host = '127.0.0.1'
    port = 21

    sock = socket.socket()
    sock.connect((host, port))

    # input function
    InputFunc(sock)

    sock.close()


if __name__ == '__main__':
    Main()