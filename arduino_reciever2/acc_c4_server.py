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
draw_rect(580,20,100,210)

x = 0
y = 0

####
board = []
def make_board():
    global board
    clear_screen('black')
    set_color('white')
    for x in range(0,8):
        draw_line(x*60 + 190,60,x*60 + 190,480)
    for y in range(0,8):
        draw_line(190,(y + 1) *60,610,(y+1) *60)
    board = []
    for i in range(0,7):
        board.append([0,0,0,0,0,0,0])
slot = None
def choose_slot(player):
    global slot
    slot = None
    set_color('black')
    fill_rect(190,0,420,50)
    while True:
        touch = touchscreen_finger_point()
        if touch != None:
            x = touch ['x']
            y = touch ['y']
            if 190 < x < 610 and y < 60:
                slot = (x - 190) / 60
                set_color('black')
                fill_rect(190,0,420,50)
                if player == 1:
                    set_color('red')
                if player == 2: 
                    set_color('blue')
                draw_rect((slot * 60) + 215,20,10,30)
            if x > 700 and y > 430 and slot != None:
                drop(player)
                break
def drop(player):
    global board,slot
    lowest_block = 6
    tokens = [0,'red.jpg','blue.jpg']
    for row in board:
        if row[slot] != 0:
            lowest_block = board.index(row) - 1
            break
    if lowest_block < 0:
        choose_slot(player)
    else:
        board[lowest_block][slot] = player
        draw_image(resize_image(load_image(tokens[player]),59,59),(slot * 60) + 191,((lowest_block * 60) +61))
    
def check_win(player,board):
    
    for row in board:
        count = 0
        for box in row:
            if box == player:
                count = count + 1
                if count == 4:
                    set_text_size(100)
                    draw_text('PLAYER ' + str(player) + 'WINS!!!',0,200)
                    time.sleep(3)
                    main()
            else:
                count = 0
    for col in range(0,len(board)):
        count = 0
        for row in board:
            if row[col] == player:
                count = count + 1
                if count == 4:
                    set_text_size(100)
                    draw_text('PLAYER ' + str(1) + 'WINS!!!',0,200)
                    time.sleep(3)
                    main()
            else:
                count = 0
def diagonal(player,board):
    diag_left = []
    row = 0
    col = 7
    for vert in range(6,-1,-1):
        col = vert
        row = 0
        curr_diag =  []
        while row < 7 and col < 7:
            curr_diag.append(board[row][col])
            col = col + 1
            row = row + 1
        diag_left.append(curr_diag)
    for hori in range(1,7):
        row = hori
        col = 0
        curr_diag =  []
        while row < 7 and col < 7:
            curr_diag.append(board[row][col])
            row = row + 1
            col = col + 1
        diag_left.append(curr_diag)
    diag1 = []
    diag2 = []
    for row in diag_left[::2]:
        if len(row) < 7:
            row = [0] *((7-len(row))/2) + row + [0] *((7-len(row))/2)
        diag1.append(row)
    for row in diag_left[1::2]:
        if len(row) < 6:
            row = [0] *((6-len(row))/2) + row + [0] *((6-len(row))/2)
        diag2.append(row)
    check_win(player,diag1)
    check_win(player,diag2)

def main():
    global board,slot
    make_board()
    player = 1
    while True:
        choose_slot(player)
        check_win(player,board)
        diagonal(player,board)
        netlink.send(slot)
        opp_slot = None
        while opp_slot == None:
            opp_slot = netlink.pop_received_data()
        player = 2
        slot = opp_slot
        drop(player)
        check_win(player,board)
        diagonal(player,board)
        player = 1
 
# main loop
calibrate_accelerometer()
sending2 = None

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
            netlink.send('game')
            main()
            
                
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