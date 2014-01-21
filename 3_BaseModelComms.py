import socket
import threading
import UDPNetworkConstants

MOTOR_FL = 0
MOTOR_FR = 1
MOTOR_RL = 2
MOTOR_RR = 3

class BaseModelComms(object):
	def __init__(self):
		self.isRunning = True
		self.roverModel = RoverModel()
		self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.telemetryRecvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.telemetryControlConnections = []
		self.commandEchoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.commandSendConnections = []
		self.gamepadSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.gamepadSendFeedbackConnections = []
		self.threads = []
		self.initSockets()

	def initSockets(self):
		self.createTelemetryRecvSocket(UDPNetworkConstants.BASE_TELEMETRY_RECV[0], UDPNetworkConstants.BASE_TELEMETRY_RECV[1])
		self.addTelemetryController(UDPNetworkConstants.BASE_TELEMETRY_CONTROL_SEND[0], UDPNetworkConstants.BASE_TELEMETRY_CONTROL_SEND[1])
		self.createCommandEchoSocket(UDPNetworkConstants.BASE_CMD_ECHO_RECV[0], UDPNetworkConstants.BASE_CMD_ECHO_RECV[1])
		self.addCommandSendConnections(UDPNetworkConstants.BASE_CMD_SEND[0], UDPNetworkConstants.BASE_CMD_SEND[1])
		self.createGamepadSocket(UDPNetworkConstants.BASE_GAMEPAD_RECV[0], UDPNetworkConstants.BASE_GAMEPAD_RECV[1])
		self.addGamepadFeedbackConnections(UDPNetworkConstants.BASE_GAMEPAD_FEEDBACK_SEND[0], UDPNetworkConstants.BASE_GAMEPAD_FEEDBACK_SEND[1])
		self.addThreads()

	def createTelemetryRecvSocket(self, ip, port):
		self.telemetryRecvSocket.bind((ip,port))

	def addTelemetryController(self, ip, port):
		self.telemetryControlConnections.append([ip, port])

	def createCommandEchoSocket(self, ip, port):
		self.commandEchoSocket.bind((ip,port))

	def addCommandSendConnections(self, ip, port):
		self.commandSendConnections.append([ip, port])

	def createGamepadSocket(self, ip, port):
		self.gamepadSocket.bind((ip,port))

	def addGamepadFeedbackConnections(self, ip, port):
		self.commandSendConnections.append([ip, port])

	def addThreads(self):
		self.threads.append(threading.Thread(target=self.telemetryRecvThread))
		self.threads.append(threading.Thread(target=self.commandEchoRecvThread))
		self.threads.append(threading.Thread(target=self.gamepadRecvThread))

	def startThreads(self):
		for i in range(len(self.threads)):
			self.threads[i].daemon = True
			self.threads[i].start()

	def telemetryRecvThread(self):
		print 'Telemetry Recv Thread:',str(self.telemetryRecvSocket)
		while self.isRunning:
			data, addr = self.telemetryRecvSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'Telemetry Recv:','X',data,'X'

	def commandEchoRecvThread(self):
		print 'Command Echo Recv Thread:',str(self.commandEchoSocket)
		while self.isRunning:
			data, addr = self.commandEchoSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'Command Echo Recv:','X',data,'X'

	def gamepadRecvThread(self):
		print 'gamepad Recv Thread:',str(self.gamepadSocket)
		while self.isRunning:
			data, addr = self.gamepadSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'gamepad Recv:','X',data,'X'
			for i in range(len(self.commandSendConnections)):
				self.sendSocket.sendto(data, (self.commandSendConnections[i][0],self.commandSendConnections[i][1]))

class RoverModel(object):
	def __init__(self):
		self.ROVER_DRIVE = [0,0,0,0]# FL,FR,RL,RR
		self.CONTROL_DRIVE  = [0,0,0,0]# FL,FR,RL,RR

	def getRoverDrive(self, num):
		return self.ROVER_DRIVE[num]

	def getControlDrive(self, num):
		return self.CONTROL_DRIVE[num]

	def setRoverDrive(self, num, speed):
		self.ROVER_DRIVE[num] = speed

	def setControlDrive(self, num, speed):
		self.CONTROL_DRIVE[num] = speed

if __name__ == '__main__':
	print 'Start BaseModelComms'
	BaseModelComms = BaseModelComms()
	BaseModelComms.startThreads()
	input("block...")