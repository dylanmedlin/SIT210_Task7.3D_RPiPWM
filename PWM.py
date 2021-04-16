import RPi.GPIO as GPIO
import time

trig = 12
echo = 10
led = 8

GPIO.setmode(GPIO.BOARD)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
pwm = GPIO.PWM(led, 1000)
pwm.start(100)

GPIO.output(led, GPIO.HIGH)

def distance():
    # set Trigger to HIGH
    GPIO.output(trig, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

try:
    while True:
        
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        
        # make range 0cm - 20cm
        if dist > 20:
            dist = 20
        
        # conver to 0 - 100
        dist = (dist / 20) * 100
        print (dist)

        # update led (less distance = brighter)
        pwm.ChangeDutyCycle(int(100 - dist))
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()