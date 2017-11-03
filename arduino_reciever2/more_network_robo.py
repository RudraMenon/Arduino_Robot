from ez_arduino_09 import *
import time
from ez_network_09 import *
# --------------------------------------------------
# touchscreen_single_demo.py
# --------------------------------------------------
 
# import the ez_touchscreen library v0.9
# import the ez_graphics library v0.9
from ez_graphics_09 import *
from ez_camera_09 import *

print os.path.exists('/dev/ttyACM0')

ACTION_STOP = 'STOP'
ACTION_FORWARD  = 'FORWARD'
ACTION_BACKWARD  = 'BACKWARD'
ACTION_ROTATE_LEFT  = 'LEFT'
ACTION_ROTATE_RIGHT = 'RIGHT'

motor_duty_cycle = 0.3

def initialize_arduino():
    try: 
        # initialize the Arduino
        arduino_init()
        
        # initialize motor control pins
        arduino_configure_pin(PIN_5, PIN_PWM)
        arduino_configure_pin(PIN_6, PIN_PWM)
        arduino_configure_pin(PIN_9, PIN_PWM)
        arduino_configure_pin(PIN_10, PIN_PWM)
    except Exception, e:
        print e
        initialize_arduino()
        

def drive(action):
    try:
        if action == ACTION_STOP:
            arduino_set_pwm(PIN_5, 0)
            arduino_set_pwm(PIN_6, 0)
            arduino_set_pwm(PIN_9, 0)
            arduino_set_pwm(PIN_10, 0)
        if action == ACTION_FORWARD:
            arduino_set_pwm(PIN_5, motor_duty_cycle* 3)  #
            arduino_set_pwm(PIN_6, 0)
            arduino_set_pwm(PIN_9, 0)
            arduino_set_pwm(PIN_10,motor_duty_cycle* 3)
        if action == ACTION_BACKWARD:
            arduino_set_pwm(PIN_5, 0)
            arduino_set_pwm(PIN_6, motor_duty_cycle* 3) # top right
            arduino_set_pwm(PIN_9, motor_duty_cycle* 3) # bottom right
            arduino_set_pwm(PIN_10,0)
            
        if action == ACTION_ROTATE_RIGHT:
            arduino_set_pwm(PIN_5, motor_duty_cycle * 3)                   #front left
            arduino_set_pwm(PIN_6, 0)    #back left
            arduino_set_pwm(PIN_9, 0)                   #front right
            arduino_set_pwm(PIN_10,motor_duty_cycle * .5)   #back right
        if action == ACTION_ROTATE_LEFT:
            arduino_set_pwm(PIN_5, motor_duty_cycle * .5)
            arduino_set_pwm(PIN_6, 0)
            arduino_set_pwm(PIN_9, 0)
            arduino_set_pwm(PIN_10, motor_duty_cycle * 3)
    except Exception, e:
        print e
        initialize_arduino()
        
#initialize_arduino()



# clear the screen
clear_screen('black')
sw = get_screen_width()
# create a new network link
netlink = create_networklink()
 
# discover other network links
set_color('white')
draw_text('discovering peers on network', 100, 100)
peers = []
while peers == []:
    peers = netlink.discover_peers()
 
# connect to the first peer we find
draw_text('connecting to' + peers[0], 100, 120)
while not netlink.connected:
    netlink.connect(peers[0])

clear_screen('white')
image = load_image('micile.jpg')
image = resize_image(image,480,480)
draw_image(image,160,0)
clear_screen('black')
data = None
while True:
    while data == None:
        data = netlink.pop_received_data()
#        select_camera(FRONT_CAMERA)
#        for i in range(5):
#            image =  camera_capture_image()
#        draw_image(image,0,0)
#        image_string = save_image_to_string(image)
#        netlink.send(image_string)
#        data = netlink.pop_received_data()
#        if not netlink.connected:
#            clear_screen('black')
#            peers = []
#            print peers
#            while peers == []:
#                peers = netlink.discover_peers()
            
#            netlink.connect(peers[0])
    if data[0] == 'image' or data[0] == 'capture' or data[0] == 'draw':
        if data[0] == 'image':
            image = load_image_from_string(data[1])
            draw_image(image,75,0)
        if data[0] == 'capture':
            image =  camera_capture_image()
            image_string = save_image_to_string(image)
            select_camera(FRONT_CAMERA)
            netlink.send(image_string)
        if data[0] == 'draw':
            print 'in1'
            if data[1] == 'clear':
                clear_screen(get_color())
            else:
#                print data[1][0]
                for i in data[1]:
                    if i[0] == 'color':
                        set_color(i[1][0],i[1][1],i[1][2])
                    else:
                        fill_circle(i[0][0],i[0][1],i[0][2])
                data = None
    else:
        print data[0]
        drive(data[0])
        data = None
    time.sleep(0.05)
#    while data != None:
#        data = netlink.pop_received_data()


