from subprocess import Popen, PIPE

p1 = Popen(["nc", "192.168.90.47", "1234"], stdin=PIPE, stdout=PIPE, 
bufsize=1024)

welcome = 'KEITHLEY INSTRUMENTS INC.,MODEL 2002,4108585,B02  /A02  \n'
p1.stdin.write('*idn?\r')
p1.stdin.flush()
if p1.stdout.readline() == welcome:
    print ("Connection with Keithley 2002 successful! :D\nGo on with your commands ... \n")
else:
    print ("Cannot see Keithley :(")
    
p1.stdin.write(':syst:frsw?\r')
p1.stdin.flush()
sw = 'REAR' if  p1.stdout.readline() == '0\n' else 'FRONT'
print ("Switch set to %s" % sw)

p1.stdin.close()
print ("Closing down the process ...")
p1.wait()
print("Process closed with %d" %p1.returncode)
quit()

while(True):
    try:
        command = raw_input(' > ')
        
        p1.stdin.write(command + '\r')
        p1.stdin.flush()
        a = p1.stdout.readline()
        print(a)
        if command == 'read?':
            print ("Voltage: " + a[0:a.find('NVDC')])
        
    except KeyboardInterrupt:
        print("User interruption!!")
        p1.stdin.close()
        print ("Closing down the process ...")
        p1.wait()
        print("Process closed with %d" %p1.returncode)
        quit()

