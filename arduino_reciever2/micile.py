# --------------------------------------------------
# network_client.py
# --------------------------------------------------
 
# import the libraries
from ez_graphics_09 import *
from ez_network_09 import *
import time
 
# clear the screen
clear_screen('black')
 
# create a new network link
netlink = create_networklink()
 
# discover other network links
set_color('white')
draw_text('discovering peers on network', 100, 100)
peers = []
while peers == []:
    peers = netlink.discover_peers()
print peers
 
# connect to the first peer we find
draw_text('connecting to' + peers[0], 100, 120)
netlink.connect(peers[0])
 
# start sending the numbers 0 to 9
for i in range(0, 10):
    data = 'value = %d ' % i
    draw_text('sending "%s"' % data, 100, 140 + i * 20)
    netlink.send(data)
    time.sleep(1)           