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

def start_recording():
    global video_writer, recording_start_time, recording_stopped, update_camera
    if not video_writer:
        #generates timestamped unique filename
        timestamp = time.strftime("%Y%m%d%H%M%S")
        video_path = os.path.join("gallery", f"recorded_video_{timestamp}.mp4")