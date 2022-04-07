import socket
import struct
import time
import numpy as np
import json 
from threading import Thread

import cv2

#from src.templates.workerprocess import WorkerProcess
#
#class LaneCentering(WorkerProcess):
#    # ===================================== INIT =========================================
#    def __init__(self, inPs, outPs):
#        """Process used for sending images over the network to a targeted IP via UDP protocol 
#        (no feedback required). The image is compressed before sending it. 
#
#        Used for visualizing your raspicam images on remote PC.
#        
#        Parameters
#        ----------
#        inPs : list(Pipe) 
#            List of input pipes, only the first pipe is used to transfer the captured frames. 
#        outPs : list(Pipe) 
#            List of output pipes (not used at the moment)
#        """
#        super(CameraStreamerProcess,self).__init__( inPs, outPs)
#
#
#json commands 
forward_control = {"action": "1", "speed": 0.18}
backward_control = {"action": "1", "speed": -0.18}
stop_control = {"action": "1", "speed": 0.00}
left_control = {"action": "2", "steerAngle": -20.5}
right_control = {"action": "2", "steerAngle": 20.5}
slight_left_control = {"action": "2", "steerAngle": -10.5}
slight_right_control = {"action": "2", "steerAngle": 10.5}
straight_control = {"action": "2", "steerAngle": 0.00}


##json command to function 
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

def straight():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(straight_control, outfile)
    time.sleep(post_command_delay)

def stop():
    with open('/home/pi/Scarlet/src/utils/remotecontrol/commands.json', 'w') as outfile:
        json.dump(stop_control, outfile)
    time.sleep(post_command_delay)




#lane centering 

def make_points(image, line):
    slope, intercept = line
    #print(slope)
    y1 = int(image.shape[0])# bottom of the image
    y2 = int(y1*4/5)         # slightly lower than the middle
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    #if x1 or x2>640:
     #   return None
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit    = []
    right_fit   = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1,x2), (y1,y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0: # y is reversed in image
                left_fit.append((slope, intercept))
            if slope>0.3:
                right_fit.append((slope, intercept))
    # add more weight to longer lines
    if len(left_fit)==0:
        print('No left lane detected')
        left_line=[[0,480, 0,380]]
    else:
        left_fit_average  = np.average(left_fit, axis=0)
        left_line  = make_points(image, left_fit_average)
        
    if len(right_fit)==0:
        print('No right lane detected')
        right_line=[[640,480, 640,380]]
    else:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_points(image, right_fit_average)
    
    averaged_lines = [left_line, right_line]
    return averaged_lines

def display_lines(img,lines):
    line_image = np.zeros_like(img)
    if lines is not None:
        p=lines[0][0][2]
        q=lines[1][0][2]
        #print(p,q)
        mean=int((p+q)/2)
        for line in lines:
            for x1, y1, x2, y2 in line:
                #print(line)
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image, mean
    
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray,(kernel, kernel),0)
    canny = cv2.Canny(gray, 100, 200)
    return canny

def region_of_interest(canny):
    height = canny.shape[0]
    width = canny.shape[1]
    mask = np.zeros_like(canny)

    triangle = np.array([[
    (0, height),
    (300, 250),
    (width, height),]], np.int32)

    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image


cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    _, frame = cap.read()
    frame=cv2.resize(frame, (640,480))
    canny_image = canny(frame)
    cropped_canny = region_of_interest(canny_image)
    
    lines = cv2.HoughLinesP(cropped_canny, 1, np.pi/180, 50, np.array([]), minLineLength=10, maxLineGap=50)
    #print(lines)
    if lines is None:
      print('No line detected')
      cv2.imshow("canny", cropped_canny)
    else:
      averaged_lines = average_slope_intercept(frame, lines)
      line_image,mean = display_lines(frame, averaged_lines)
      combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
      #print(combo_image.shape)
      cv2.line(combo_image,(mean,int(combo_image.shape[0]*4/5)), (mean, int(combo_image.shape[0]*4/5)-10), (0,0,255),2)
      
      cv2.line(combo_image,(320,235),(320,245), (0,0,255),2)
      pos=mean-320
      print(pos)
      forward()
 
      if pos < -15 & pos > -25:
          slight_left()
      elif pos > 15 & pos < 25:
          slight_right()
      elif pos < -25:
          strong_left()
      elif pos > 25:
          string_right()
      else:
          straight()

      
      combo_image=cv2.resize(combo_image,(700,500))
      cv2.imshow("final", combo_image)
      #cv2.imshow("line", line_image)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

    
