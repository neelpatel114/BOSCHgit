import json 
import time

forward_control = {"action": "1", "speed": 0.15}
backward_control = {"action": "1", "speed": -0.18}
stop_control = {"action": "1", "speed": 0.00}
left_control = {"action": "2", "steerAngle": -20.5}
right_control = {"action": "2", "steerAngle": 20.5}
slight_left_control = {"action": "2", "steerAngle": -10.5}
slight_right_control = {"action": "2", "steerAngle": 10.5}
straight_control = {"action": "2", "steerAngle": 0.00}


post_command_delay = 2
def forward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(forward_control, outfile)
    time.sleep(post_command_delay)

def right_forward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(right_control, outfile)
    time.sleep(1)
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(forward_control, outfile)
    time.sleep(post_command_delay)

def left_forward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(left_control, outfile)
    time.sleep(1)
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(forward_control, outfile)
    time.sleep(post_command_delay)

def backward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(backward_control, outfile)
    time.sleep(post_command_delay)

def left_backward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(left_control, outfile)
    time.sleep(1)
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(backward_control, outfile)
    time.sleep(post_command_delay)

def right_backward():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(right_control, outfile)
    time.sleep(1)
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(backward_control, outfile)
    time.sleep(post_command_delay)

def strong_right():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(right_control, outfile)
    time.sleep(post_command_delay)

def slight_right():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(slight_right_control, outfile)
    time.sleep(post_command_delay)

def strong_left():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(left_control, outfile)
    time.sleep(post_command_delay)

def slight_left():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(slight_left_control, outfile)
    time.sleep(post_command_delay)

def stop():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(stop_control, outfile)
    time.sleep(post_command_delay)


while(True):
        forward()

    
