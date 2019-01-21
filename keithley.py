import socket   #for sockets
import sys
import time
import numpy as np
 
class Keithley2002:
    """" Connect and control Keithley2002 over GPIB-Ethernet converter """

    def __init__(self, tcp_addr='192.168.90.47', tcp_port=1234):
        self.tcp_addr, self.tcp_port = tcp_addr, tcp_port
        self.welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2002,4108585,B02  /A02  \n'
        # Test connection and all of the settings
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((tcp_addr, tcp_port))
            self.s.settimeout(5)

            
        except socket.error as err_msg:
            print ('Unable to instantiate socket. Error code: ' + str(err_msg[0]) + ' , Error message : ' + err_msg[1])
            sys.exit();
         
        print ('\nSocket Initialized.\n')   
        self.initKeithley2002()

    def initKeithley2002(self):
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
        if self.s.recv(100) == self.welcome:
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
        print("Deviation: +%.3f, %.3f mV" % ((voltage.max()-voltage.mean())*1e3, (voltage.min()-voltage.mean())*1e3))

