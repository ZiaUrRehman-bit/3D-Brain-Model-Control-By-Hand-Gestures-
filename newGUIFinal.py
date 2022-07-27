import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog


# Defining CreateWidgets() function to create necessary tkinter widgets
def createwidgets():

    root.title("3D Brain Model Control By Hand Gestures")

    root.feedlabel = Label(root, bg="steelblue", fg="white", text="3D Model Control", font=('Comic Sans MS',20))
    root.feedlabel.grid(row=1, column=2, padx=150, pady=20, columnspan=2)

    root.CAMBTN = Button(root, text="3D Model", command=model, bg="LIGHTBLUE", font=('Comic Sans MS',15), width=10)
    root.CAMBTN.grid(row=2, column=2, padx=20, pady=20, columnspan=2)

    root.helpBTN = Button(root, text="HELP", command=open_help, bg="LIGHTBLUE", font=('Comic Sans MS', 15),
                         width=10)
    root.helpBTN.grid(row=3, column=2, padx=20, pady=20, columnspan=2)

def open_help():

    img = cv2.imread("Final-Dataset.jpg")
    img = cv2.resize(img, (600, 600))
    cv2.imshow("Help", img)
    cv2.waitKey(0)

def model():

    img = cv2.imread("sss.png")
    img = cv2.resize(img, (600, 600))
    cv2.imshow("3D Model", img)
    cv2.waitKey(0)

# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index


# Setting the title, window size, background color and disabling the resizing property
root.title("Pycam")
root.geometry("500x400")
root.resizable(True, True)
root.configure(background = "sky blue")

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

createwidgets()
root.mainloop()