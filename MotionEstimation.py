from tkinter import *
import tkinter
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askopenfilename
import cv2
import sys
import os
from sys import platform

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '\\python\\openpose\\Release');
os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '\\x64\\Release;' +  dir_path + '\\bin;'+dir_path + '\\python\\openpose\\Release;.;'
import pyopenpose as op

params = dict()
params["model_folder"] = dir_path+"/models/"


main = tkinter.Tk()
main.title("Human Motion Estimation and Prediction") #designing main screen
main.geometry("800x500")

global filename
global loaded_model

def upload(): #function to upload tweeter profile
    global filename
    filename = filedialog.askopenfilename(initialdir="testimages")
    img = cv2.imread(filename)
    cv2.imshow("Uploaded Image",img)
    cv2.waitKey(0)

def estimatePose():
    opWrapper = op.WrapperPython()# It creates an instance of the WrapperPython class from the OpenPose library. This class is used to provide a Python interface for the OpenPose library and allows you to configure and run the OpenPose pose estimation pipeline using Python code.
    opWrapper.configure(params)#By calling opWrapper.configure(params), we are setting up the OpenPose algorithm with the specified configuration settings, so that it can be used to process input data and generate output data.
    opWrapper.start()# After configuring the OpenPose wrapper object with the desired parameters, the opWrapper.start() method is called to start the OpenPose framework. This method initializes all the necessary components required for the processing of input frames.
    datum = op.Datum()#After the OpenPose framework is started, the next step is to capture the video frames and feed them to the OpenPose framework for processing. This is done using the op.Datum() class which creates a new Datum object to store the output data from OpenPose. The Datum object is then passed to the OpenPose framework for processing each frame.
    imageToProcess = cv2.imread(filename)#The above code reads an image from a file using OpenCV's imread() function and stores it in the variable imageToProcess
    datum.cvInputData = imageToProcess# It then sets cvInputData attribute of datum (an instance of the Datum class) to imageToProcess, which is the input image for OpenPose.
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))#it pushes datum onto OpenPose's processing queue using emplaceAndPop() function, which processes the input image and updates the attributes of datum with the results
    height, width = imageToProcess.shape[:2]#including detected keypoint coordinates for body pose estimation, stored in poseKeypoints.
    img = np.zeros((height, width, 3), dtype = 'uint8')#The code then creates an output image img with the same dimensions as imageToProcess and initializes all pixels to black.
    persons = datum.poseKeypoints    #it assigns the detected poseKeypoints to persons variable for further processing or display.
    for k in range(0, persons.shape[0]):#This code iterates through each person detected in the image by the OpenPose model. The variable "persons" contains all the detected pose keypoints for each person in the image.
        person = persons[k]#The loop iterates through each person (dimension 0 of the persons array) and selects the pose keypoints for that person by setting "person" equal to the pose keypoints for that specific person.
        for i in range(0, 24):
            j = i + 1
            point1 = person[i]
            point2 = person[j]
            x1 = int(point1[0])
            y1 = int(point1[1])
            x2 = int(point2[0])
            y2 = int(point2[1])
            if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                size = np.int(point1.size)
                cv2.circle(img, (x1, y1), size, (0, 255, 0), 2, lineType = 8, shift = 0)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness = 2)            
    '''
    print("Body keypoints: \n" + str(datum.poseKeypoints)+" "+str(datum.poseKeypoints.shape))
    print("Face keypoints: \n" + str(datum.faceKeypoints))
    print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
    '''
    cv2.imshow("Estimation Output", datum.cvOutputData)
    cv2.imshow("Simulation Output", img)
    cv2.waitKey(0)


def uploadVideo():
    global filename
    filename = filedialog.askopenfilename(initialdir="testVideos")#It executes that if we want to estimate the pose using video of a person then if we click the button Estimate Human Motion from Video from the interface then it tries to open the videos folder asks to select a video.


def estimateVideoPose():
    global filename
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    datum = op.Datum()
    video = cv2.VideoCapture(filename)
    while(True):
        ret, frame = video.read()
        print(ret)
        if ret == True:
             rawImage = frame
             cv2.imwrite("test.jpg",rawImage)
             imageToProcess = cv2.imread("test.jpg")
             datum.cvInputData = imageToProcess
             opWrapper.emplaceAndPop(op.VectorDatum([datum]))
             height, width = imageToProcess.shape[:2]
             img = np.zeros((height, width, 3), dtype = 'uint8')
             persons = datum.poseKeypoints    
             for k in range(0, persons.shape[0]):
                 person = persons[k]
                 for i in range(0, 24):
                     j = i + 1
                     point1 = person[i]
                     point2 = person[j]
                     x1 = int(point1[0])
                     y1 = int(point1[1])
                     x2 = int(point2[0])
                     y2 = int(point2[1])
                     if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                         size = np.int(point1.size)
                         cv2.circle(img, (x1, y1), size, (0, 255, 0), 2, lineType = 8, shift = 0)
                         cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness = 2) 
             cv2.imshow("Estimation Output", datum.cvOutputData)
             cv2.imshow("Simulation Output", img)
             if cv2.waitKey(650) & 0xFF == ord('q'):
                break  
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    
def exit():
    global main
    main.destroy()
    
font = ('times', 16, 'bold')
title = Label(main, text='Human Motion Estimation using Machine Learning', justify=LEFT)
title.config(bg='lavender blush', fg='DarkOrchid1')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=100,y=5)
title.pack()

#This code executes the upload function when we click on the button upload image in the interface
font1 = ('times', 14, 'bold')
uploadimage = Button(main, text="Upload Image", command=upload)
uploadimage.place(x=200,y=100)
uploadimage.config(font=font1)  

#This code executes the estimatePose function when we click on the button Estimate Human Motion from Image in the interface
estimateButton = Button(main, text="Estimate Human Motion from Image", command=estimatePose)
estimateButton.place(x=200,y=150)
estimateButton.config(font=font1)

#This code executes the uploadVideo function when we click on the buttonUpload Video File in the interface
uploadvideo = Button(main, text="Upload Video File", command=uploadVideo)
uploadvideo.place(x=200,y=200)
uploadvideo.config(font=font1)  

#This code executes the estimateVideoPose function when we click on the Estimate Human Motion from Video in the interface
videoButton = Button(main, text="Estimate Human Motion from Video", command=estimateVideoPose)
videoButton.place(x=200,y=250)
videoButton.config(font=font1) 

#This code executes the Exit function and it tries to stop the execution
exitapp = Button(main, text="Exit", command=exit)
exitapp.place(x=200,y=300)
exitapp.config(font=font1) 

main.config(bg='light coral')
main.mainloop()
