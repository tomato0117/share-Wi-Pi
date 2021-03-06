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
#LED,Gesture
import grove_gesture_sensor
from grovepi import *

#ほか
import time

import sys
import subprocess


#Json関連
import json
from collections import OrderedDict
#import pprint


routerFlag =False #セキュア回線をONにしている際にTrue(1)



def router():
#セキュア回線のONOFF関連のまとめ

    global routerFlag

                
    if routerFlag == True:
	#onにする
	sub = subprocess.call(['sudo','ip','l','set','wlan1','up']) 
	if sub==1:
		print('\n\n\nトングル繋がってますか？\n\n')
	print("Turn on secure line")

	led("send")
	
        #print("router ON  routerFlag:"+ str(routerFlag))

	
    else:
	#off
	sub = subprocess.call(['sudo','ip','l','set','wlan1','down'])
	if sub==1:
		print('\n\n\nトングル繋がってますか？\n\n')
	print("Turn off secure line")


	led("send")
	
	#print("router OFF routerFlag:"+ str(routerFlag))
		



    
    
def led(job):
    global	routerFlag
    led = 7
    if job=="send":
	#回線開放中
	if (routerFlag==True):
		#Blink the LED
		digitalWrite(led,1)		# Send HIGH to switch on LED
		print ("router LED ON!")
		
	else:
		digitalWrite(led,0)		# Send LOW to switch on LED
		
    elif job=="recog":
	#Gesture認識
	for num in range(5):
		#Blink the LED
		digitalWrite(led,1)    
		#print ("LED ON!")
		time.sleep(0.1)

		digitalWrite(led,0)    
		#print ("LED OFF!")
		time.sleep(0.1)
	
    elif job=="wakeup":
	for num in range(5):
	#プログラム起動時
		#Blink the LED
		digitalWrite(led,1)   
		#print ("LED ON!")
		time.sleep(0.05)

		digitalWrite(led,0)     
		#print ("LED OFF!")
		time.sleep(0.05)
	
	

def main():
    global routerFlag
    try:
	g=grove_gesture_sensor.gesture()
 	g.init() 
	print("Welcome to the Wi-Pi")
	subprocess.call(['sudo','ip','l','set','wlan0','up']) #public line ON

    except IOError:
    #なぜかラズパイ起動後には必ず１回IOErrorが出るためリスタートしている g.init() 部分
	print("wake-up Error Resterting")
	main()
	pass
    
    try:
	while True:
	    gest=g.return_gesture()

	    #Match the gesture
	    if gest==g.FORWARD:
		print("FORWARD")
		
		led("recog")
		routerFlag =True
		router()
		time.sleep(1)

	    elif gest==g.DOWN:
		print("DOWN")
		
		led("recog")
		routerFlag =False
		router()
		time.sleep(1)   

		
	    else :
		time.sleep(.01)

    except IOError:#意図しない強制終了の際に、プログラムを再起動させる
	print("__________________\n try \n________________")
	subprocess.Popen(['python','/home/pi/Desktop/Wi-Pi-System/main/Wi-Pi.py'])
	time.sleep(2)

    except KeyboardInterrupt: 
	print("Ctrl +C ")
	digitalWrite(7,0)
	#↓プログラム強制終了時に回線をOFFにするため落とす
	
	subprocess.call(['sudo','ip','l','set','wlan0','down']) #public line off
	subprocess.call(['sudo','ip','l','set','wlan1','down']) #secure line off
	print("Turn off secure line")
	print("See you")
	sys.exit()

if __name__ == '__main__':
    global routerflag
    led("wakeup")
    with open('/home/pi/Desktop/Wi-Pi-System/main/Wi-Pi.json','r') as f:
	df = json.load(f)
	routerFlag = df['routerFlag']
    main()
