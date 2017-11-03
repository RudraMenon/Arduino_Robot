from ez_arduino_09 import *
import time

# --------------------------------------------------
# touchscreen_single_demo.py
# --------------------------------------------------
 
# import the ez_touchscreen library v0.9
# import the ez_graphics library v0.9
from ez_touchscreen_09 import *
from ez_graphics_09 import *
 



ACTION_STOP = 'STOP'
ACTION_FORWARD  = 'FORWARD'
ACTION_BACKWARD  = 'BACKWARD'
ACTION_ROTATE_LEFT  = 'LEFT'
ACTION_ROTATE_RIGHT = 'RIGHT'

motor_duty_cycle = 0.25

def initialize_arduino():
    # initialize the Arduino
    arduino_init()
    
    # initialize motor control pins
    arduino_configure_pin(PIN_5, PIN_PWM)
    arduino_configure_pin(PIN_6, PIN_PWM)
    arduino_configure_pin(PIN_9, PIN_PWM)
    arduino_configure_pin(PIN_10, PIN_PWM)

def drive(action):
    if action == ACTION_STOP:
        arduino_set_pwm(PIN_5, 0)
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, 0)
#        arduino_write_pin(PIN_5, False)
#        arduino_write_pin(PIN_6, False)
#        arduino_write_pin(PIN_9, False)
#        arduino_write_pin(PIN_10, False)
    if action == ACTION_FORWARD:
        arduino_set_pwm(PIN_5, motor_duty_cycle)  #
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, 0)
    if action == ACTION_BACKWARD:
        arduino_set_pwm(PIN_5, 0)                   #front left
        arduino_set_pwm(PIN_6, motor_duty_cycle)    #back left
        arduino_set_pwm(PIN_9, 0)                   #front right
        arduino_set_pwm(PIN_10, 0)   #back right
    if action == ACTION_ROTATE_LEFT:
        arduino_set_pwm(PIN_5, 0)
        arduino_set_pwm(PIN_6,0) # top right
        arduino_set_pwm(PIN_9, motor_duty_cycle * 3) # bottom right
        arduino_set_pwm(PIN_10, 0)
    if action == ACTION_ROTATE_RIGHT:
        arduino_set_pwm(PIN_5, 0)
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, motor_duty_cycle * 3)
        
initialize_arduino()
#drive(ACTION_FORWARD)
#print "Forward"
#time.sleep(3)
#drive(ACTION_BACKWARD)
#print "backward"
#time.sleep(3)
#drive(ACTION_ROTATE_LEFT)
#print "Left"
#time.sleep(3)
#drive(ACTION_ROTATE_RIGHT)
#print "Right"
#time.sleep(3)
#drive(ACTION_STOP)



# clear the screen
clear_screen('black')
sw = get_screen_width()
sh = get_screen_height()
set_color('red')

draw_rect(400,50,100,100,'green')
draw_rect(400,350,100,100,'green')
draw_rect(200,200,100,100,'green')
draw_rect(600,200,100,100,'green')

# main loop
while True:
    # read a single finger point from the touchscreen
    touch_point = touchscreen_finger_point()
    if touch_point != None:
        # get the x and y coordinates of the touch
        x = touch_point['x']
        y = touch_point['y']

        if (x >400)and (x < 500) and (y > 50) and (y < 150):
            drive(ACTION_FORWARD)
            time.sleep(0.05)
        if (x >400)and (x < 500) and (y >350) and (y < 450):
            drive(ACTION_BACKWARD)
            time.sleep(0.05)
        if (x >200)and (x < 300) and (y >200) and (y < 300):
            drive(ACTION_ROTATE_LEFT)
            time.sleep(0.05)
        if (x >600)and (x < 700) and (y >200) and (y < 300):
            drive(ACTION_ROTATE_RIGHT)
            time.sleep(0.05)
    else:
        drive(ACTION_STOP)


