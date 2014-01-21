import socket
import threading
import UDPNetworkConstants

MOTOR_FL = 0
MOTOR_FR = 1
MOTOR_RL = 2
MOTOR_RR = 3

class RoverModelComms(object):
	def __init__(self):
		self.isRunning = True
		self.roverModel = RoverModel()
		self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.daemonRecvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.daemonConnections = []
		self.telemetryControlRecvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.telemetryTargetConnections = []
		self.commandRecvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.commandEchoConnections = []
		self.threads = []
		self.initSockets()

	def initSockets(self):
		self.createDaemonRecvSocket(UDPNetworkConstants.ROVER_DAEMON_RECV[0], UDPNetworkConstants.ROVER_DAEMON_RECV[1])
		self.addDaemon(UDPNetworkConstants.DAEMON_TESTDAEMON_RECV[0], UDPNetworkConstants.DAEMON_TESTDAEMON_RECV[1])
		self.createTelemetryControlRecvSocket(UDPNetworkConstants.ROVER_TELEMETRY_CTRL_RECV[0], UDPNetworkConstants.ROVER_TELEMETRY_CTRL_RECV[1])
		self.addTelemetryTarget(UDPNetworkConstants.ROVER_TELEMETRY_SEND[0], UDPNetworkConstants.ROVER_TELEMETRY_SEND[1])
		self.createCommandRecvSocket(UDPNetworkConstants.ROVER_CMD_RECV[0], UDPNetworkConstants.ROVER_CMD_RECV[1])
		self.addCommandEchoTarget(UDPNetworkConstants.ROVER_CMD_ECHO_SEND[0], UDPNetworkConstants.ROVER_CMD_ECHO_SEND[1])
		self.addThreads()

	def createDaemonRecvSocket(self, ip, port):
		self.daemonRecvSocket.bind((ip, port))

	def addDaemon(self, ip, port):
		self.daemonConnections.append([ip, port])

	def createTelemetryControlRecvSocket(self, ip, port):
		self.telemetryControlRecvSocket.bind((ip, port))

	def addTelemetryTarget(self, ip, port):
		self.telemetryTargetConnections.append([ip, port])

	def createCommandRecvSocket(self, ip, port):
		self.commandRecvSocket.bind((ip, port))

	def addCommandEchoTarget(self, ip, port):
		self.commandEchoConnections.append([ip, port])

	def addThreads(self):
		self.threads.append(threading.Thread(target=self.daemonRecvThread))
		self.threads.append(threading.Thread(target=self.telemetryRecvThread))
		self.threads.append(threading.Thread(target=self.commandRecvThread))

	def startThreads(self):
		for i in range(len(self.threads)):
			self.threads[i].daemon = True
			self.threads[i].start()

	def daemonRecvThread(self):
		print 'Daemon Thread:',str(self.daemonRecvSocket)
		while self.isRunning:
			data, addr = self.daemonRecvSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'Daemon:','X',data,'X'
			for i in range(len(self.telemetryTargetConnections)):
				self.sendSocket.sendto(data, (self.telemetryTargetConnections[i][0],self.telemetryTargetConnections[i][1]))

	def telemetryRecvThread(self):
		print 'Telemetry Receive Thread:',str(self.telemetryControlRecvSocket)
		while self.isRunning:
			data, addr = self.telemetryControlRecvSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'Telemetry:','X',data,'X'

	def commandRecvThread(self):
		print 'Command Receive Thread:',str(self.commandRecvSocket)
		while self.isRunning:
			data, addr = self.commandRecvSocket.recvfrom(1024) # buffer size is 1024 bytes
			msg = data.split('.')
			print 'Command:','X',data,'X'
			for i in range(len(self.daemonConnections)):
				self.sendSocket.sendto(data, (self.daemonConnections[i][0],self.daemonConnections[i][1]))

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
	print 'Start RoverModelComms'
	RoverModelComms = RoverModelComms()
	RoverModelComms.startThreads()
	input("block...")














	# def _addConnectionSet(ip, port):
	# 	socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 	socket.bind(ip,port)
	# 	sendPort = port + 1
	# 	return [socket, ip, sendPort]

	# def addDaemonConnection(ip, port):
	# 	self.daemonConnections.append(self._addConnectionSet(ip, port))

	# def addTelemetryConnection(ip, port):
	# 	self.telemetryConnections.append(self._addConnectionSet(ip, port))

	# def addCommandConnections(ip, port):
	# 	self.commandConnections.append(self._addConnectionSet(ip, port))

	# def addThreads(self):
	# 	self.threads.append(threading.Thread(target=self.daemonRecvThread, args = (self.daemonConnections,)))
	# 	# self.threads.append(threading.Thread(target=self.telemetryRecvThread, args = (self.telemetryConnections,)))

	# def daemonRecvThread(self, daemonConnectionInfo):
	# 	print 'Daemon Thread'
	# 	while self.isRunning:
	# 		data, addr = daemonConnectionInfo[0].recvfrom(1024) # buffer size is 1024 bytes
	# 		msg = data.split('.')
	# 		print 'msg:',msg
	# 		try:
	# 			if len(msg) == 4:
	# 				if msg[0] == 'R':# CONTROL(SET) COMMANDS
	# 					if msg[1] == '1':# ROVER DRIVE SYSTEMS
	# 						if msg[2] == 'L':
	# 							self.roverModel.setRoverDrive(MOTOR_FL, int(msg[3]))
	# 							self.roverModel.setRoverDrive(MOTOR_RL, int(int(msg[3]) * -1))
	# 						elif msg[2] == 'R':
	# 							self.roverModel.setRoverDrive(MOTOR_FR, int(msg[3]))
	# 							self.roverModel.setRoverDrive(MOTOR_RR, int(int(msg[3]) * -1))
	# 						else:
	# 							self.roverModel.setRoverDrive(int(msg[2])-1, int(msg[3]))
	# 							# daemonConnectionInfo[0].sendto(data, (daemonConnectionInfo[1], daemonConnectionInfo[2]))
	# 		except ValueError:
	# 			# this is a casting error, generally when casting
	# 			# int(msg[]). Just throw away msg.
	# 			pass

	# def telemetryRecvThread(self, telemetryConnectionInfo):
	# 	print 'Telemetry Thread'
	# 	while self.isRunning:
	# 		data, addr = daemonConnection.recvfrom(1024) # buffer size is 1024 bytes
	# 		msg = data.split('.')
	# 		try:
	# 			if len(msg) == 4:
	# 				if msg[0] == 'R':# CONTROL(SET) COMMANDS
	# 					if msg[1] == '1':# ROVER DRIVE SYSTEMS
	# 						if msg[2] == 'L':
	# 							self.roverModel.setRoverDrive(MOTOR_FL, int(msg[3]))
	# 							self.roverModel.setRoverDrive(MOTOR_RL, int(int(msg[3]) * -1))
	# 							telemetryConnectionInfo[0].sendto(data, (telemetryConnectionInfo[1], telemetryConnectionInfo[2]))
	# 						elif msg[2] == 'R':
	# 							self.roverModel.setRoverDrive(MOTOR_FR, int(msg[3]))
	# 							self.roverModel.setRoverDrive(MOTOR_RR, int(int(msg[3]) * -1))
	# 							telemetryConnectionInfo[0].sendto(data, (telemetryConnectionInfo[1], telemetryConnectionInfo[2]))
	# 						else:
	# 							self.roverModel.setRoverDrive(int(msg[2])-1, int(msg[3]))
	# 							telemetryConnectionInfo[0].sendto(data, (telemetryConnectionInfo[1], telemetryConnectionInfo[2]))
	# 		except ValueError:
	# 			# this is a casting error, generally when casting
	# 			# int(msg[]). Just throw away msg.
	# 			pass








# class RoverModelComms2(object):
# 	def __init__(self, ip, roverRecvPort, baseRecvPort,roverSendPort,baseSendPort):
# 		super(RoverModelComms, self).__init__()
# 		self.UDP_IP = ip
# 		self.roverRecvPort = roverRecvPort
# 		self.baseRecvPort = baseRecvPort
# 		self.roverSendPort = roverSendPort
# 		self.baseSendPort = baseSendPort
# 		self.roverSocket = socket.socket(socket.AF_INET, # Internet
# 					 socket.SOCK_DGRAM) # UDP
# 		self.roverSocket.bind((self.UDP_IP, self.roverRecvPort))
# 		self.controlSocket = socket.socket(socket.AF_INET, # Internet
# 					 socket.SOCK_DGRAM) # UDP
# 		self.controlSocket.bind((self.UDP_IP, self.baseRecvPort))
# 		self.sockSend = socket.socket(socket.AF_INET, # Internet
# 					 socket.SOCK_DGRAM) # UDP
# 		self.isRunning = True
# 		self.roverModel = RoverModel()
# 		self.threads = []

# 	def addThreads(self):
# 		self.threads.append(threading.Thread(target=self.openRoverConnection, args = (self.roverSocket,)))
# 		self.threads.append(threading.Thread(target=self.openBaseConnection, args = (self.controlSocket,)))

# 	def startThreads(self):
# 		for i in range(len(self.threads)):
# 			self.threads[i].daemon = True
# 			self.threads[i].start()

# 	# Receive Packets from Rover Driver Program
# 	def openRoverConnection(self, roverSocket):
# 		print "start roverConnection:"
# 		while self.isRunning:
# 			data, addr = roverSocket.recvfrom(1024) # buffer size is 1024 bytes
# 			print 'rover:'+data
# 			msg = data.split('.')
# 			try:
# 				if len(msg) == 4:
# 					if msg[0] == 'R':# CONTROL(SET) COMMANDS
# 						if msg[1] == '1':# ROVER DRIVE SYSTEMS
# 							if msg[2] == 'L':
# 								self.roverModel.ROVER_DRIVE[0] = int(msg[3])
# 								self.roverModel.ROVER_DRIVE[2] = int(int(msg[3]) * -1)
# 								self.sockSend.sendto(data, (self.UDP_IP, self.baseSendPort))
# 							elif msg[2] == 'R':
# 								self.roverModel.ROVER_DRIVE[1] = int(msg[3])
# 								self.roverModel.ROVER_DRIVE[3] = int(int(msg[3]) * -1)
# 								self.sockSend.sendto(data, (self.UDP_IP, self.baseSendPort))
# 							else:
# 								self.roverModel.ROVER_DRIVE[int(msg[2])-1] = int(msg[3])
# 								self.sockSend.sendto(data, (self.UDP_IP, self.baseSendPort))
# 			except ValueError:
# 				# this is a casting error, generally when casting
# 				# int(msg[]). Just throw away msg.
# 				pass

# 	# Receive Packets from Base Station
# 	def openBaseConnection(self, baseSocket):
# 		print "start baseConnection:"
# 		while self.isRunning:
# 			data, addr = baseSocket.recvfrom(1024) # buffer size is 1024 bytes
# 			print 'base:'+data
# 			msg = data.split('.')
# 			try:
# 				if len(msg) == 4:
# 					if msg[0] == 'C':# CONTROL(SET) COMMANDS
# 						if msg[1] == '1':# ROVER DRIVE SYSTEMS
# 							if msg[2] == 'L':
# 								self.roverModel.CONTROL_DRIVE[0] = int(msg[3])
# 								self.roverModel.CONTROL_DRIVE[2] = int(int(msg[3]) * -1)
# 								self.sockSend.sendto(data, (self.UDP_IP, self.roverSendPort))
# 							elif msg[2] == 'R':
# 								self.roverModel.CONTROL_DRIVE[1] = int(msg[3])
# 								self.roverModel.CONTROL_DRIVE[3] = int(int(msg[3]) * -1)
# 								self.sockSend.sendto(data, (self.UDP_IP, self.roverSendPort))
# 							else:
# 								self.roverModel.CONTROL_DRIVE[int(msg[2])-1] = int(msg[3])
# 								self.sockSend.sendto(data, (self.UDP_IP, self.roverSendPort))
# 			except ValueError:
# 				# this is a casting error, generally when casting
# 				# int(msg[]). Just throw away msg.
# 				pass

# if __name__ == '__main__':
# 	roverModel = RoverModelComms("127.0.0.1", 40000, 45000, 40001,45001)
# 	roverModel.addThreads()
# 	roverModel.startThreads()