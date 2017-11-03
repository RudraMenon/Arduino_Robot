# --------------------------------------------------
# accelerometer_demo.py
# --------------------------------------------------
 
# import the ez_hardware library v0.9
# import the ez_graphics library v0.9
from ez_hardware_09 import *
from ez_graphics_09 import *
import time
 
# init
x = 0
y = 0
 
 
# main loop
while True:
    # read the accelerometer
    xyz = read_accelerometer()
    
    # format the values in a nice string
    s = "X:%4d Y:%4d Z:%4d" % (xyz[0], xyz[1], xyz[2])
    
    # update the rectangle position
    x = (x + xyz[0]) % 780  # modulus by 780
    y = (y + xyz[1]) % 460  # modules by 460
    
    # clear the screen
    clear_screen('black')
     
    # draw the text and rectangle
    set_text_size(20)
    set_color('yellow')
    draw_text(s, 50, 100)
    fill_rect(x, y, 20, 20)
    
    # sleep
    time.sleep(0.1)