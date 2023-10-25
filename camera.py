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
            
    camera_feed.after(10, update_camera_feed)
    

#this function is now to display the images that are recorded. Breakdown: this function opens an image and displays it in the feed
#do this by using PIL to open the image, converts it to a format that tkinter can use 
#finally, updating the camera widget with the newly converted image.

def show_image(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image=image)
    camera_feed.config(image=photo)
    camera_feed.image = photo
    
#this function opens a window for the video player where the user can view recordings. This also pauses the camera feed updates while video is in use

def play_video(video_path):
    def close_video_player():
        video_player.destroy()
        global update_camera
        update_camera = True
        
    global update_camera
    update_camera = False
    
    video_player = tk.Toplevel(root)
    video_player.title("Video Player")
    
    video_cap = cv2.VideoCapture(video_path)
    
    def update_video_frame():
        ret, frame = video_cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=img)
            video_label.config(image=photo)
            video_label.image = photo
            video_player.after(10, update_video_frame)
            
            frame_rate = video_cap.get(cv2.CAP_PROP_FPS)
            
            delay = int(1000 / frame_rate)
            
            video_player.after(delay, update_video_frame)
        else:
            video_player.destroy()
    
    video_label = tk.Label(video_player)
    
    video_label.pack()
    
    update_video_frame()
    
    video_player.protocol("WM_DELETE_WINDOW", close_video_player)
def create_video_thumbnail(video_path):
    video_cap = cv2.VideoCapture(video_path)
    ret, frame = video_cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        thumbnail = Image.fromarray(frame).resize((100, 100))
        thumbnail_photo = ImageTk.PhotoImage(image=thumbnail)
        # Return both the thumbnail and filename
        return thumbnail_photo, os.path.basename(video_path)
    return None, None

def play_video_from_thumbnail(video_path):
    play_video(video_path)

def open_gallery():
    global update_camera
    update_camera = False  # Pause camera feed updates
    gallery_window = tk.Toplevel(root)
    gallery_window.title("Gallery")
    
    def back_to_camera():
        gallery_window.destroy()
        global update_camera
        update_camera = True  # Resume updating the camera feed
    
    back_button = tk.Button(gallery_window, text="Back to Camera",
                            command=back_to_camera)
    back_button.pack()
    gallery_dir = "gallery"
    image_files = [f for f in os.listdir(gallery_dir) if f.endswith(".jpg")]
    video_files = [f for f in os.listdir(gallery_dir) if f.endswith(".mp4")]
    # Clear the existing image_thumbnails and video_thumbnails lists
   
    del image_thumbnails[:]
    del video_thumbnails[:]
    for image_file in image_files:
        image_path = os.path.join(gallery_dir, image_file)
        thumbnail = Image.open(image_path).resize((100, 100))
        thumbnail_photo = ImageTk.PhotoImage(image=thumbnail)
        image_name = os.path.basename(image_file)
        def show_image_in_gallery(img_path, img_name):
            image_window = tk.Toplevel(gallery_window)
            image_window.title("Image")
            img = Image.open(img_path)
            img_photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(image_window, image=img_photo)
            img_label.image = img_photo
            img_label.pack()
            img_label_name = tk.Label(image_window, text=img_name)
            img_label_name.pack()
        thumbnail_label = tk.Label(gallery_window, image=thumbnail_photo)
        thumbnail_label.image = thumbnail_photo
        thumbnail_label.bind("<Button-1>", lambda event,
                                                  img_path=image_path,
                                                  img_name=image_name:
        show_image_in_gallery(img_path, img_name))
        thumbnail_label.pack()
        image_thumbnails.append(thumbnail_photo)  # Store the PhotoImage objects
        # Display the image filename below the thumbnail
        image_name_label = tk.Label(gallery_window, text=image_name)
        image_name_label.pack()
    for video_file in video_files:
        video_path = os.path.join(gallery_dir, video_file)
        # Create a video thumbnail and get the filename
        thumbnail_photo, video_name = create_video_thumbnail(video_path)
        if thumbnail_photo:
            # Create a button with the video thumbnail
            video_thumbnail_button = tk.Button(
                gallery_window,
                image=thumbnail_photo,
                command=lambda path=video_path: play_video_from_thumbnail(path)
            )
            video_thumbnail_button.pack()
            # Store the video thumbnail PhotoImage objects
            video_thumbnails.append(thumbnail_photo)
            # Display the video filename below the thumbnail
            video_name_label = tk.Label(gallery_window, text=video_name)
            video_name_label.pack()

# Create the main root window
root = tk.Tk()
root.title("Practice Camera App")

# Initialize variables
video_writer = None
recording_start_time = 0  # Initialize recording start time
recording_stopped = False  # Initialize recording_stopped flag

# App buttons
capture_button = tk.Button(root, text="Snap", command=capture_image)
record_button = tk.Button(root, text="Record", command=start_recording)
stop_button = tk.Button(root, text="Stop", command=stop_recording)
stop_button = tk.Button(root, text="Halt Recording", command=stop_recording)
gallery_button = tk.Button(root, text="The Spread", command=open_gallery)
quit_button = tk.Button(root, text="Quit", command=root.quit)


# Grid layout for buttons
capture_button.grid(row=0, column=0, padx=10, pady=10)
record_button.grid(row=0, column=1, padx=10, pady=10)
stop_button.grid(row=0, column=2, padx=10, pady=10)
gallery_button.grid(row=0, column=3, padx=10, pady=10)
quit_button.grid(row=0, column=4, padx=10, pady=10)

# Create camera feed label
camera_feed = tk.Label(root)
camera_feed.grid(row=1, column=0, columnspan=5)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Function to update the camera feed
def update_camera_feed():
    if update_camera:
        if not video_writer:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=img)
                camera_feed.config(image=photo)
                camera_feed.image = photo
    root.after(10, update_camera_feed)
update_camera_feed()

# Start the tkinter main loop
root.mainloop()
    

        
        
        
        