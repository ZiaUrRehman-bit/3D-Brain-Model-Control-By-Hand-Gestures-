import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
import Track_Hand as ht
import Classification as Classifier
import numpy as np
import math
import time
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import pyautogui

Segmentor = SelfiSegmentation()

hands = ht.handTracker(maximumHands=1,
                       detConfidence=0.8,
                       trackConfidence=0.8)

# declare the classifier with model and lable
classifier = Classifier.Classifier("keras_model.h5", "labels.txt")

offset = 20
imageSize = 300

labels = ["moveRight", "moveLeft", "moveUp", "moveDown", "zoomIN", "zoomOut",
          "rotateCW", "rotateACW", "Select"]

# Defining CreateWidgets() function to create necessary tkinter widgets
def createwidgets():

    root.title("3D Brain Model Control By Hand Gestures")

    myMenue = Menu(root)
    root.config(menu = myMenue)
    file_menu = Menu(myMenue)
    myMenue.add_cascade(label= "Menu", menu = file_menu)
    file_menu.add_command(label = "Help", command = open_help)
    file_menu.add_command(label  ="3D Model", command = model)


    root.feedlabel = Label(root, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Comic Sans MS',20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    # root.saveLocationEntry = Entry(root, width=55, textvariable=destPath)
    # root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)
    #
    # root.browseButton = Button(root, width=10, text="BROWSE", command=destBrowse)
    # root.browseButton.grid(row=3, column=2, padx=10, pady=10)

    # root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="LIGHTBLUE", font=('Comic Sans MS',15), width=20)
    # root.captureBTN.grid(row=4, column=1, padx=10, pady=10)

    root.CAMBTN = Button(root, text="STOP CAMERA", command=StopCAM, bg="LIGHTBLUE", font=('Comic Sans MS',15), width=13)
    root.CAMBTN.grid(row=4, column=2)

    # root.previewlabel = Label(root, bg="steelblue", fg="white", text="IMAGE PREVIEW", font=('Comic Sans MS',20))
    # root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)
    #
    # root.imageLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    # root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)
    #
    # root.openImageEntry = Entry(root, width=55, textvariable=imagePath)
    # root.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

    # root.openImageButton = Button(root, width=10, text="BROWSE", command=imageBrowse)
    # root.openImageButton.grid(row=3, column=5, padx=10, pady=10)

    # Calling ShowFeed() function
    ShowFeed()

# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()
    finalFrame = frame.copy()
    try:
        if ret:
            # Flipping the frame vertically
            # frame = cv2.flip(frame, 1)

            # Displaying date and time on the feed
            cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

            frame = hands.findAndDrawHands(finalFrame)

            # find landmarks and bounding box
            lm, bbox = hands.findLandmarks(frame)

            if lm:
                x, y, w, h = bbox

                # creating our own image for same size
                imgWhite = np.ones((300, 300, 3), np.uint8) * 255
                print(imgWhite.shape)

                # staring hight ending hight, starting width and ending width
                # imgCrop = frame[y:y + h, x:x + w]
                imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]

                imgCrop = Segmentor.removeBG(imgCrop, (255, 255, 255))

                # imgCrop = cv2.Canny(imgCrop, 170, 200)  # by changing the threshold valuse we can reduce or enhnce the edges
                # dialation (increase the thickness of edges) for that we need kernal
                # imgCrop = cv2.dilate(imgCanny, kernel, iterations=1)

                imgCropShape = imgCrop.shape
                # add cropped image in to white image
                # imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop

                # so in order to fit our croped image on the white image we have to do
                # some calculations

                aspectRatio = h / w  # if value is above one its mean hight is greater

                if aspectRatio > 1:  # fix the hight
                    k = imageSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imageSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imageSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(labels[index])
                else:  # fix the width
                    k = imageSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgWhite, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imageSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(labels[index])

                cv2.rectangle(finalFrame, (x - 20, y - 20), (x + w + 20, y + h + 20),
                              (255, 0, 255), 1)
                cv2.line(finalFrame, (x - 20, y - 20), (x - 20, y - 20 + 20), (255, 0, 255), 3)
                cv2.line(finalFrame, (x - 20, y - 20), (x - 20 + 20, y - 20), (255, 0, 255), 3)

                cv2.putText(finalFrame, labels[index], (x, y - 26),
                            cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)


            # Changing the frame color from BGR to RGB
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Creating an image memory from the above frame exporting array interface
            videoImg = Image.fromarray(cv2image)

            # Creating object of PhotoImage() class to display the frame
            imgtk = ImageTk.PhotoImage(image = videoImg)

            # Configuring the label to display the frame
            root.cameraLabel.configure(image=imgtk)

            # Keeping a reference
            root.cameraLabel.imgtk = imgtk

            # Calling the function after 10 milliseconds
            root.cameraLabel.after(10, ShowFeed)
        else:
            # Configuring the label to display the frame
            root.cameraLabel.configure(image='')
    except:
        pass

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

# def destBrowse():
#     # Presenting user with a pop-up for directory selection. initialdir argument is optional
#     # Retrieving the user-input destination directory and storing it in destinationDirectory
#     # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
#     destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
#
#     # Displaying the directory in the directory textbox
#     destPath.set(destDirectory)

# def imageBrowse():
#     # Presenting user with a pop-up for directory selection. initialdir argument is optional
#     # Retrieving the user-input destination directory and storing it in destinationDirectory
#     # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
#     openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
#
#     # Displaying the directory in the directory textbox
#     imagePath.set(openDirectory)
#
#     # Opening the saved image using the open() of Image class which takes the saved image as the argument
#     imageView = Image.open(openDirectory)
#
#     # Resizing the image using Image.resize()
#     imageResize = imageView.resize((640, 480), Image.ANTIALIAS)
#
#     # Creating object of PhotoImage() class to display the frame
#     imageDisplay = ImageTk.PhotoImage(imageResize)
#
#     # Configuring the label to display the frame
#     root.imageLabel.config(image=imageDisplay)
#
#     # Keeping a reference
#     root.imageLabel.photo = imageDisplay
#
# # Defining Capture() to capture and save the image and display the image in the imageLabel
# def Capture():
#     # Storing the date in the mentioned format in the image_name variable
#     image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
#
#     # If the user has selected the destination directory, then get the directory and save it in image_path
#     if destPath.get() != '':
#         image_path = destPath.get()
#     # If the user has not selected any destination directory, then set the image_path to default directory
#     else:
#         messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")
#
#     # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
#     imgName = image_path + '/' + image_name + ".jpg"
#
#     # Capturing the frame
#     ret, frame = root.cap.read()
#
#     # Displaying date and time on the frame
#     cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
#
#     # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
#     success = cv2.imwrite(imgName, frame)
#
#     # Opening the saved image using the open() of Image class which takes the saved image as the argument
#     saved_image = Image.open(imgName)
#
#     # Creating object of PhotoImage() class to display the frame
#     saved_image = ImageTk.PhotoImage(saved_image)
#
#     # Configuring the label to display the frame
#     root.imageLabel.config(image=saved_image)
#
#     # Keeping a reference
#     root.imageLabel.photo = saved_image
#
#     # Displaying messagebox
#     if success :
#         messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)


# Defining StopCAM() to stop WEBCAM Preview
def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="START CAMERA", command=StartCAM)

    # Displaying text message in the camera label
    root.cameraLabel.config(text="OFF CAM", font=('Comic Sans MS',70))

def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Setting width and height
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)

    # Removing text message from the camera label
    root.cameraLabel.config(text="")

    # Calling the ShowFeed() Function
    ShowFeed()

# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index
root.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Setting width and height
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Setting the title, window size, background color and disabling the resizing property
root.title("Pycam")
root.geometry("700x700")
root.resizable(True, True)
root.configure(background = "sky blue")

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

createwidgets()
root.mainloop()