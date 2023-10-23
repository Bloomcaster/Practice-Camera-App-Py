#tkinter a py library for GUI
#cv2 a library of py bindings used to solve computer vision problems
#PIL imaging library in py, extensive file format support
#os is operating system
#threading allows different parts of the program to run concurrently and simplify design
#time is used for dates litereally

import tkinter  as tk
import cv2
from PIL import Image, ImageTk
import os
import threading
import time

#creating a directory for captured images/recordings. This step ensures the directory exists BEFORE capturing or recording videos

if not os.path.exists("gallery"):
    os.makedirs("gallery")
    
#defining thumbnail images and video variables, this stores the images in the gallery
#update camera will control camera feed updates

image_thumbnails = []
video_thubmnails = []
update_camera = True

#function that will OpenCV to capture image from feed. It should retrieve a frame, save it in gallery and display it using show_image
#ret means resolution enhancement technology, a form of image processing used to manipulate dot characteristics,
#in python this is a boolean regarding if there is a return true if the FRAME is available
def capture_image():
    ret, frame = cap.read()

#following code generates a unique filename with timestamp
    
    if ret:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        image_path = os.path.join("gallery", f"captured_image_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        show_image(image_path)
        
#starting and stopping recording. Before we display we need to create.
#to do this create a function that initiates the video process 
#function should also disable the RECORD button (to prevent multiple recording at the same time)
#and enable the STOP RECORDING button
#mp4 is a popular video format used to share, download and stream content
#it is a container format, which means it can store various types of audio and video as long as it is encoded in a codec mp4 format

def start_recording():
    global video_writer, recording_start_time, recording_stopped, update_camera
    
    if not video_writer:
        #generates timestamped unique filename
        timestamp = time.strftime("%Y%m%d%H%M%S")
        video_path = os.path.join("gallery", f"recorded_video_{timestamp}.mp4")
        
        fourcc = cv2.VideoWriter(video_path, fourcc, 20.0,
                                 (640, 480))
        
        recording_start_time = time.time()
        recording_stopped = False
        record_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        #to start a separate thread for recording material and time-lapse
        
        recording_thread = threading.Thread(target=record_and_display)
        recording_thread.start()
        
#Now to creat a function that stope the recording and releases the video writer
#With this function the UI is updated enabling the Record button and disabling the Stop Record button.

def stop_recording():
    global video_writer, recording_stopped
    
    if video_writer:
        video_writer.release()
        recording_stopped = True
        record_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        
#Here is a function that will continually capture frames from the camera, process and then display on GUI camera feed
#It should always do this unless the Stop Recording button is pressed
#elasped time is also calulated when recording starts and displayed on the video frame

def record_and_display():
    global recording_stopped, update_camera
    
    while video_writer and not recording_stopped:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            #calculating elasped time and adding it to the frame
            elapsed_time = time.time() - recording_start_time
            timestamp = f"Time Elapsed: {int(elapsed_time)}s"
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            camera_feed.config(image=photo)
            camera_feed.image = photo
            
            video_writer.write(frame)
            time.sleep(0.05)
            
    camer_feed.after(10, update_camera_feed)
        
        
        
        