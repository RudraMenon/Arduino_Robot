from ez_sound_09 import*
from ez_network_09 import*
from ez_graphics_09 import*

sound = load_sound('cartoon001.wav')
netlink = create_networklink()
clear_screen('white')
netlink.listen_for_connection()

# start sending random numbers
while not netlink.connected:
    time.sleep(1) 
clear_screen('black')
print 'sound'
netlink.send(sound)