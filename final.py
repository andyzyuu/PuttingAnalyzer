# Citation: https://www.youtube.com/watch?v=Jvf5y21ZqtQ&list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq&ab_channel=sentdex partially inspired for cv2 info
# Citation: cv2 to pil to CMU image info drawn from demo-pil-scaling.py from CS Academy
# Citation: cv2 to pil to CMU Graphics image functionality inspired/outlined by TA Jason Niow
# Citation: Sorting using key parameter: https://www.geeksforgeeks.org/python-sorted-function/
# Citation: Enumerate function understanding: https://www.geeksforgeeks.org/enumerate-in-python/
# Citation: Polyfit understanding: https://www.youtube.com/watch?v=Dggl0fJJ81k&ab_channel=AdamGaweda and https://www.geeksforgeeks.org/numpy-poly1d-in-python/
# Citation: .index understanding: https://www.w3schools.com/python/ref_list_index.asp
# Citation: Euclidean distance formula (for calculating deviation of impact versus setup keypoints): https://www.cuemath.com/euclidean-distance-formula/#:~:text=The%20Euclidean%20distance%20formula%20is%20used%20to%20find%20the%20length,right%2Dangled%20triangle%2C%20etc.
# Citation: scipy interpolation understanding: https://www.youtube.com/watch?v=0bwVFBAZ7TI&ab_channel=CodingSpecs
# Citation: Perplexity AI for conceptual linkage of what libraries to use keypoints: Prompt: What library for math functions and interpolations?
# Citation: Function of new() using subprocess to allow user to open file: Google Generative AI - "subprocess: This allows you to run external commands. The code snippet runs an AppleScript command to open Finder's file selection dialog.""
# Citation: Z-score normalization: https://www.slingacademy.com/article/how-to-use-numpy-for-data-normalization-and-preprocessing/#standardization-(z-score-normalization)
# Ideal arc points linked: https://docs.google.com/document/d/1vbDf5ALQ6wf6Xe71ibur57L3CAqePQ7yNkYGF7oR0rw/edit?usp=sharing
from pathlib import Path
import cv2
from cmu_graphics import *
from PIL import Image
import tkinter as tk
from tkinter import Tk, filedialog
from scipy.interpolate import interp1d
import numpy as np
import easygui
import sys
import subprocess
# import sys
# print(sys.executable)
# print(sys.path)


# recording = False
# recorded = False

def onAppStart(app):
    app.capLive = cv2.VideoCapture(0)
    app.importedFile = None
    app.capImport = cv2.VideoCapture(app.importedFile)
    app.frame = None
    app.frame2 = None
    app.recording = False
    app.recorded = False
    app.frameInterval = 3 # Default to 1 
    app.live = False # User wants to use live recording 
    app.useVideo = False # User wants to import a video 
    
    app.frames = []
    app.currentFrameIndex = 0
    app.frameDelay = 100  # Milliseconds between frame changes
    app.stepsPerSecond = 1000 // app.frameDelay
    app.videoPath = None
    app.pilFrames = None
    app.frameCount = None
    app.copied = False
    
    app.keyPointsFilled = False #To display result screen when user is done with keypoints
 
    app.dots = []
    app.allDots = []
    app.counter = 0
    app.finished = False # To signal to end the replay
    
    app.replayFrames = None
    app.replaying = False
    
    app.height = int(app.capLive.get(cv2.CAP_PROP_FRAME_HEIGHT))
    app.width = int(app.capLive.get(cv2.CAP_PROP_FRAME_WIDTH))
    app.frame_size = (app.width, app.height)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 30.0, frame_size)
    app.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    app.out = cv2.VideoWriter('finalOutput.mp4', app.fourcc, 20.0, app.frame_size)
    
    app.importRectX = 367
    app.importRectY = 540
    app.greenRectWidth = 300
    app.greenRectHeight = 100
    app.liveRectX = 1102
    app.liveRectY = 540
    
    
    
    app.overallScore = None
    app.algorithmCalculated = False
    
    app.count = 0
def onStep(app):
    # frame = cv2.imread(app.cap)
    if app.useVideo == True and app.copied == False:
        app.videoPath = f'''{app.importedFile}'''

        app.pilFrames = cv2ToPilFrames(app, app.videoPath)
        app.frameCount = int(cv2.VideoCapture(app.videoPath).get(cv2.CAP_PROP_FRAME_COUNT))
        for frame in app.pilFrames:
            app.frames.append(CMUImage(frame))
            app.copied = True
        app.recorded = True
    if app.replaying == False and app.live == True:
        ret, frame = app.capLive.read()
        # print(frame)
        colorFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pilFrame = Image.fromarray(colorFrame)
        app.frame = CMUImage(pilFrame)
        
    if app.replaying == True and app.copied == False:
        app.videoPath = "/Users/andy/Term Project/finalOutput.mp4"
        app.pilFrames = cv2ToPilFrames(app, app.videoPath)
        app.frameCount = int(cv2.VideoCapture("/Users/andy/Term Project/finalOutput.mp4").get(cv2.CAP_PROP_FRAME_COUNT))
        for frame in app.pilFrames:
            app.frames.append(CMUImage(frame))
            app.copied = True
 
    if app.recording == True:
        app.out.write(frame)
    if app.keyPointsFilled == True and app.algorithmCalculated == False:
        algorithm(app, app.allDots)
    
def redrawAll(app):
    if not app.live and not app.useVideo:
        drawLabel("Welcome to Putting Analysis", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
        drawRect(app.importRectX, app.importRectY, app.greenRectWidth, app.greenRectHeight, fill='green', align='center')
        drawRect(app.liveRectX, app.liveRectY, app.greenRectWidth, app.greenRectHeight, fill='green', align='center')
        drawLabel('Import Video', 257, 540, font='montserrat', size=42, border='white', borderWidth=1.5, align='left')
        drawLabel('Live Recording', 968, 540, font='montserrat', size=42, border='white', borderWidth=1.5, align='left')
        drawLabel('Please choose between recording a live video or importing a video', 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
        # print(app.width, app.height)
    if app.frame != None and not app.replaying and app.live:
        drawImage(app.frame, 0, 0)
        if not app.recording and not app.recorded:
            drawLabel("Press 's' to begin recording and 'e' to end recording", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recording:
        drawLabel("Recording... (press 'e' to end recording)", 410, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recorded and not app.keyPointsFilled and not app.useVideo:
        drawLabel("Press 'r' to replay and draw keypoints on your putter", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recorded and not app.keyPointsFilled and app.useVideo:
        if app.currentFrameIndex < len(app.frames) and app.allDots == []:
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Start by pressing 'n' until you find the frame before your putter begins to move and draw four keypoints on each corner", 735, 30, font='montserrat', size=25, border='white', borderWidth=1.5)
        elif app.currentFrameIndex < len(app.frames):
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Click on each of the four corners of your putter and press 'n' for the next frame", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("Press 'd' to finish once the stroke is complete", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
        # drawLabel('Test', 410, 30, font='montserrat', size=42, border='white', borderWidth=1.5)

    if app.replaying and not app.keyPointsFilled:
    #     for frame in app.replayFrames:
    #         drawImage(frame, 0, 0)
        if app.currentFrameIndex < len(app.frames) and app.allDots == []:
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Start by pressing 'n' until you find the frame before your putter begins to move and draw four keypoints on each corner", 735, 30, font='montserrat', size=25, border='white', borderWidth=1.5)
        elif app.currentFrameIndex < len(app.frames):
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Click on each of the four corners of your putter and press 'n' for the next frame", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("Press 'd' to finish once the stroke is complete", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
    # if app.keyPointsFilled:
    #     drawLabel('Result of ')
    if app.keyPointsFilled and app.algorithmCalculated:
        drawLabel(f"Rating: {app.overallScore}", 200, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
        drawLabel("Click 'x' to reset", 200, 80, font='montserrat', size=42, border='white', borderWidth=1.5)
    for i in range(len(app.dots)):
        drawCircle(app.dots[i][0], app.dots[i][1], 8, fill='red', border='black')
        
def onKeyPress(app, key):
    if key == 's' and not app.recording:
        print('Recording started')
        app.recording = True
    if key == 'e' and app.recording:
        print('Recording ended')
        app.recording = False
        app.recorded = True
        app.out.release()
        # app.out = None
    if key == 'r' and app.recorded:
        print('Replaying recording')
        app.capLive.release()
        # app.replayFrames = cv2_to_cmu_frames(app.cap)
        app.replaying = True
    if key == 'n' and app.allDots == []:
        app.currentFrameIndex += app.frameInterval
    if key == 'n' and ((app.replaying and app.counter == 4) or (app.recorded and app.useVideo == True and app.counter == 4)):
        if app.currentFrameIndex < len(app.frames) - app.frameInterval:
            app.currentFrameIndex += app.frameInterval
        else:
            app.currentFrameIndex = len(app.frames) - 1
            app.keyPointsFilled = True
        app.counter = 0
        app.allDots.extend(app.dots)
        app.dots = []
    if key == 'd' and not app.keyPointsFilled and app.replaying and app.counter == 4:
        app.keyPointsFilled = True
    if key == 'd' and app.useVideo and app.counter == 4:
        app.dots = []
        app.keyPointsFilled = True
    if key == 'x' and app.keyPointsFilled:
        reset(app)
    
    # if key == 'q':
    
def onMousePress(app, mouseX, mouseY):
    
    if not app.live and not app.useVideo:
        if app.importRectX - app.greenRectWidth / 2 < mouseX < app.importRectX + app.greenRectWidth / 2 and app.importRectY - app.greenRectHeight / 2 < mouseY < app.importRectY + app.greenRectHeight / 2:
            # openFileDialog(app)
            # openFile()
            temp = new()
            app.importedFile = fileFilter(temp)
            app.useVideo = True
            
        elif app.liveRectX - app.greenRectWidth / 2 < mouseX < app.liveRectX + app.greenRectWidth / 2 and app.liveRectY - app.greenRectHeight / 2 < mouseY < app.liveRectY + app.greenRectHeight / 2:
            app.live = True
    if app.counter != 4 and not app.keyPointsFilled and app.recorded:
        app.dots.append((mouseX, mouseY))
        app.counter += 1
        
    
        
def cv2ToPilFrames(app, video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(frame)
        frames.append(pil_image)
    
    cap.release()
    return frames

def algorithm(app, listPoints):
    # listPoints is a list of tuples of each keypoint
    topLeftList = []
    bottomLeftList = []
    topRightList = []
    bottomRightList = []
    for i in range(0, len(listPoints), 4):
        group = listPoints[i:i+4]
        
        # Sort by x coordinate
        sortedX = sorted(group, key=sortByX)
        left = sortedX[:2]
        right = sortedX[2:]
        
        # Sort left points by y coordinate 
        leftSortedByY = sorted(left, key=sortByY)
        topLeft = leftSortedByY[0]
        bottomLeft = leftSortedByY[1]
        
        # Sort right points by y coordinate
        rightSortedByY = sorted(right, key=sortByY)
        topRight = rightSortedByY[0]
        bottomRight = rightSortedByY[1]
        
        topLeftList.append(topLeft)
        bottomLeftList.append(bottomLeft)
        topRightList.append(topRight)
        bottomRightList.append(bottomRight)
        
    # Actual algorithm (looking for a slight arc in, back to impact/original location, then arc in)
    app.overallScore = (algHelper(topLeftList, 0) + algHelper(bottomLeftList, 1) + algHelper(topRightList, 2) + algHelper(bottomRightList, 3)) / 4
    app.algorithmCalculated = True
    
    # setupTL = topLeftList[0]
    # setupBL = bottomLeftList[0]
    # setupTR = topRightList[0]
    # setupBR = bottomRightList[0]
    
    # for i in range(len(topLeftList)):
        
def sortByX(point):
    return point[0]
    
def sortByY(point):
    return point[1]

def algHelper(coordinates, cycle):
    # print(coordinates)
    xCoordinates = []
    yCoordinates = []
    for coord in coordinates:
        xCoordinates.append(coord[0])
    for coord in coordinates:
        yCoordinates.append(coord[1])
    # print(xCoordinates)
    # print(yCoordinates)
    impactPointCoords = findImpactPoint(coordinates)  
    impactPointIndex = coordinates.index(impactPointCoords)
    # print(impactPointCoords)
    
    
    def arcConsistency(x, y):
        xN = np.array(xCoordinates)
        yN = np.array(yCoordinates)

        xNorm = (xN - xN.mean()) / xN.std()
        yNorm = (yN - yN.mean()) / yN.std()
        quadratic = np.polyfit(xNorm, yNorm, 2)
        arcHeight = abs(quadratic[0]) # first coeiff. of the quadratic, captures most of the curve-ness of the arc
        if cycle == 0:
            idealMinArc = 0.25 # Top left
            idealMaxArc = 0.7 # Top left
            idealMean = (idealMinArc + idealMaxArc) / 2
        elif cycle == 1:
            idealMinArc = 0.02 # Bottom left
            idealMaxArc = 1.94 # Bottom left
            idealMean = (idealMinArc + idealMaxArc) / 2
        elif cycle == 2:
            idealMinArc = 0.0003 # Top Right
            idealMaxArc = 0.29 # Top Right
            idealMean = (idealMinArc + idealMaxArc) / 2
        elif cycle == 3:
            idealMinArc = 0.065 # Bottom Right
            idealMaxArc = 0.75 # Bottom Right
            idealMean = (idealMinArc + idealMaxArc) / 2
        print('Ideal Mean: ' + str(idealMean))
        print('Arc Height' + str(arcHeight))
        return 100 - abs(idealMean - arcHeight) * 45
        if arcHeight < idealMinArc:
            return 100 - (idealMinArc - arcHeight) * 100 # scaling the differences
        elif arcHeight > idealMaxArc:
            return 100 - (arcHeight - idealMaxArc) * 100 
        else:
            return 100
    # print(impactPointIndex)
    # print(xCoordinates[:impactPointIndex])
    # print(yCoordinates[:impactPointIndex])
    postImpactArcConsistency = arcConsistency(xCoordinates[:impactPointIndex], yCoordinates[:impactPointIndex])
    preImpactArcConsistency = arcConsistency(xCoordinates[impactPointIndex:], yCoordinates[impactPointIndex:])

    overallArcConsistency = 100 - abs(postImpactArcConsistency - preImpactArcConsistency)
    
    setupCoords = coordinates[0]
    impactSetupEuclidean = np.sqrt((setupCoords[0] - impactPointCoords[0])**2 + (setupCoords[1] - impactPointCoords[1])**2)
    impactSetupComparisonScore = 100 - impactSetupEuclidean * 0.5
    
    # preImpactPathInterp = interp1d(xCoordinates[:impactPointIndex], yCoordinates[:impactPointIndex], kind='quadratic')
    # postImpactPathInterp = interp1d(xCoordinates[impactPointIndex:], yCoordinates[impactPointIndex:], kind='quadratic')

    # commonX = xCoordinates[:(min(impactPointIndex, len(xCoordinates)-impactPointIndex)) - 1] # Finds a position either at impact position or close to impact position to have a X variable to compare
    # print("commonX:", commonX)

    # prePostImpactComparison = np.mean(np.abs(preImpactPathInterp(commonX) - postImpactPathInterp(commonX)))
    # prePostImpactComparisonScore = 100 - prePostImpactComparison * 0.12
    print(postImpactArcConsistency)
    print(preImpactArcConsistency)
    print(overallArcConsistency)
    print(impactSetupComparisonScore)
    overallScore = (0.25 * (postImpactArcConsistency + preImpactArcConsistency) / 2 +
        0.25 * overallArcConsistency +
        0.5 * impactSetupComparisonScore) #+
        # 0.1 * prePostImpactComparisonScore)
    print(coordinates)
    return rounded(max(min(overallScore, 100), 0))

# def findImpactPoint(coordinates):
#     minY = float('inf') # Makes sure that the first value is always min_y, and goes past the initial decrease from backstroke to forwardstroke
#     minYIndex = 0
#     for i, (x, y) in enumerate(coordinates):
#         if y < minY:
#             print('!!!!!')
#             minY = y
#             minYIndex = i
#             print(minY)
#             print(minYIndex)
#         elif y > minY: # When stroke comes back to impact, return the coordinate
#             print(y)
#             print(minY)
#             return coordinates[minYIndex]
#     return None
def findImpactPoint(coordinates): #debugged
    setupY = coordinates[0][1]
    for i, (x, y) in enumerate(coordinates):
        if y < setupY and i > 0.55 * len(coordinates):
            return coordinates[i]

def new():
    file_path = subprocess.check_output(["osascript", "-e", 'choose file']).decode("utf-8").strip()
    return file_path
    # if file_path:
    #     print("Selected file:", file_path)
    
def fileFilter(file):
    counter = 0
    result = ''
    for line in file.split(':'):
        if counter == 0:
            counter += 1
            result += '/'
            continue
        else:
            result = result + line + '/'
    return result[:-1]

def reset(app):
    app.capLive = cv2.VideoCapture(0)
    app.importedFile = None
    app.capImport = cv2.VideoCapture(app.importedFile)
    app.frame = None
    app.frame2 = None
    app.recording = False
    app.recorded = False
    app.frameInterval = 3 # Default to 1 
    app.live = False # User wants to use live recording 
    app.useVideo = False # User wants to import a video 
    
    app.frames = []
    app.currentFrameIndex = 0
    app.frameDelay = 100  # Milliseconds between frame changes
    app.stepsPerSecond = 1000 // app.frameDelay
    app.videoPath = None
    app.pilFrames = None
    app.frameCount = None
    app.copied = False
    
    app.keyPointsFilled = False #To display result screen when user is done with keypoints
 
    app.dots = []
    app.allDots = []
    app.counter = 0
    app.finished = False # To signal to end the replay
    
    app.replayFrames = None
    app.replaying = False
    
    app.height = int(app.capLive.get(cv2.CAP_PROP_FRAME_HEIGHT))
    app.width = int(app.capLive.get(cv2.CAP_PROP_FRAME_WIDTH))
    app.frame_size = (app.width, app.height)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 30.0, frame_size)
    app.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    app.out = cv2.VideoWriter('finalOutput.mp4', app.fourcc, 20.0, app.frame_size)
    
    app.importRectX = 367
    app.importRectY = 540
    app.greenRectWidth = 300
    app.greenRectHeight = 100
    app.liveRectX = 1102
    app.liveRectY = 540
    
    
    
    app.overallScore = None
    app.algorithmCalculated = False
        
runApp(width=1470, height=891)