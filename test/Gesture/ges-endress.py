# coding: UTF-8
#!/usr/bin/env python
#
# GrovePi Example for using the Grove - Gesture Sensor v1.0(http://www.seeedstudio.com/depot/Grove-Gesture-p-2463.html)
#       
# This example returns a value when a user does an action over the sensor
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import grove_gesture_sensor

import time
import subprocess
from grovepi import *

import json
from collections import OrderedDict
import pprint



routerFlag =False #routerネットに繋がらない回線がONで１
#flag2 =False
sub =""
time.sleep(1)


def router():
	
    global routerFlag
    global sub
    #global flag2
                
    if routerFlag == 1:
	#onにする
	#subprocess.call(['sudo','ip','set','wlan1','up'])

	#subprocess.call(['sudo','sed','-i','s/Wi-Pi-OPEN.conf/hostapd.conf/g','/etc/default/hostapd'])
	#subprocess.call(['sudo','systemctl','restart','dhcpcd'])
	#subprocess.call(['sudo','systemctl','restart','hostapd'])
	led()
	led_subprocess()
	print("subpro1")
	
	
        routerFlag=0
	#flag2=1
        print("router ON :"+ str(routerFlag))
	

	
    else:
	#off
	#subprocess.call(['sudo','ip','set','wlan1','down'])

	#subprocess.call(['sudo','sed','-i','s/hostapd.conf/Wi-Pi-OPEN.conf/g','/etc/default/hostapd'])
	#subprocess.call(['sudo','systemctl','restart','dhcpcd'])
	#subprocess.call(['sudo','systemctl','restart','hostapd'])
	led()
	sub.kill()
	print("subpro2")
	
	routerFlag= 1 
	#flag2= 0
	print("router OFF :"+ str(routerFlag))
		


def led():
    led = 7
	
    #Blink the LED
    digitalWrite(led,1)     # Send HIGH to switch on LED
    print ("LED ON!")
    time.sleep(3)

    digitalWrite(led,0)     # Send LOW to switch off LED
    print ("LED OFF!")
    time.sleep(3)
	
	
	

    
def led_subprocess():
    global sub
    global routerFlag
    if(routerFlag  != 1):
	sub=subprocess.Popen(['python','/home/pi/Desktop/Wi-Pi-System/test/Other/led_thread.py'])


def main():
    try:
	print("いんすたんす？")
	g=grove_gesture_sensor.gesture()
	print("ｇ init")
	g.init()
	print("initfin")
    
	#ledd = threading.Thread(target=led)
    except IOError:
	g.init()
	print("IOE 1nitmain")
	pass
    
    try:
	while True:
	    time.sleep(0.1)
	    gest=g.return_gesture()

	    #Match the gesture
	    if gest==g.FORWARD:
		print("FORWARD")
		time.sleep(1)
		router()


	    elif gest==g.DOWN:
		print("DOWN")
		time.sleep(1)
		router()
		    	
	    else :
		time.sleep(.1)
    

	#elif gest==0:
	#    led()
    except IOError:
	global routerFlag
	print("__________________/ntry/n________________")
	subprocess.call(['i2cdetect', '-y', '1'])
	subprocess.Popen(['python','/home/pi/Desktop/Wi-Pi-System/test/Gesture/ges-subprocess.py'])

	print("IOE  sub kill")
	sub.kill()
	
	with open('/home/pi/Desktop/Wi-Pi-System/test/Data/Wi-Pi.json','w') as f:
	    df['routerFlag']=routerFlag
	    json.dump(df, f)
	
            
"""

            
'''
        elif gest==g.RIGHT:
            print("RIGHT")
            time.sleep(1)
            router()
        elif gest==g.LEFT:
            
            print("LEFT")
            time.sleep(1)
            router()
            
        elif gest==g.UP:
            print("UP")
            time.sleep(1)
	    print("router")
            router()

'''
        elif gest==g.CLOCKWISE:
            print("CLOCKWISE")
    #        time.sleep(1)
            led()
        elif gest==g.ANTI_CLOCKWISE:
            print("ANTI_CLOCKWISE")
   #         time.sleep(1)
            led()
        elif gest==g.WAVE:
            print("WAVE")
   #         time.sleep(1)
            led()

"""
    
if __name__ == '__main__':
    global routerflag
    with open('/home/pi/Desktop/Wi-Pi-System/test/Data/Wi-Pi.json','r') as f:
	df = json.load(f)
	routerFlag = df['routerFlag']
	led_subprocess() #再起動後用
    main()
