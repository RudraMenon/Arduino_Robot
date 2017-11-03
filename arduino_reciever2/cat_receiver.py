from ez_hardware_09 import *
from ez_graphics_09 import *
import time
from ez_arduino_09 import *
from ez_network_09 import*

clear_screen('black')
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
    if action == 'STOP':
        arduino_set_pwm(PIN_5,0)  #
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, 0)
    if action == 'LOAD':
        arduino_set_pwm(PIN_5, motor_duty_cycle * 3)  #
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, 0)
    if action == ACTION_BACKWARD:
        arduino_set_pwm(PIN_5, 0)                   #front left
        arduino_set_pwm(PIN_6, motor_duty_cycle * 3)    #back
        arduino_set_pwm(PIN_9, 0)                   #front right
        arduino_set_pwm(PIN_10, 0)   #back right
    if action == 'FIRE':
        arduino_set_pwm(PIN_5, 0)
        arduino_set_pwm(PIN_6,0) # top right
        arduino_set_pwm(PIN_9, motor_duty_cycle * 3) # SHOOT
        arduino_set_pwm(PIN_10, 0)
    if action == ACTION_FORWARD:
        arduino_set_pwm(PIN_5, 0)
        arduino_set_pwm(PIN_6, 0)
        arduino_set_pwm(PIN_9, 0)
        arduino_set_pwm(PIN_10, motor_duty_cycle * 3) # FORWARD
initialize_arduino()
# init
x = 0
y = 0
 
clear_screen('black')
netlink = create_networklink()
set_color('white')
draw_text('discovering peers on network', 100, 100)
peers = []
while peers == []:
    peers = netlink.discover_peers()
print peers
draw_text('connecting to' + peers[0], 100, 120)
netlink.connect(peers[0])


while True:
    data = None
    while data == None:
        data = netlink.pop_received_data()
    print data
    if data == 'FIRE':
        drive('STOP')
        drive('FIRE')
        time.sleep(2)
        drive('LOAD')
        time.sleep(2)
        drive('STOP')
    else:
        drive(data)