import socket


def InputFunc(sock):
    availableCommand = ['DELE', 'USER', 'PASS', 'CWD', 'RETR', 'RMD', 'QUIT']
    cmd = raw_input("Enter command: ")
    cmdCheck = cmd.split(" ")[0]

    if cmdCheck in availableCommand:
        sock.send(cmd)
        response = sock.recv(1024)
        print response

    else:
        print 'COMMAND NOT FOUND'


def Main():
    host = '127.0.0.1'
    port = 5000
    sock = socket.socket()
    sock.connect((host, port))

    InputFunc(sock)

    sock.close()


if __name__ == '__main__':
    Main()