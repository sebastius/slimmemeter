#!/usr/bin/env python3

import sys
import serial
import subprocess

################
#Error display #
################
def show_error():
	ft = sys.exc_info()[0]
	fv = sys.exc_info()[1]
	print("Fout type: %s" % ft )
	print("Fout waarde: %s" % fv )
	return

################################################################################################################################################
#Main program
################################################################################################################################################
print ("DSMR P1 uitlezer")
print ("Control-C om te stoppen")

#Set COM port config
ser = serial.Serial()
ser.baudrate = 9600
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_EVEN
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyMetertrekker"

#Open COM port
try:
	ser.open()
except:
	sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)      

while 1:
	p1_line=''

	try:
		p1_raw = ser.readline()
	except:
		sys.exit ("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name )      

	p1_str=str(p1_raw, "utf-8")
	p1_line=p1_str.strip()

	print (p1_line)

	if p1_line[0:9] == "1-0:1.8.1":
		print("daldag      ", p1_line[10:15])
		meter = int(float(p1_line[10:15]))
		subprocess.run(
			[
				"mqtt-simple",
				"-h",
				"houseparty.local",
				"-p",
				"p1meter/dal",
				"-m",
				str(meter)+" KWh",
			]
		)
	elif p1_line[0:9] == "1-0:1.8.2":
		print("piekdag     ", p1_line[10:15])
		meter = int(float(p1_line[10:15]))
		subprocess.run(
			[
				"mqtt-simple",
				"-h",
				"houseparty.local",
				"-p",
				"p1meter/piek",
				"-m",
				str(meter)+" KWh",
			]
		)
#	print "meter totaal  ", meter

# Huidige stroomafname: 1-0:1.7.0
	elif p1_line[0:9] == "1-0:1.7.0":
		print("Afgenomen vermogen      ", int(float(p1_line[10:17])*1000), " W")
		meter = int(float(p1_line[10:17])*1000)
		subprocess.run(
			[
				"mqtt-simple",
				"-h",
				"localhost",
				"-p",
				"p1meter/vermogen",
				"-m",
				str(meter)+" W",
			]
		)
	else:
		pass

#Close port and show status
try:
	ser.close()
except:
	sys.exit ("Oops %s. Programma afgebroken." % ser.name )  
