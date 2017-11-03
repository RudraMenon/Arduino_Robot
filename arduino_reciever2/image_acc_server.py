from ez_hardware_09 import*
from ez_graphics_09 import*
from ez_network_09 import*


clear_screen('black')
netlink = create_networklink()
set_color('white')
draw_text('Waiting for connection', 100, 100)
netlink.listen_for_connection()
while not netlink.connected:
    time.sleep(1)


x = 0
y = 0
 
 
# main loop
calibrate_accelerometer()
sending2 = None
while True:
    data = None
        
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
        data = None
        data = netlink.pop_received_data()
        if data != None:
            draw_image(load_image_from_string(data),80,0)
#    break
    # sleep
    time.sleep(0.01)