from __future__ import print_function
import RPi.GPIO as GPIO
import datetime
import time
import signal
import sys
import os

# Configuration

# Debug output?
DEBUG = True

# BCM pin used to drive PWM fan
FAN_PIN = 18

# Time to wait between each refresh in [s]
WAIT_TIME = 10

# Frequency for PWM control in [Hz]
PWM_FREQ = 200

# Configurable temperature in [deg C] and fan speed in [%]
MIN_TEMP = 45
MAX_TEMP = 70
FAN_LOW = 0
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100

# Get CPU temperature
def getCpuTemperature ( ) :
	res = os.popen ( 'vcgencmd measure_temp' ) .readline ( )
	temp = ( res.replace ( "temp=", "" ) .replace ( "'C\n","" ) )
	return temp

# Set fan speed as duty cycle [0..100]
def setFanSpeed ( speed ) :
	fan.start ( speed )
	return ( )

# Handle fan speed
def handleFanSpeed ( ) :
	temp = float ( getCpuTemperature ( ) )
	# Turn off the fan if the temperature is below MIN_TEMP
	if temp < MIN_TEMP :
		setFanSpeed ( FAN_OFF )
		fanspeed = FAN_OFF
	# Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
	elif temp > MAX_TEMP :
		setFanSpeed ( FAN_MAX )
		fanspeed = FAN_MAX
	# Caculate dynamic fan speed
	else :
		step = ( FAN_HIGH - FAN_LOW ) / ( MAX_TEMP - MIN_TEMP)
		cooltemp = temp - MIN_TEMP
		fanspeed = FAN_LOW + ( round ( cooltemp ) * step )
		setFanSpeed ( fanspeed )
	if DEBUG :
		print ( datetime.datetime.now ( ) .isoformat ( " " ), "%.2f" % temp, "%.2f" % fanspeed )
	return ( )

try :
	# Setup GPIO pin
	GPIO.setwarnings ( False )
	GPIO.setmode ( GPIO.BCM )
	GPIO.setup ( FAN_PIN, GPIO.OUT, initial = GPIO.LOW )
	fan = GPIO.PWM ( FAN_PIN, PWM_FREQ )
	setFanSpeed ( FAN_OFF )
	# Handle fan speed every WAIT_TIME sec
	while True :
		handleFanSpeed ( )
		time.sleep ( WAIT_TIME )

except KeyboardInterrupt :
	# trap a CTRL+C keyboard interrupt
	setFanSpeed ( FAN_HIGH )
	# resets all GPIO ports used by this function
	fan.stop ( )
	GPIO.cleanup ( )

#
