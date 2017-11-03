# --------------------------------------------------
# Arduino_PWM_demo.py
# --------------------------------------------------
 
# Shows how to use the Arduino PWM
 
# import the ez_arduino libary v0.9 and the time library
from ez_arduino_09 import * 
import time
 
# Initialize the Arduino
arduino_init()
 
# Configure Pins for an SPI device
arduino_configure_pin(PIN_9, PIN_PWM)
 
# Configure for a 25% duty cycle
arduino_set_pwm(PIN_9, 0.25)
 
# Loop forever
while True:
    # sleep so app will stop when interrupted by the IDE
    time.sleep(0.01)     