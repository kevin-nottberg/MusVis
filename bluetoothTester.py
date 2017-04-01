import os
import glob
import time
from threading import Thread
from bluetooth import *

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

STATUS = "off"

lightBuffer = 00
diffRed = 10
diffBlue = 10
diffGreen = 10

getStatus():
	
    #if thread.isAlive() == TRUE:
        #STATUS = "on"
        #break
    #elif thread.isAlive() == FALSE:
        #STATUS = "off"
        #break

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "LightControlServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                 )

while True:          
	print "Waiting for connection on RFCOMM channel %d" % port
        client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info
	
	try:
		data = client_sock.recv(1024)
		if len(data) == 0: break
		print "received [%s]" % data
		
		if data == 'temp':
			#Something
		elif data == 'lightOn':
			data = 'light on!'
                    	if STATUS = "on":
				#break and do nothing
		elif data == 'lightOff':
			#Stop the ledaudio light thread
		        data = 'light off!'
                    	STATUS = "off"
		else:
			data = 'WTF!' 
	            	client_sock.send(data)
		        print "sending [%s]" % data

	except IOError:
		pass
        
	except KeyboardInterrupt:

		print "disconnected"

		client_sock.close()
		server_sock.close()
		print "all done"

		break
    
