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
		self.init_joystick(sock)
		self.isRunning = True

	def init_joystick(self, socket):
		# 1. Get Joystick and get number of inputs
		self.socket = socket
		# joystick = pygame.joystick.Joystick(0)# num = ID
		# joystick.init()
		
	def doStuff(self):
		keys = pygame.key.get_pressed()
		print 'const:',keys[K_w],keys[K_s],keys[K_a],keys[K_d]
		if keys[K_w]:
			print 'up:'
			self.sendCommand(MODEL_DRIVE_HEADER+'L'+'.'+str(-100))
			self.sendCommand(MODEL_DRIVE_HEADER+'R'+'.'+str(100))
		if keys[K_s]:
			print 'down'
			self.sendCommand(MODEL_DRIVE_HEADER+'L'+'.'+str(100))
			self.sendCommand(MODEL_DRIVE_HEADER+'R'+'.'+str(-100))
		if keys[K_a]:
			print 'left'
			self.sendCommand(MODEL_DRIVE_HEADER+'L'+'.'+str(50))
			self.sendCommand(MODEL_DRIVE_HEADER+'R'+'.'+str(100))
		if keys[K_d]:
			print 'right'
			self.sendCommand(MODEL_DRIVE_HEADER+'L'+'.'+str(100))
			self.sendCommand(MODEL_DRIVE_HEADER+'R'+'.'+str(50))
		# for event in pygame.event.get():
		# 	eventType = event.type
		# 	# if eventType == JOYAXISMOTION:
		# 	# 	for i in range(self.numAxis):
		# 	# 		axis = self.joystick.get_axis(i)
		# 	# 		if self.prevAxis[i] != axis:
		# 	# 			self.prevAxis[i] = axis
		# 	# 			self.sendCommand(MODEL_DRIVE_HEADER+str(i)+'.'+str(axis*-100))
		# 	if eventType == KEYDOWN:
				

	def sendCommand(self, sendCmd):
		self.socket.sendto(sendCmd, (UDP_IP, UDP_PORT))

def main():
	sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
	delay = 0.001
	pygame.init()
	input_manager = InputManager(sock)

	while input_manager.isRunning:
		# print 'dostuff'
		input_manager.doStuff()
		time.sleep(delay)


if __name__ == '__main__':
	main()
	input("block...")