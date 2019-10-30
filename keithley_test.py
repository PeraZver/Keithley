from keithley import Keithley2002
import socket

k = Keithley2002("192.168.90.251", 1234)

#k.initKeithley2002()
  
message = '0'

while(True):
    try:
        message = raw_input(" > ")     
        #print(repr(message))  
        
        if message[0:2] == 'ch':
            k.channel_select(message[2:])
        
        elif message == 'read?':       
            k.readout()

        elif message == 'err':
            k.errorCheck()

        elif message =='loop':
        	k.loopRead()

        else:
            k.normalTxRx(message)
        
    except socket.timeout:
        print ("socket timeout. New command. \n")
    
    except KeyboardInterrupt:
        print("User interruption!!")
        k.close()
        quit()