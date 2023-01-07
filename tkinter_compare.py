import time
import face_recognition
import cv2
import numpy as np
import csv
import os
import glob
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

# Set the directory where the images are stored
directory = 'photos/'

video_capture = cv2.VideoCapture(0)

known_face_encoding = []
known_face_names = []

root = Tk()
root.title("attendence system")
root.geometry("700x640")
root.configure (bg="black")

f1=LabelFrame (root, bg="red")
f1.pack()
L1= Label(f1, bg="red")
L1.pack()

#insert name
lastAttend= Label(root,text="Last attended student", font =20)
lastAttend.pack()

#if data is not aavailable
availableCSV= Label(root,text="No one ", font =20)
availableCSV.pack()

cap=cv2.VideoCapture(0)


# Iterate over the files in the directory
for filename in os.listdir(directory):
  # Check if the file is an image
  if filename.endswith(".jpg") or filename.endswith(".png"):
    # Load the image
    img = Image.open(os.path.join(directory, filename))
    print(filename)

    tempImg = face_recognition.load_image_file(os.path.join(directory, filename))
    IMG_encoded = face_recognition.face_encodings(tempImg)[0]
    # Add the image to the images array
    known_face_encoding.append(IMG_encoded)
    # Get the name of the image (without the extension)
    name = os.path.splitext(filename)[0]
    # Add the name to the names array
    known_face_names.append(name)



students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
s=True


now = datetime.now()
current_date = now.strftime("%Y-%m-%d")


f= open(current_date+'.csv','w+',newline='')
lnwriter = csv.writer(f)


# Create a treeview with one column for each field in the CSV file
treeview = ttk.Treeview(root, columns=list(range(2)))
 # Configure the treeview
treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    img1= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame=ImageTk.PhotoImage (Image.fromarray(img1))
    L1['image'] = frame
    root.update()


    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name =""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            face_names.append(name)
            if name in known_face_names:
                if name in students:
                    # Check if the treeview has data and clear it if it does
                    if treeview.get_children():
                        for item in treeview.get_children():
                            treeview.delete(item)


                    temp = "last came : "+name
                    lastAttend.config(text=temp)
                    students.remove(name)
                    print(students)
                    timeInfo = datetime.now()
                    current_time = timeInfo.strftime("%A, %B %d, %Y %I:%M %p")
                    lnwriter.writerow([name,current_time])
                    f.flush()
                    time.sleep(1)
                    
                    # Try to open the file
                    try:
                        with open(current_date+'.csv', 'r') as file:
                            availableCSV.config(text="")
                            reader = csv.reader(file)
                            data = list(reader)
    
                       

                        # Insert the data into the treeview
                        for i, row in enumerate(data):
                            treeview.insert('', 'end', values=row)
                       
                    except FileNotFoundError:
                        availableCSV.config(text="file not found")

        
        

video_capture.release()


