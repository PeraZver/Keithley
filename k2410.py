import os
import csv
import time, datetime
from keithley import Keithley2410

k = Keithley2410()

####### Starting measurement #######################
print("\nMeasurement started on " + time.ctime() + ".\n") 
start_time = datetime.datetime.now()

# Filename
filename = 'Diode_' + str(start_time.date()) + '_' + str(start_time.hour) + '-' + str(start_time.minute) + ".csv"
csv_file = open(filename, "wb")
writer = csv.writer(csv_file)
writer.writerow(["Voltage", "Current"])



volt, curr = k.measureDiode()
rows = zip(volt, curr)
for row in rows:
	writer.writerow(row)

print("Measurement done!")
print("Measurement time: " + str(datetime.datetime.now() - start_time))
print("Measurement data stored in " + filename)

csv_file.close()
k.close()