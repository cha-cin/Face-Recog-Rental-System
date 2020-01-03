import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(17, GPIO.OUT)
GPIO.cleanup()
