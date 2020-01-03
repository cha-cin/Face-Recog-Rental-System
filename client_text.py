import socketio
import RPi.GPIO as GPIO
import time




sio = socketio.Client()
sio.connect('http://127.0.0.1:3000/')

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)


p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

@sio.on('micro_servo_client')
def control_micro_servo(data):
    global p
    if data == "true":
        p.start(0) # Initialization
        try:
            for a in range(100):
                p.ChangeDutyCycle(11)
                time.sleep(0.01)
            for b in range(100):
                p.ChangeDutyCycle(4)
                time.sleep(0.01)
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
    else:
        print("not have author")
