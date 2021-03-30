# Keithley Multimeter Scripts

Pero's script for interfacing fabulous Keithley devices such as 2002 and 2007. 

Pero, 2018

## Usage

### GPIB-Ethernet Converter (Yellowbox)
Connect the Yellowbox to the GPIB Port of the instrument. Make sure that Yellowbox is connected to the ELAB network. If the IP address is unknown, you can use Netfinder program to find, or summon the IT spirits. Dont't forget to power it on. Try connecting to the Yellowbox via "raw" connection in terminal (telnet to IP, port 1234). First, make sure that auto response is turned on `++auto 1`. Set the GPIB address, for example `++addr 16`. If everything's OK, you should get the response from Keithley after typing `*idn?`. If not, you chose your career poorly. 

### Library
In your Python script simply include `k = Keithley2002("192.168.90.61", 1234)` with the proper Yellowbox IP address, of course. 
All the instument control functions from the Keithley class are available from then on. The one you care the most about is the `k.readout()`.

### Documentation
Not coming soon.

Pero, 3/2021
