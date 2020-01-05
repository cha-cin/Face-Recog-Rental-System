from machine import PWM, Pin
import time
import network
import socket 

servo = PWM(Pin(4), freq=50)

def do_connect():
	SSID = 'Jiahsin iPhone'
	PASSWORD = 'hellojiahsin'

	sta_if = network.WLAN(network.STA_IF)
	ap_if = network.WLAN(network.AP_IF)
	if ap_if.active():
		ap_if.active(False)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(SSID, PASSWORD)
		while not sta_if.isconnected():
			pass
	print('Network configuration:', sta_if.ifconfig())
	ip = socket.gethostbyname('http://140.115.87.73:3000/')
	print(ip)


def main():
	do_connect()
	# for i in range(10):
	# 	servo.duty(50)
	# 	time.sleep(1)
	# 	servo.duty(100)
	# 	time.sleep(1)
	#data = socketObject.listen('micro_servo_client')

if __name__ == "__main__":
	main()
