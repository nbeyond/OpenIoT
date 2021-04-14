#!/usr/bin/env python

# TempCC_Closed.py: A program that reads temperatures from DS18B20 thermometers and 
#		save the results in a file.
#
#		author: Chan-Hee Park at KIGAM
#		date: 2017. 04. 10. 

import subprocess
import threading
import time
import serial
import datetime
import os
import glob
import MySQLdb
import sys

# Write file
temp_out = "/home/pi/closed_temp.dat"

# Connect mysql
db = MySQLdb.connect(host= "192.168.0.8",
                 user="pi",
                 passwd="YourPassword",
                 db="YourIoTDB")
curs = db.cursor()

while True:
	# Get the time for now
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	second = now.second

	# Make a system command
	arg = 'multitemp.sh'

	# Write off every one minute
	geo_id = "cc_closed"
	if (second%60 == 0):
	# Write off every 5 minutes	
#	if(minute%5 == 0) and (second%60 == 0):
		results = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
		data = results.communicate()
		split_data = data[0].split()
		with open(temp_out, "a") as text_file:
			text_file.write('{0} {1} {2} {3}\n'.format(now, split_data[0], split_data[1], split_data[2]))
			text_file.flush()

		# Insert energy data into db
		temperature = split_data[0].split('=')
		temp1 = float(temperature[1])
		temperature = split_data[1].split('=')
		temp2 = float(temperature[1])
		temperature = split_data[2].split('=')
		temp3 = float(temperature[1])
		try:
			curs.execute('''INSERT INTO cc_closed (geo_id, time, temp1, temp2, temp3) 
				VALUES (%s, %s, %s, %s, %s)''', (geo_id, now, temp1, temp2, temp3))
			db.commit()
		except:
			print ('Error: the database is being rolled back.')

	time.sleep(1)

#print now, split_data[0], split_data[1], split_data[2]

#for i in xrange(len(split_data)):
#	print split_data[i]

