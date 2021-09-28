import pymsgbox
import cv2
import numpy as np
import os
import pyautogui
import pyperclip
from collections import deque


def scroller():
	cap = cv2.VideoCapture(0)

	yellow_lower = np.array([22, 93, 0])
	yellow_upper = np.array([45, 255, 255])
	prev_x = 0
	prev_y = 0

	while True:
	    ret, frame = cap.read()
	    ret, frame2 = cap.read()
	    diff = cv2.absdiff(frame, frame2)
	    if(diff.any()):
		    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
		    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		    for c in contours:
		        area = cv2.contourArea(c)
		        if area > 100:
		            x, y, w, h = cv2.boundingRect(c)
		            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		            if y < prev_y:
		                pyautogui.press('space')

		            prev_y = x
	    cv2.imshow('frame', frame)
	    if cv2.waitKey(10) == ord('q'):
	        break

	cap.release()
	cv2.destroyAllWindows()








def aircanvas():
	def empty(a):
	    print("")

	bpoints = [deque(maxlen=1024)]
	gpoints = [deque(maxlen=1024)]
	rpoints = [deque(maxlen=1024)]
	blpoints = [deque(maxlen=1024)]


	blue_index = 0
	green_index = 0 
	red_index = 0
	black_index = 0

	kernel = np.ones((5,5),np.uint8)

	frame_height = 640
	frame_width = 480
	cap =cv2.VideoCapture(0)
	cap.set(3,frame_width)
	cap.set(4,frame_height)
	cap.set(10,150)
 
	colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
	colorIndex = 0


	#Making Trackbar window and trackbars

	cv2.namedWindow("Trackbars")
	cv2.resizeWindow("Trackbars", 560,320)
	cv2.createTrackbar("Hue Min","Trackbars",0,131,empty)
	cv2.createTrackbar("Hue Max","Trackbars",131,131,empty)
	cv2.createTrackbar("Sat Min","Trackbars",150,255,empty)
	cv2.createTrackbar("Sat Max","Trackbars",255,255,empty)
	cv2.createTrackbar("Val Min","Trackbars",102,255,empty)
	cv2.createTrackbar("Val Max","Trackbars",255,255,empty)


	#Creating Paint Window

	paintWin = np.zeros([480,640,3]) + 255
	paintWin = cv2.rectangle(paintWin, (30,1), (120,65), (0,0,0) , 0 )
	paintWin = cv2.rectangle(paintWin, (160,1) , (255,65) , colors[0], -1)
	paintWin = cv2.rectangle(paintWin, (280,1) , (370,65) , colors[1], -1)
	paintWin = cv2.rectangle(paintWin, (400,1) , (485,65) , colors[2], -1)
	paintWin = cv2.rectangle(paintWin, (520,1) , (600,65) , colors[3], -1)

	cv2.putText(paintWin, "CLEAR",(58,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(paintWin, "BLUE",(187,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	cv2.putText(paintWin, "GREEN",(295,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	cv2.putText(paintWin, "RED",(415,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	cv2.putText(paintWin, "BLACK",(530,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


	# Main Video Capturing 

	while True:
	    success,img = cap.read()
	    img = cv2.flip(img,1)
	    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	    # Getting Trackbar Positions for creating a mask

	    h_min = cv2.getTrackbarPos("Hue Min","Trackbars")
	    s_min = cv2.getTrackbarPos("Sat Min","Trackbars")
	    v_min = cv2.getTrackbarPos("Val Min","Trackbars")
	    h_max = cv2.getTrackbarPos("Hue Max","Trackbars")
	    s_max = cv2.getTrackbarPos("Sat Max","Trackbars")
	    v_max = cv2.getTrackbarPos("Val Max","Trackbars")

	    lower = np.array([h_min,s_min,v_min])
	    upper = np.array([h_max,s_max,v_max])


	    # Shows color Options in Video Outputed by Webcam 

	    img = cv2.rectangle(img, (30,1), (120,65), (122,122,122) , -1 )
	    img = cv2.rectangle(img, (160,1) , (255,65) , colors[0], -1)
	    img = cv2.rectangle(img, (280,1) , (370,65) , colors[1], -1)
	    img = cv2.rectangle(img, (400,1) , (485,65) , colors[2], -1)
	    img = cv2.rectangle(img, (520,1) , (600,65) , colors[3], -1)

	    cv2.putText(img, "CLEAR ALL",(58,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0, 0, 0), 1, cv2.LINE_AA)
	    cv2.putText(img, "BLUE",(187,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	    cv2.putText(img, "GREEN",(295,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	    cv2.putText(img, "RED",(415,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
	    cv2.putText(img, "BLACK",(530,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


	    # Making A mask and dilating and eroding to remove impurities.  

	    mask = cv2.inRange(imgHSV,lower,upper)
	    mask = cv2.erode(mask,kernel,iterations=1)
	    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	    mask = cv2.dilate(mask,kernel,iterations=1)


	    cnt,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	    center = None

	    if len(cnt) > 0:
	        # Sorting the contours on basis of their length
	        cnt = sorted(cnt,key = cv2.contourArea, reverse=True)[0]
	        # Finding the minimum area of contour
	        ((x,y),radius) = cv2.minEnclosingCircle(cnt)
	        # Drawing the circle around the contour
	        cv2.circle(img, (int(x),int(y)), int(radius), (0,255,255), 2)

	        # Finding the area and centroid of the contour
	        M = cv2.moments(cnt)
	        center = (int(M['m10'] / M['m00']) , int(M['m01'] / M['m00']))


	        # Drawing line on the screen
	        if center[1] <= 65:
	            if 30 <= center[0] <= 120: #Clear Button

	                bpoints = [deque(maxlen=512)]
	                gpoints = [deque(maxlen=512)]
	                rpoints = [deque(maxlen=512)]
	                blpoints = [deque(maxlen=512)]

	                blue_index = 0
	                green_index = 0 
	                red_index = 0
	                black_index = 0

	                paintWin[67:,:,:] = 255
	            elif 160 <= center[0] <= 255:
	                    colorIndex = 0 # Blue
	            elif 280 <= center[0] <= 370:
	                    colorIndex = 1 # Green
	            elif 400 <= center[0] <= 485:
	                    colorIndex = 2 # Red
	            elif 520 <= center[0] <= 600:
	                    colorIndex = 3 # 
	        else :
	            if colorIndex == 0:
	                bpoints[blue_index].appendleft(center)
	            elif colorIndex == 1:
	                gpoints[green_index].appendleft(center)
	            elif colorIndex == 2:
	                rpoints[red_index].appendleft(center)   
	            elif colorIndex == 3:
	                blpoints[black_index].appendleft(center)

	    else:
	        bpoints.append(deque(maxlen=512))
	        blue_index += 1
	        gpoints.append(deque(maxlen=512))
	        green_index += 1
	        rpoints.append(deque(maxlen=512))
	        red_index += 1
	        blpoints.append(deque(maxlen=512))
	        black_index += 1

	        # Draw lines of all the colors on the canvas and frame 
	    points = [bpoints, gpoints, rpoints, blpoints]
	    for i in range(len(points)):
	        for j in range(len(points[i])):
	            for k in range(1, len(points[i][j])):
	                if points[i][j][k - 1] is None or points[i][j][k] is None:
	                    continue
	                cv2.line(img, points[i][j][k - 1], points[i][j][k], colors[i], 2)
	                cv2.line(paintWin, points[i][j][k - 1], points[i][j][k], colors[i], 2)

	    cv2.imshow("Air Canvas",img)
	    cv2.imshow("Mask",mask)
	    cv2.imshow("Paint", paintWin)
	    if cv2.waitKey(50) & 0xFF == ord('q'):
	        break

	cap.release()
	cv2.destroyAllWindows()	








def sharing():
	cap = cv2.VideoCapture(0)

	yellow_lower = np.array([22, 93, 0])
	yellow_upper = np.array([45, 255, 255])
	prev_x = 0
	prev_y = 0

	while True:
	    ret, frame = cap.read()
	    ret, frame2 = cap.read()
	    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
	    
	    diff = cv2.absdiff(frame, frame2)
	    if(diff.any()):
		    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
		    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		    for c in contours:
		        area = cv2.contourArea(c)
		        if area > 100:
		            x, y, w, h = cv2.boundingRect(c)
		            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		            
		            
		            
		            if y < prev_y:
		            	# date = pyautogui.press('ctrl','c')
		            	pyautogui.hotkey('ctrl', 'c')
		            	date = pyperclip.paste()
		            	date=date[7:]
		            	cmd = "scp -r navaneeswarreddy@192.168.225.34:{0} /home/navaneeswarreddy/Music/".format(date)
		            	img = cv2.rectangle(frame, (52,1) , (600,65) , colors[1] , -1)
		            	cv2.putText(img, cmd ,(57,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
		            	os.system(cmd)
		            	
		            	    

		            prev_y = x
	    cv2.imshow('frame', frame)
	    if cv2.waitKey(10) == ord('q'):
	        break

	cap.release()
	cv2.destroyAllWindows()




def index():
	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		img = cv2.rectangle(frame, (10,6) , (630,55) , (224,78,98) , -1)
		img = cv2.rectangle(frame, (42,65) , (590,130) , (247,160,140) , -1)
		img = cv2.rectangle(frame, (42,135) , (590,200) , (247,160,140) , -1)
		img = cv2.rectangle(frame, (42,205) , (590,270) , (247,160,140) , -1)
		cv2.putText(img, "VISION ASSISSTANT"  ,(175,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2 , cv2.LINE_AA)
		cv2.putText(img, "1. SCROLLER"  ,(75,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		cv2.putText(img, "2. FILE SHARING"  ,(75,175), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		cv2.putText(img, "3. AIR CANVAS"  ,(75,245), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1 )
		cv2.putText(img, " Chose the Option ? Then, Click Q to enter "  ,(60,300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
		cv2.putText(img, " Want to Exit ? Then, Click E to exit "  ,(95,350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0 , 255), 2 )
		

		if cv2.waitKey(10) == ord('q'):
			response = pymsgbox.prompt('Enter  your Option ')
			cap.release()
			cv2.destroyAllWindows()

			if (response == "1"):
				scroller()
				index()
			elif (response == "2"):
				sharing()
				index()
			elif (response == "3"):
				aircanvas()
				index()
			else:
				pymsgbox.alert('Chose the correct Option', 'Title')
				index()
		elif cv2.waitKey(10) == ord('e'):
			break


		cv2.imshow('frame', frame)





index()
