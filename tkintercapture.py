import cv2
import os
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import datetime


# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
directory = "photos/"
studentName = ""
def captureImg():
        image=Image.fromarray(img1)
        studentName = E1.get()+".jpg"
        image.save(os.path.join(directory, studentName))
        

def goBack():
        print('exit command')

root = Tk()
root.title("attendence systemm -student add ")
root.geometry("700x640")
root.configure (bg="black")



f1=LabelFrame (root, bg="red")
f1.pack()
L1= Label(f1, bg="red")
L1.pack()


#insert name
Label(root,text="enter Name", font =20).pack()


E1=Entry(root,font=("Arial Black",12))
E1.pack()

cap=cv2.VideoCapture(0)
b1 = Button(root, text="Take Snapshot", font=("times new roman", 20, "bold"), bg="black", fg="red", command=captureImg)
b1.pack()


while True:
    _,img=cap.read()
    img1= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=ImageTk.PhotoImage (Image.fromarray(img1))
    L1['image'] = img
    root.update()

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(img1, 1.1, 4)
    if len(faces) > 0:
        b1["state"] = "normal"
        b1["text"] = "Face detected,Insert name"
        if E1.get() =="":
            b1["state"] = "disabled"
            b1["text"] = "Write student name"
        else:
            b1["state"] = "normal"
            b1["text"] = "Take snapshot"
    else:
        b1["state"] = "disabled"
        b1["text"] = "No face detected"



    
    

cap.release()