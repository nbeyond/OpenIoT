#!/usr/bin/python

"""
Listen to serial, return most recent numeric values
Lots of help from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device

revised by Chan-Hee Park for flow meter
"""
#from threading import Thread
import threading
import time
import serial
import datetime
import os
import glob
import MySQLdb
import sys

# Get the total number of args passed 
#total = len(sys.argv)

#if total < 2:
#	print "Usage: pi-serial.py <currentLiters>"
# Get the currentLiters
#currentLiters = sys.argv[1]

# File write
def writeFile(line):
	f = open("/home/pi/closed_flow.dat", 'a')
	f.write(line)
	f.close()
	
last_received = ''
def receiving(ser):
    global last_received
    buffer = ''

    while True:
#        buffer += ser.read(ser.inWaiting())
        buffer += ser.read(1024)
        if '\n' in buffer:
		last_received, buffer = buffer.split('\n')[-2:]

def isfloat(value):
	try:
		float(value)
		return True
	except:
		return False

if __name__=='__main__':
	ser = serial.Serial(
		port='/dev/ttyACM0',
		baudrate=115200,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		timeout=0.1,
		xonxoff=0,
		rtscts=0,
		interCharTimeout=None
	)

	threading.Thread(target=receiving, args=(ser,)).start()

	db = MySQLdb.connect(host= "192.168.0.8",
                 user="pi",
                 passwd="YourPassword",
                 db="YourIoTDB")
	curs = db.cursor()
	while True:
		dataArray = last_received.split(',')
		if isfloat(dataArray[0]): 
			flow1 = float(dataArray[0])
			volume1 = float(dataArray[1])
			flow2 = float(dataArray[2])
			volume2 = float(dataArray[3])
			now = datetime.datetime.now()
			hour = now.hour
			minute = now.minute
			second = now.second

			# Write off
#			print now, flow1, volume1, flow2, volume2

			# Write off 
			geo_id = "cc_closed"
			if (second%60 == 0):
				line = str(now)+" "+str(flow1)+" "+str(volume1)+" "+str(flow2)+" "+str(volume2)+"\n"
				writeFile(line)

				print ('Writing to nbeyond cc_closed_flow in nbeyond!')
				# Insert into flow data into cc_closed 
				try:
					curs.execute('''INSERT INTO cc_closed_flow 
						VALUES (%s, %s, %s, %s, %s, %s)''', (geo_id, now, flow1, volume1, flow2, volume2))
					db.commit()
#					print ('mysql updated!')
				except:
					print ('Error: the database is being rolled back.')

		time.sleep(1)

