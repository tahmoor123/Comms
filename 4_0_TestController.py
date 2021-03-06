import time
import socket
import threading
import UDPNetworkConstants

class ControllerTest(object):
    def __init__(self, ip, port):
        super(ControllerTest, self).__init__()
        self.DATA_HEADER = 'R.1.L.'
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.isRunning = True
        self.sendLocations = []
        self.threads = []
        self.addThreads()

    def addSendLocation(self, ip, port):
        self.sendLocations.append([ip, port])

    def addThreads(self):
        self.threads.append(threading.Thread(target=self.recvThread))
        self.threads.append(threading.Thread(target=self.sendThread))

    def startThreads(self):
        for i in range(len(self.threads)):
            self.threads[i].daemon = True
            self.threads[i].start()

    def recvThread(self):
        print '*Controller Test Recv Thread*'
        while self.isRunning:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            msg = data.split('.')
            # Handle Daemon controls
            print 'msg',data

    def sendThread(self):
        print '*Controller Test Thread*'
        num = 0
        while self.isRunning:
            #1. read status
            if num > 100:
                num = 0
            else:
                num += 1
            print 'num:',num
            for i in range(len(self.sendLocations)):
                self.sendSocket.sendto(self.DATA_HEADER+str(num), (self.sendLocations[i][0],self.sendLocations[i][1]))
            time.sleep(1)

if __name__ == '__main__':
    print 'start Controller Test'
    daemon = ControllerTest(UDPNetworkConstants.CTRL_GAMEPAD_FEEDBACK_RECV[0], UDPNetworkConstants.CTRL_GAMEPAD_FEEDBACK_RECV[1])
    daemon.addSendLocation(UDPNetworkConstants.CTRL_GAMEPAD_SEND[0], UDPNetworkConstants.CTRL_GAMEPAD_SEND[1])
    daemon.startThreads()
    input("block...")