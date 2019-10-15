import socket   #for sockets
import sys
import time
import numpy as np
 
class Keithley2002:
	""" Connect and control Keithley2002 over GPIB-Ethernet converter """

	def __init__(self, tcp_addr='192.168.90.47', tcp_port=1234):
		self.tcp_addr, self.tcp_port = tcp_addr, tcp_port
		#self.welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2002,4108585,B02  /A02  \n'
		self.welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2002'
		# Test connection and all of the settings
		try:
			#create an AF_INET, STREAM socket (TCP)
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((tcp_addr, tcp_port))
			self.s.settimeout(5)
			self.s.send("++addr 16\r")
			
		except socket.error as err_msg:
			print ('Unable to instantiate socket. Error code: ' + str(err_msg[0]) + ' , Error message : ' + err_msg[1])
			sys.exit();
		 
		print ('\nSocket Initialized.\n')   
		self.initKeithley2002()

	def initKeithley2002(self):

		self.s.send("++addr\r")
		print("GPIB Address %s" % self.s.recv(10).decode())
		self.checkID()
		self.checkPanel()
		self.formatSelect()
		self.s.send(":init:cont off; cont?\r")
		if self.s.recv(5) == '0\n':
			print("Keithley Initialized.")
		else:
			print("Initialization funny, but you can continue.")

	def checkID(self):
		#Test connection
		self.s.send("*idn?\r")
		if self.s.recv(100)[0:36] == self.welcome:
			print ("Connection with Keithley 2002 estabilished! :D\n")
		else:
			print ("Cannot see Keithley :(")

	def checkPanel(self):
		# Switch to back panel
		self.s.send(':syst:frsw?\r')
		x = 'REAR' if  self.s.recv(50).decode() == '0\n' else 'FRONT'
		print ("Switch set to %s" % x)

	def formatSelect(self):
		# Format high precision
		self.s.send(':form:exp hpr; exp?\r')
		x = 'High Precision' if  self.s.recv(100).decode() == 'HPR\n' else 'Normal'
		print ('Data format set to: %s' % x)

		# Readout format
		self.s.send(':form:elem read, stat, unit, chan; elem?\r')
		print("Data format: %s" % self.s.recv(50))

	def errorCheck(self):
		print("Error inquery")
		self.s.send(':syst:err?\r')
		print("Error message: %s" % self.s.recv(50))

	def channel_select(self, chNumber ):
		self.chNumber = chNumber
		#print("Setting Up Channel " + self.chNumber)
		self.s.send(':route:close (@' + self.chNumber + '); close? (@' + self.chNumber + ')\r')
		if self.s.recv(5) == '1\n':
			print("Channel " + self.chNumber + " set.")
		else:
			print("Channel not set :(")

	def readout(self):
		""" Read voltage """
		self.s.send('read?\r')
		data = self.s.recv(50)
		print ("CH " + data[-10:-8] + " Voltage: " + data[0:data.find('NVDC')])    
		return data[0:data.find('NVDC')]

	def setOhm(self):
		self.s.send(":func 'res'; func?\r")
		if (self.s.recv(10).decode() == '"RES"\n'):
			print ("2-Wire Ohmmeter selected!")

	def setOhm4W(self):
		self.s.send(":func 'fres'; func?\r")
		if (self.s.recv(10).decode() == '"FRES"\n'):
			print ("4-Wire Ohmmeter selected!")

	def readOhm(self):
		self.s.send(":func?\r")
		if (self.s.recv(10).decode() == '"RES"\n'):
			self.s.send(":read?\r")
			data = self.s.recv(50)
			#print ("Resistance:\t %s" %(data[0:data.find('NOHM')]) )
			return data[0:data.find('NOHM')]
		else:
			print ("2W-Ohmmeter not selected")


	def readOhm4W(self):
		self.s.send(":func?\r")
		if (self.s.recv(10).decode() == '"FRES"\n'):
			self.s.send(":read?\r")
			data = self.s.recv(50)
			#print ("Resistance:\t %s" %(data[0:data.find('NOHM')]) )
			return data[0:data.find('NOHM4W')]
		else:
			print ("4W-Ohmmeter not selected")

	def close(self):
		self.s.close()
		print ("Closing down the socket ...")

	def normalTxRx(self, message):
		self.s.send(message + '\r')
		data = self.s.recv(100)
		print (data)

	def loopRead(self, channel='09'):
		#self.channel_select(channel)
		voltage = np.array([])
		print("Loop measurement started.")
		while True:
			try:
				self.s.send('read?\r')
				data = self.s.recv(50)
				voltage = np.append(voltage, float(data[0:data.find('NVDC')]))
				print ("CH %s Voltage: %.9f V.\r" % (data[-10:-8], float(data[0:data.find('NVDC')])) )  
				time.sleep(1)
				#print('\r')
			except KeyboardInterrupt:
				print("User interrupted loop measurement")
				break
		print("\nStatistics Time !!!!") 
		print("No. of samples: %d" % np.shape(voltage)[0])       
		print("Average value: %.2f V, StDev: %.3f mV." % (voltage.mean(), voltage.std()*1e3))
		print("Deviation: +%.3f, -%.3f mV" % ((voltage.max()-voltage.mean())*1e3, (voltage.min()-voltage.mean())*1e3))


class Keithley2410:
	""" Connect and control Keithley2410 over GPIB-Ethernet converter """

	def __init__(self, tcp_addr='192.168.90.47', tcp_port=1234):
		self.tcp_addr, self.tcp_port = tcp_addr, tcp_port
		#self.welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2410,4412021,C34 Sep 21 2016 15:30:00/A02  /K/M\n'
		self.welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2410'
		# Test connection and all of the settings
		try:
			#create an AF_INET, STREAM socket (TCP)
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((tcp_addr, tcp_port))
			self.s.settimeout(5)
			self.s.send("++addr 24\r")

			
		except socket.error as err_msg:
			print ('Unable to instantiate socket. Error code: ' + str(err_msg[0]) + ' , Error message : ' + err_msg[1])
			sys.exit();
		 
		print ('\nSocket Initialized.\n')   
		self.initKeithley2410()

	def initKeithley2410(self):
		self.s.send("++addr\r")
		print("GPIB Address %s" % self.s.recv(10).decode())
		self.s.send(":syst:pres; pos?\r")		
		if self.s.recv(10).decode() == 'PRES\n':
		    print("Keithley 2410 Preset.")
		else:
		    print("Initialization funny, but you can continue.")
		
		self.checkID()
		self.checkPanel()
		self.formatSelect()
		print("Keithley Initialized.")

	def close(self):
		self.s.close()
		print ("Closing down the socket ...")

	def checkID(self):
		#Test connection
		self.s.send("*idn?\r")
		if self.s.recv(100)[0:36] == self.welcome:
			print ("Connection with Keithley 2410 estabilished! :D\n")
		else:
			print ("Cannot see Keithley :(")

	def checkPanel(self, panel='fron'):
		""" Switch to front/back panel """
		self.s.send(':syst:frsw %s; frsw?\r' % panel) # This can also be achieved with :rout:term function
		time.sleep(0.1)
		x = 'REAR' if  self.s.recv(10).decode() == 'REAR\n' else 'FRONT'
		print ("Switch set to %s" % x)

	def formatSelect(self, form='asc'):
		""" Select output format """
		self.s.send(':form:data %s; data?\r' % form)
		time.sleep(0.1)
		x = 'ASCII' if  self.s.recv(20).decode() == 'ASC\n' else 'IEEE754 S.P.'
		print ('Data format set to: %s' % x)

		# Readout format
		self.s.send(':form:elem volt,curr,res; elem?\r')
		time.sleep(0.1)
		print("Data format: %s" % self.s.recv(50))
 
	def normalTxRx(self, message):
		self.s.send(message + '\r')
		time.sleep(0.1)
		data = self.s.recv(100)
		print (data)

	def errorCheck(self):
		print("Error inquery")
		self.s.send(':syst:err?\r')
		time.sleep(0.1)
		print("Error message: %s" % self.s.recv(50))

	def setOutput(self, output_state): 
		""" Output state can be either 'ON' or 'OFF' """
		self.s.send(":outp %s; outp?\r" % output_state)
		time.sleep(0.1)
		x = 'ON' if self.s.recv(5) == '1\n' else 'OFF'
		print("Output %s" % x)

# These functions set basic source and sense

	def setSource(self, source):
		""" source can be 'volt' or 'curr'. """
		self.s.send(":sour:func %s; func?\r" % source) # <--- No quotations here
		time.sleep(0.1)
		x = 'Voltage' if self.s.recv(10) == "VOLT\n" else 'Current'
		print("Source set to: %s" % x)

	def setSourceMode(self, source='volt', mode='fix'):
		""" Source mode can be FIXed, LIST or SWEep. Source either VOLT or CURR """
		self.s.send(':sour:%s:mode %s; mode?\r' % (source, mode) )
		time.sleep(0.1)
		print("Source mode: %s" % self.s.recv(5))	

	def setSourceRange(self, source='volt', rang='AUTO'):
		""" Source range can be <n> =   -1.05 to 1.05 Specify I-Source level (amps)
										-1100 to 1100 Specify V-Source level (volts)
										DEFault 100uA range (I-Source)
												20V range (V-Source)
										MINimum 1uA range (I-Source)
												200mV range (V-Source)
										MAXimum 1A range (I-Source)
												1100V range (V-Source)
										UP Select next higher range
										DOWN Select next lower range 
										AUTO AUtomatically assigned."""    

		if rang == 'AUTO': 
			self.s.send(':sour:%s:rang:auto 1; auto?\r' % source )
			time.sleep(0.1)
			print("Source Auto %s" % ('enabled.' if self.s.recv(10).decode()=='1\n' else 'disabled.' ) )	
		else:								
			self.s.send(':sour:%s:rang %s; rang?\r' % (source, rang) )
			time.sleep(0.1)
			print("Source range: %s" % self.s.recv(20))	

	def setSourceLevel(self, source='volt', lev='DEF'):
		""" Set source level at <n> = -1.05 to 1.05 Set I-Source amplitude (amps)
									-1100 to 1100 Set V-Source amplitude (volts)
									DEFault 0A or 0V
									MINimum -1.05A or -1100V
									MAXimum +1.05A or +1100V """	
		self.s.send(':sour:%s:lev %s; lev?\r' % (source, lev))	
		time.sleep(0.1)
		print("Source level: %s" % self.s.recv(20))							

	def setSense(self, sense='curr'):
		""" measure either VOLTage, CURRent or RESistance. """
		self.s.send(':sense:func "%s"; func?\r' % sense) # <--- Use quotations here
		time.sleep(0.1)
		print("Sense set to: %s" % self.s.recv(20))

	def setSenseProtection(self, sense='curr', compliance='DEF'):
		""" Set compliance value <n> = -1.05 to 1.05 Current compliance limit
										-1100 to 1100 Voltage compliance limit
										DEFault 105uA, 21V
										MINimum -1.05A, -1100V
										MAXimum 1.05A, 1100V """
		self.s.send(':sens:%s:prot %s; prot?\r' % (sense, compliance) )
		time.sleep(0.1)
		print("Sense compliance: %s" % self.s.recv(20))

	def setSenseRange(self, sense='curr', rang='DEF'):
		""" Setting measuremetn range <n> = -1.05 to 1.05 Expected reading in amps
											-1100 to 1100 Expected reading in volts
											0 to 2.1e8 Expected reading in ohms
											DEFault 1.05e-4 (amps), 21 (volts), 2.1e5 (ohms)
											MINimum -1.05 (amps), -1100 (volts), 0 (ohms)
											MAXimum 1.05 (amps), 1100 (volts), 2.1e8 (ohms)
											UP Select next higher measurement range
											DOWN Select next lower measurement range 
											AUTO Automatically assigned. """
		if rang == 'AUTO':
			self.s.send(':sens:%s:rang:auto 1; auto?\r' % sense)
			time.sleep(0.1)
			print("Sense Auto %s"  % ('enabled.' if self.s.recv(10).decode()=='1\n' else 'disabled.' )  )
		else:	
			self.s.send(':sens:%s:rang %s; rang?\r' % (sense, rang) )
			time.sleep(0.1)
			print("Sense range: %s" % self.s.recv(20))			

	def readOut(self):
		self.setOutput('ON')
		self.s.send(':read?\r')
		time.sleep(0.1)
		data = self.s.recv(50).split(',')
		print("Voltage:   %s \nCurrent:   %s \nResistance: %s" % (data[0], data[1], data[2]))
		self.setOutput('OFF')

# Some sweet sweep functions		

	def setSweepStart(self, source='curr', value=0):
		""" Define sweep start """
		self.s.send('sour:%s:start %s; start?\r' % (source, value) )
		print("Source sweep start: %s" % self.s.recv(20))

	def setSweepStop(self, source='curr', value=0):
		""" Define sweep stop """
		self.s.send('sour:%s:stop %s; stop?\r' % (source, value) )
		print("Source sweep stop: %s" % self.s.recv(20))

	def setSweepStep(self, source='curr', value=0):
		""" Define sweep step """
		self.s.send('sour:%s:step %s; step?\r' % (source, value) )
		print("Source sweep step: %s" % self.s.recv(20))

	def setSweepMode(self, mode='lin'):
		""" Set the sweep spacing to LINear or LOGarithmic """
		self.s.send(':sour:swe:spac %s; spac?\r' % mode)
		print("Source mode %s." % ('linear' if self.s.recv(20).decode()=='LIN\n' else 'logarithmic'))

	def setSweepRange(self, rang='AUTO'):
		""" Adjusts sweep range <name> = BEST Use the best fixed mode
										AUTO Use the most sensitive source
										range for each sweep level
										FIXed Use the present source range for
										the entire sweep """

		self.s.send(':sour:swe:rang %s; rang?\r' % rang)
		print("Sweep range set to %s" % self.s.recv(20))

	def setSweepNoPoints(self, NoPoints='10'):
		""" Sets sweep number of points """
		self.s.send(':trig:coun %s; coun?\r' % NoPoints)
		print("Number of sweep points: %s" % self.s.recv(20))

# These fucntion combine previous ones to get desired measurement

	def sourceVMeasureI(self, v, compliance='100e-3'):
		""" Take V-I measurement """
		self.setSource('volt')
		self.setSourceMode('volt', 'fix')
		self.setSourceRange('volt', 'AUTO')
		self.setSourceLevel('volt', v)

		self.setSense('curr')
		self.setSenseProtection('curr', compliance)
		self.setSenseRange('curr', 'AUTO')

		self.readOut()

	def sourceIMeasureV(self, i, compliance='100e-3'):
			""" Take V-I measurement """
			self.setSource('curr')
			self.setSourceMode('curr', 'fix')
			self.setSourceRange('curr', 'AUTO')
			self.setSourceLevel('curr', i)

			self.setSense('volt')
			self.setSenseProtection('volt', compliance)
			self.setSenseRange('volt', 'AUTO')

			self.readOut()

	def sourceVMeasureV(self, v, compliance='100e-3'):
			""" Take V-I measurement """
			self.setSource('volt')
			self.setSourceMode('volt', 'fix')
			self.setSourceRange('volt', 'AUTO')
			self.setSourceLevel('volt', v)

			self.setSense('volt')
			self.setSenseProtection('volt', compliance)
			self.setSenseRange('volt', 'AUTO')

			self.readOut()

	def sourceIMeasureI(self, i, compliance='100e-3'):
			""" Take V-I measurement """
			self.setSource('curr')
			self.setSourceMode('curr', 'fix')
			self.setSourceRange('curr', 'AUTO')
			self.setSourceLevel('curr', i)

			self.setSense('curr')
			self.setSenseProtection('curr', compliance)
			self.setSenseRange('curr', 'AUTO')

			self.readOut()

# These functions wrap previous ounes to get more meaningfull measurements

	def measureV(self):
		""" Only measure V """
		self.sourceIMeasureV('0', 'MAX')

	def measureI(self):
		""" Only measure I """
		self.sourceVMeasureI('0', 'MAX')

	def sinkI(self, i):
		""" sink current """
		self.sourceVMeasureI('0', i)

	def measureDiode(self):
		""" Measurement of Diode U-I characteristics using instrument's sweep function. """

		Imin = 0.0
		Imax = 50e-3
		Istep = 0.1e-3
		Npoints = int((Imax - Imin)/Istep)
		a = ''
		data = ''

		self.setSource('curr')
		self.setSense('volt')
		self.setSenseProtection('volt', '2')

		# Set up the sweep
		self.setSweepStart('curr', Imin)
		self.setSweepStop('curr', Imax)
		self.setSweepStep('curr', Istep)
		self.setSweepMode('lin')		
		self.setSweepRange('AUTO')  # adjust the source sweep range

		self.setSourceMode('curr', 'swe')   # set the source in the sweep mode
		self.setSweepNoPoints(Npoints)

		self.setOutput('ON')
		self.s.send(':read?\r')

		while a != '\n':
			a = self.s.recv(1)
			data += a
		data = data[:-1].split(',')
		# print(data[:-1].split(','))
		self.setOutput('OFF')
		return data[0::3], data[1::3] # return voltage and current

		