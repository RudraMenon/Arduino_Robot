#--------------------------------------------
# Rudra Menon
# Arduino RC Car Remote
#--------------------------------------------
# import graphics, network,touchscreen,camera, and time
from ez_graphics_09 import *
from ez_network_09 import *
from ez_touchscreen_09 import*
from ez_camera_09 import *
import time 

clear_screen('black')
netlink = create_networklink()
# wait for a connection
set_color('white')
draw_text('Waiting for connection', 100, 100)
netlink.listen_for_connection()
while netlink.connected == False:
    time.sleep(.5)
#draw background
clear_screen('black')
set_color('white')
draw_image(load_image('send.jpg'),700,0)
draw_image(load_image('get.jpg'),700,120)
draw_image(load_image('draw.jpg'),700,240)
draw_image(load_image('ctrl.jpg'),700,360)
draw_rect(700,0,100,120)
draw_rect(700,120,100,120)
draw_rect(700,240,100,120)
draw_rect(700,360,100,120)
# Main Loop
while True:
    if not netlink.connected:
        listen_for_connection()
        while not netlink.connected:
            time.sleep(1)
    touch = touchscreen_finger_point()
    if touch != None:
        x = touch['x']
        y = touch['y']
#       choose one of the options (send picture, recieve picture, send drawing, control car)
        if x > 700:
#           Send picture option
            if y < 120:
                set_color('black')
                fill_rect(0,0,700,480)
                while touch != None:
                    x = touch['x']
                    y = touch['y']
                    touch = touchscreen_finger_point()
#                   capture image
                    image = camera_capture_image()
#                   draw image
                    draw_image(image,0,0)
#                convert image to string
                image_string = save_image_to_string(image)
#                send the string to other tablet
                netlink.send(['image',image_string])
#           recieve image from other tablet
            if 120 < y < 240:
                set_color('black')
                fill_rect(0,0,700,480)
#               send message to other tablet
#                the other tablet will capture an image and send it to this one
                netlink.send(['capture'])
                image_string = None
#                recieve data
                while image_string == None:
                    image_string = netlink.pop_received_data()
#                convert string to image
                image2 = load_image_from_string(image_string)
#                draw image
                draw_image(image2,0,0)
                while touch != None:
                    touch = touchscreen_finger_point()
#            Draw option
            if 240 < y < 360:
#                draw background
                colors = ['white','black','red','orange','yellow','green','blue']
                for i in range(len(colors)):
                    set_color(colors[i])
                    fill_rect(i*100,0,100,50)
                set_color('white')
                fill_rect(0,50,700,10)
                draw_rect(0,430,100,50)
                red = 255
                green = 255
                blue = 255
                
                while touch != None:
                    touch = touchscreen_finger_point()
                first = True
                draw = False
                draw_list = []
                while True:
                    touch = touchscreen_finger_point()
                    if touch != None:
                        x = touch['x']
                        y = touch['y']
#                        if user are touching option panel, stop drawing
                        if x > 700:
                            break
#                        if touch point is on the color panel, change color to 
#                         the color being touched
                        if y < 50:
                            c     = get_pixel_color(x, y)
                            red   = (c >> 16) & 255
                            green = (c >>  8) & 255
                            blue  = (c >>  0) & 255
                            set_color(red,green,blue)
#                            add the color chosen to the list that will be sent
                            draw_list.append(['color',[red,green,blue]])
                        else:
#                            draw a dot where user touhes
                            if x < 700 and y > 50:
                                fill_circle(x,y,5)
#                                add the coordinates of each dot to the list 
#                                 that will be sent
                                draw_list.append([[x+75,y]])
                        draw = True
                        first = True
                    else:
#                        after user stop touching the screen, wait .2 seconds 
#                         before sending listj
                        if first:
                            stop = time.time() + .2
                            first = False
                        if (time.time() > stop) and draw and first == False:
                            netlink.send(['draw',draw_list])
                            first = True
                            draw = False
                            draw_list = []
                            
#            Controls option
            if 360 < y :
#                draw controls
                set_color('black')
                fill_rect(0,0,700,480)
                set_color('white')
                draw_image(resize_image(load_image('arrrow_up.jpg'),100,100),175,0)
                draw_image(resize_image(load_image('arrow_down.jpg'),100,100),175,380)
                draw_image(load_image('arrow_right.jpg'),525,0)
                draw_image(load_image('arrow_left.jpg'),0,0)
#                draw_image(load_image('stop.jpg'),175,180)
                draw_rect(0,0,175,480)
                draw_rect(175,0,350,100)
                draw_rect(175,380,350,100)
                draw_rect(525,0,175,480)
                while touch != None:
                    touch = touchscreen_finger_point()
                instruct = None
                stopped = True
                last_click = None
                while True:
                    touch = touchscreen_finger_point()
                    if touch != None:
                        x = touch['x']
                        y = touch['y']
                        if x < 175:
#                             if user touches the left side, make instruct = 'left'
                            instruct = ['LEFT']
                            last_click = time.time()
                        if 175 < x < 525:
                            if y < 100:
                                instruct = ['FORWARD']
                                last_click = time.time()
                            if y > 380:
                                instruct = ['BACKWARD']
                                last_click = time.time()
                        if 700 > x > 525:
                            instruct = ['RIGHT']
                            last_click = time.time()
                        if 175 < x < 350 and 100 < y < 380:
                            print 'stop'
                            instruct = ['STOP']
                        if x > 700 and y < 360:
                            break
                    else:
                        if last_click != None:
                            if time.time() > last_click + .1:
                                last_click = None
                                print 'stop'
                                instruct = ['STOP']
                    if instruct != None:
#                        send whichever direction was touched
                        netlink.send(instruct)
                        instruct = None
    