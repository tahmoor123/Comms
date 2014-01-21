import time
import pygame
from pygame.locals import *
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
DRIVER_COMMANDS = False
MODEL_DRIVE_LEFT  = '0'
MODEL_DRIVE_RIGHT = '1'
MODEL_DRIVE_HEADER = 'R.1.'

class InputManager:
    def __init__(self, sock):
        print 'joystick:',pygame.joystick.get_count()
        self.init_joystick(sock)
        self.isRunning = True

    def init_joystick(self, socket):
        # 1. Get Joystick and get number of inputs
        self.socket = socket
        joystick = pygame.joystick.Joystick(0)# num = ID
        joystick.init()
        self.joystick = joystick
        self.joystick_name = joystick.get_name()
        self.numAxis = self.joystick.get_numaxes()
        self.numBalls = self.joystick.get_numballs()
        self.numButtons = self.joystick.get_numbuttons()
        self.numHats = self.joystick.get_numhats()
        # 2. Generate lists to store previous input states
        self.prevAxis = list()
        for i in range(self.numAxis):
            self.prevAxis.append(0)
        self.prevBalls = list()
        for i in range(self.numBalls):
            self.prevBalls.append(0)
        self.prevButtonsUp = list()
        for i in range(self.numButtons):
            self.prevButtonsUp.append(0)
        self.prevButtonsDown = list()
        for i in range(self.numButtons):
            self.prevButtonsDown.append(0)
        self.prevHats = list()
        for i in range(self.numHats):
            self.prevHats.append(0)
        
    def doStuff(self):
        for event in pygame.event.get():
            eventType = event.type
            if eventType == JOYAXISMOTION:
                for i in range(self.numAxis):
                    axis = self.joystick.get_axis(i)
                    if self.prevAxis[i] != axis:
                        self.prevAxis[i] = axis
                        self.sendCommand(MODEL_DRIVE_HEADER+str(i)+'.'+str(axis*-100))
            elif eventType == JOYBALLMOTION:
                for i in range(self.numBalls):
                    ball = self.joystick.get_ball(i)
                    if self.prevBalls[i] != ball:
                        self.prevBalls[i] = ball
                        self.sendCommand('ball:'+str(i)+':'+str(ball)+'\n')
            elif eventType == JOYHATMOTION:
                for i in range(self.numHats):
                    hat = self.joystick.get_hat(i)
                    if self.prevHats[i] != hat:
                        self.prevHats[i] = hat
                        self.sendCommand('hat:'+str(i)+':'+str(hat)+'\n')
            elif eventType == JOYBUTTONUP:
                for i in range(self.numButtons):
                    button = self.joystick.get_button(i)
                    if self.prevButtonsUp[i] != button:
                        self.prevButtonsUp[i] = button
                        self.sendCommand('button_up:'+str(i)+':'+str(button)+'\n')
            elif eventType == JOYBUTTONDOWN:
                for i in range(self.numButtons):
                    button = self.joystick.get_button(i)
                    if self.prevButtonsUp[i] != button:
                        self.prevButtonsUp[i] = button
                        self.sendCommand('button_down:'+str(i)+':'+str(button)+'\n')

    def sendCommand(self, sendCmd):
        self.socket.sendto(sendCmd, (UDP_IP, UDP_PORT))

def main():
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    delay = 0.001
    pygame.init()
    input_manager = InputManager(sock)
    while input_manager.isRunning:
        input_manager.doStuff()
        time.sleep(delay)


if __name__ == '__main__':
    main()
    input("block...")