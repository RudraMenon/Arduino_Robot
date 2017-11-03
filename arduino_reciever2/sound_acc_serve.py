from ez_hardware_09 import*
from ez_graphics_09 import*
from ez_network_09 import*
from ez_touchscreen_09 import*
from ez_sound_09 import *
clear_screen('black')
netlink = create_networklink()
set_color('white')
draw_text('Waiting for connection', 100, 100)
netlink.listen_for_connection()
while not netlink.connected:
    time.sleep(1)

clear_screen('black')
set_color('white')
draw_rect(680,20,100,210)
draw_rect(680,230,100,210)
 
# main loop
calibrate_accelerometer()
sending2 = None
x = 0
y = 0
while True:
    touch = touchscreen_finger_point()
    while touch != None:
        x = touch['x']
        y = touch['y']
        if x > 680 and y < 240:
            calibrate_accelerometer()
            try:
                netlink.send('send_pic')
                print 'send'
            except Exception,e:
                print e
                if not netlink.connected:
                    clear_screen('black')
                    netlink.listen_for_connection()
                while not netlink.connected:
                    time.sleep(.5)
            data = None
            while data == None:
                data = netlink.pop_received_data()
            print data
            clear_screen('black')
    #        drive('STOP')
            draw_image(load_image_from_string(data),0,0)
            touch = None
        if x > 680 and y > 240:
            netlink.send(['STOP',0,0,0,0])
            set_color('red')
            fill_circle(100,100,20)
            capture_sound_start(8000,3.5)
            sound = get_captured_sound()
            play_sound(sound)
            set_color('black')
            fill_rect(0,0,150,150)
            sound_string = save_sound_to_string(sound)
            netlink.send('sound',sound_string)
            break
                
    # read the accelerometer
    xyz = read_accelerometer()
    
    # format the values in a nice string
    s = "X:%4d Y:%4d Z:%4d" % (xyz[0], xyz[1], xyz[2])
    
    # update the rectangle position
    x = (x + xyz[0]) % 780  # modulus by 780
    y = (y + xyz[1]) % 460  # modules by 460
    backward = 0
    forward = 0
    right = 0
    left = 0
    if xyz[1] > 30:
        backward = (xyz[1] - 30) * 3/50
    if xyz[1] < - 30:
        forward = -1 * (xyz[1] + 30) * 3/50
    if xyz[0] > 30:
        right = (xyz[0] - 30) * 3/50
    if xyz[0] < -30:
        left = (xyz[0] - 30) * 3/50
    if right > 3:
        right =3
    if left < -3:
        left = -3
    if forward > 3:
        forward = 3
    if backward > 3:
        backward = 3
        
    motor_duty = .25
    tilt = [forward,backward,right,left*-1]
    print tilt
    action_list = ['FORWARD','BACKWARD','RIGHT','LEFT']
    action = action_list[tilt.index(max(tilt))]
    if tilt == [0,0,0,0]:
        action = 'STOP'
    print action
    sending = [action,forward,backward,right,left*-1]
    if sending != sending2:
        try:
            netlink.send(sending)
        except Exception,e:
            print e
            if not netlink.connected:
                clear_screen('black')
                netlink.listen_for_connection()
            while not netlink.connected:
                time.sleep(.5)
        sending2 = sending
        set_color('black')
        fill_rect(0,0,800,20)
        fill_rect(780,0,20,480)
        fill_rect(0,0,20,480)
        fill_rect(0,460,800,20)
        set_color('yellow')
        if action == 'FORWARD':
            fill_rect(0,0,800,20)
        if action == 'RIGHT':
            fill_rect(780,0,20,480)
        if action == 'LEFT':
            fill_rect(0,0,20,480)
        if action == 'BACKWARD':
            fill_rect(0,460,800,20)
    set_color('yellow')
    
    
    # sleep
    time.sleep(0.01)