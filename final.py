# Citation: Background Image Link: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.hjgt.org%2Fblog%2Fhelpful-tip-tuesday-putting-golf%2F&psig=AOvVaw3NsWEDBimUyujNVApcovY2&ust=1733277390602000&source=images&cd=vfe&opi=89978449&ved=0CBcQjhxqFwoTCNjTuMu_iooDFQAAAAAdAAAAABAQ
# Citation: https://www.youtube.com/watch?v=Jvf5y21ZqtQ&list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq&ab_channel=sentdex partially inspired for cv2 info
# Citation: cv2 to pil to CMU image info drawn from demo-pil-scaling.py from CS Academy
# Citation: cv2 to pil to CMU Graphics image functionality inspired/outlined by TA Jason Niow
# Citation: cv2 frame count knowledge from cv2 documentation: https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#ggaeb8dd9c89c10a5c63c139bf7c4f5704dadadc646b31cfd2194794a3a80b8fa6c2
# Citation: Sorting using key parameter: https://www.geeksforgeeks.org/python-sorted-function/
# Citation: Enumerate function understanding: https://www.geeksforgeeks.org/enumerate-in-python/
# Citation: Polyfit understanding: https://www.youtube.com/watch?v=Dggl0fJJ81k&ab_channel=AdamGaweda and https://www.geeksforgeeks.org/numpy-poly1d-in-python/
# Citation: .index understanding: https://www.w3schools.com/python/ref_list_index.asp
# Citation: Euclidean distance formula (for calculating deviation of impact versus setup keypoints): https://www.cuemath.com/euclidean-distance-formula/#:~:text=The%20Euclidean%20distance%20formula%20is%20used%20to%20find%20the%20length,right%2Dangled%20triangle%2C%20etc.
# Citation: scipy interpolation understanding: https://www.youtube.com/watch?v=0bwVFBAZ7TI&ab_channel=CodingSpecs # Note: Not applied in final algorithm due to bugs
# Citation: Perplexity AI for conceptual linkage of what libraries to use keypoints: Prompt: What library for math functions and interpolations?
# Citation: Z-score normalization: https://www.slingacademy.com/article/how-to-use-numpy-for-data-normalization-and-preprocessing/#standardization-(z-score-normalization)
# Citation: Using os listdir to allow user to choose a file (that leads to file path and thus ability to read video file): https://www.geeksforgeeks.org/python-os-listdir-method/
# Ideal arc points linked: https://docs.google.com/document/d/1vbDf5ALQ6wf6Xe71ibur57L3CAqePQ7yNkYGF7oR0rw/edit?usp=sharing
import os
import cv2
from cmu_graphics import *
from PIL import Image
from urllib.request import urlopen
# from scipy.interpolate import interp1d
import numpy as np


def onAppStart(app):
    app.bgPILImage = (Image.open(urlopen('https://www.hjgt.org/wp-content/uploads/2024/02/Putting.jpg')))
    app.bgImage = CMUImage(app.bgPILImage.resize((1470, 891)))
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
    app.frameDelay = 1  # Milliseconds between frame changes
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
    app.out = cv2.VideoWriter('finalOutput.mp4', app.fourcc, 3.0, app.frame_size)
    
    app.importRectX = 367
    app.importRectY = 540
    app.greenRectWidth = 300
    app.greenRectHeight = 100
    app.liveRectX = 1102
    app.liveRectY = 540
    
    app.redBackX = 70
    app.redBackY = 750
    app.redBackWidth = 225
    app.redBackHeight = 100
    
    app.helpX = 735
    app.helpY = 750
    app.helpWidth = 200
    app.helpHeight = 100
    
    app.overallScore = None
    app.algorithmCalculated = False
    app.ratingColor = None
    
    app.count = 0
    
    app.length = None
    app.mp4List = None
    app.wantToOpen = False
    app.panelOpened = False
    app.chosen = False
    app.helpOpen = False
    
    app.postImpactArcTL = None
    app.postImpactArcBL = None
    app.postImpactArcTR = None
    app.postImpactArcBR = None
    
    
    app.preImpactArcTL = None
    app.preImpactArcBL = None
    app.preImpactArcTR = None
    app.preImpactArcBR = None
    
    app.impactSetupComparsonTL = None
    app.impactSetupComparsonBL = None
    app.impactSetupComparsonTR = None
    app.impactSetupComparsonBR = None
    
def onStep(app):
    if app.useVideo == True and app.copied == False:
        app.videoPath = f'''{app.importedFile}'''

        app.pilFrames = cv2ToPilFrames(app, app.videoPath)
        app.frameCount = int(cv2.VideoCapture(app.videoPath).get(cv2.CAP_PROP_FRAME_COUNT))
        for frame in app.pilFrames:
            app.frames.append(CMUImage(frame))
            app.copied = True
        # app.recorded = True
    if app.replaying == False and app.live == True:
        ret, frame = app.capLive.read()
        # print(frame)
        colorFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pilFrame = Image.fromarray(colorFrame)
        app.frame = CMUImage(pilFrame)
        
        
    if app.replaying == True and app.copied == False:
        app.videoPath = "/Users/andy/Term Project/finalOutput.mp4"
        tempCap = cv2.VideoCapture(app.videoPath)
        fps = tempCap.get(cv2.CAP_PROP_FPS) 
        print('FPS: ' + str(fps))
        app.pilFrames = cv2ToPilFrames(app, app.videoPath)
        app.frameCount = int(cv2.VideoCapture("/Users/andy/Term Project/finalOutput.mp4").get(cv2.CAP_PROP_FRAME_COUNT))
        print(app.frameCount)
        for frame in app.pilFrames:
            app.frames.append(CMUImage(frame))
            cv2.waitKey(int(1000 / 30))
            app.copied = True
 
    if app.recording == True:
        # cv2.waitKey(int(1000 / 30))
        
        app.out.write(frame)
    if app.keyPointsFilled == True and app.algorithmCalculated == False:
        algorithm(app, app.allDots)
    if app.algorithmCalculated == True:
        if app.overallScore < 50:
            app.ratingColor = 'red'
        elif app.overallScore < 75:
            app.ratingColor = 'orange'
        elif app.overallScore < 85:
            app.ratingColor = 'yellow'
        else:
            app.ratingColor = 'green'
            
def redrawAll(app):
    if not app.live and not app.useVideo and not app.wantToOpen:
        drawImage(app.bgImage, 0, 445, align='left')
        drawLabel("Welcome to Putting Analyzer", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
        drawRect(app.importRectX, app.importRectY, app.greenRectWidth, app.greenRectHeight, fill='green', align='center', border='lightgreen', borderWidth=1.5)
        drawRect(app.liveRectX, app.liveRectY, app.greenRectWidth, app.greenRectHeight, fill='green', align='center', border='lightgreen', borderWidth=1.5)
        drawRect(app.helpX, app.helpY, app.helpWidth, app.helpHeight, fill='green', align='center', border='lightgreen', borderWidth=1.5)
        drawLabel('Import Video', 257, 540, font='montserrat', size=42, border='white', borderWidth=1.5, align='left')
        drawLabel('Live Recording', 968, 540, font='montserrat', size=42, border='white', borderWidth=1.5, align='left')
        drawLabel('Help', 697, 750, font='montserrat', size=42, border='white', borderWidth=1.5, align='left')
        drawLabel('Please choose between importing a video or recording a live video', 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
      
    if app.helpOpen: 
        drawRect(0, 0, 1470, 891, fill='darkgreen')
        drawLabel('Putting Analyzer FAQ', 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
        drawLabel('Q: How to use Putting Analyzer?', 22, 80, font='montserrat', size=42, border='white', borderWidth=2.5, bold=True, align='left')
        drawLabel('A: Using either imported files from the same file directory or using a live webcam, with the camera angled slightly down and 18-24 inches above the ground,', 735, 120, size=21, border='white', borderWidth=1.5)
        drawLabel('and record your putting stroke. After, using your mouse, attach keypoints on the 4 corners of your putter head, doing it frame by frame until the video', 735, 150, size=21, border='white', borderWidth=1.5)
        drawLabel('ends or when the stroke has ended, and your final rating will be outputted, from a rating of 0 to 100.', 735, 180, size=21, border='white', borderWidth=1.5)
        drawLabel('Q: How does the algorithm work?', 22, 240, font='montserrat', size=42, border='white', borderWidth=2.5, bold=True, align='left')
        drawLabel('A: Using the keypoints inputted by the user, each point is separated into a top left, top right, bottom left, and bottom right keypoint. After doing so,', 735, 280, size=21, border='white', borderWidth=1.5)
        drawLabel('the keypoints of each category are illustrated by a polynomial of the 2nd degree. Taking the coefficient of the highest degree variable, we can', 735, 310, size=21, border='white', borderWidth=1.5)
        drawLabel('visualize the curve of the putter head, and using those values to calculate the impact location versus the setup, and the overall arc to an optimal one.', 735, 340, size=21, border='white', borderWidth=1.5)
        drawLabel('Q: How is the feedback generated?', 22, 400, font='montserrat', size=42, border='white', borderWidth=2.5, bold=True, align='left')
        drawLabel('A: Using the information that the algorithm generates, we can have an approximate understanding of the weak points of your putting stroke, and thus is', 735, 440, size=21, border='white', borderWidth=1.5)
        drawLabel('the software can specify the parts that may need particular improvement or focus.', 735, 470, size=21, border='white', borderWidth=1.5)
        drawLabel('Q: How can we use the previous recording that we recorded', 22, 530, font='montserrat', size=42, border='white', borderWidth=2.5, bold=True, align='left')
        drawLabel('in order to analyze again?', 22, 570, font='montserrat', size=42, border='white', borderWidth=2.5, bold=True, align='left')
        drawLabel('''A: After clicking "Import Video" in the home page, you can then choose the mp4 file named "previousRecording.mp4" This mp4 will portray the previous''', 735, 610, size=21, border='white', borderWidth=1.5)
        drawLabel('recording that was recorded within the software. Note that after recording again, that previous recording file will be replaced with a new recording.', 735, 640, size=21, border='white', borderWidth=1.5)
        drawRect(app.redBackX, app.redBackY, app.redBackWidth, app.redBackHeight, fill='red', border='darkred', borderWidth=3)
        drawLabel('Back', 180, 800, font='montserrat', size=42, border='white', borderWidth=1.5)     
        
    if app.wantToOpen:
        drawRect(0, 0, 1470, 891, fill='darkgreen')
        for i in range(app.length):
            if i == 0:
                drawRect(735, 100, 800, 691 / app.length, fill='green', align='center', border='lightgreen', borderWidth=1.5)
                drawLabel(f'{app.mp4List[i]}', 735, 100 , font='montserrat', size=42, border='white', borderWidth=1.5, align='center')
            else:
                drawRect(735, 100 + (691 / app.length) * i, 800, 691 / app.length, fill='green', align='center', border='lightgreen', borderWidth=1.5)
                drawLabel(f'{app.mp4List[i]}', 735, 100 + (691 / app.length) * i, font='montserrat', size=42, border='white', borderWidth=1.5, align='center')
        
        drawRect(app.redBackX, app.redBackY, app.redBackWidth, app.redBackHeight, fill='red', border='darkred', borderWidth=3)
        drawLabel('Back', 180, 800, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.frame != None and not app.replaying and app.live:
        drawImage(app.frame, 0, 0)
        if not app.recording and not app.recorded:
            drawLabel("Press 's' to begin recording and 'e' to end recording", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recording:
        drawLabel("Recording... (press 'e' to end recording)", 410, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recorded and not app.keyPointsFilled and not app.useVideo and not app.wantToOpen:
        drawLabel("Press 'r' to replay and draw keypoints on your putter", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recorded and not app.keyPointsFilled and app.useVideo and not app.wantToOpen:
        if app.currentFrameIndex < len(app.frames) and app.allDots == []:
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Start by pressing 'n' until you find the frame before ", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("your putter begins to move and draw four keypoints on each corner", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
        elif app.currentFrameIndex < len(app.frames):
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Click on each of the four corners of your putter and press 'n' for the next frame," , 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("or press 'b' to remove your previous keypoint", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("Press 'd' to finish once the stroke is complete", 735, 110, font='montserrat', size=42, border='white', borderWidth=1.5)

    if app.replaying and not app.keyPointsFilled and not app.wantToOpen:
    #     for frame in app.replayFrames:
    #         drawImage(frame, 0, 0)
        if app.currentFrameIndex < len(app.frames) and app.allDots == []:
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Start by pressing 'n' until you find the frame before ", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("your putter begins to move and draw four keypoints on each corner", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
        elif app.currentFrameIndex < len(app.frames):
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Click on each of the four corners of your putter and press 'n' for the next frame," , 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("or press 'b' to remove your previous keypoint", 735, 70, font='montserrat', size=42, border='white', borderWidth=1.5)
            drawLabel("Press 'd' to finish once the stroke is complete", 735, 110, font='montserrat', size=42, border='white', borderWidth=1.5)
    # if app.keyPointsFilled:
    #     drawLabel('Result of ')
    if app.keyPointsFilled and app.algorithmCalculated:
        impactFeedback = None
        postImpactArcFeedback = None
        preImpactArcFeedback = None
        drawImage(app.bgImage, 0, 445, align='left')
        drawLabel("Press 'x' to reset and import another video or record a live video", 735, 865, font='montserrat', size=42, border='white', borderWidth=1.5)
        drawLabel(f"Rating: ", 450, 185, font='montserrat', size=95, border=app.ratingColor, borderWidth=1.7, bold=True)
        if app.ratingColor != 'yellow':
            drawCircle(800, 185, 175, fill='dark' + app.ratingColor, opacity=75, border='black', borderWidth=2)
        elif app.ratingColor == 'yellow':
            drawCircle(800, 185, 175, fill='gold', opacity=75, border='black', borderWidth=2)
        drawCircle(800, 185, 145, fill=app.ratingColor, opacity=50, border='black', borderWidth=1)
        drawLabel(f"{app.overallScore}", 800, 185, font='montserrat', size=95, border=app.ratingColor, borderWidth=1.7, bold=True)
        if app.impactSetupComparisonTL < 40 or app.impactSetupComparisonBL < 40 or app.impactSetupComparisonTR < 40 or app.impactSetupComparisonBR < 40 and impactFeedback == None:
            impactFeedback = 'poor, and we suggest to make sure you are hitting the ball in the middle of the face.'
        elif app.impactSetupComparisonTL < 75 or app.impactSetupComparisonBL < 75 or app.impactSetupComparisonTR < 75 or app.impactSetupComparisonBR < 75 and impactFeedback == None:
            impactFeedback = 'mediocre, and we would suggest to look at your impact position.'
        elif app.impactSetupComparisonTL < 100 or app.impactSetupComparisonBL < 100 or app.impactSetupComparisonTR < 100 or app.impactSetupComparisonBR < 100 and impactFeedback == None:
            impactFeedback = 'great!'
        if app.postImpactArcTL < 0 or app.postImpactArcBL < 0 or app.postImpactArcTR < 0 or app.postImpactArcBR < 0 and postImpactArcFeedback == None:
            postImpactArcFeedback = 'very poor, and we would suggest you focus on the consistency of the forwardstroke arc.'
        elif app.postImpactArcTL < 60 or app.postImpactArcBL < 60 or app.postImpactArcTR < 60 or app.postImpactArcBR < 60 and postImpactArcFeedback == None:
            postImpactArcFeedback = 'mediocre, and we would suggest to continue to pay attention to the forwardstroke arc.'
        elif app.postImpactArcTL < 100 or app.postImpactArcBL < 100 or app.postImpactArcTR < 100 or app.postImpactArcBR < 100 and postImpactArcFeedback == None:
            postImpactArcFeedback = 'great!'
        if app.preImpactArcTL < 0 or app.preImpactArcBL < 0 or app.preImpactArcTR < 0 or app.preImpactArcBR < 0 and preImpactArcFeedback == None:
            preImpactArcFeedback = 'very poor, and we would suggest you focus on the consistency of the backstroke arc.'
        elif app.preImpactArcTL < 60 or app.preImpactArcBL < 60 or app.preImpactArcTR < 60 or app.preImpactArcBR < 60 and preImpactArcFeedback == None:
            preImpactArcFeedback = 'mediocre, and we would suggest to continue to pay attention to the backstroke arc.'
        elif app.preImpactArcTL < 100 or app.preImpactArcBL < 100 or app.preImpactArcTR < 100 or app.preImpactArcBR < 100 and preImpactArcFeedback == None:
            preImpactArcFeedback = 'great!'     
        drawLabel('Feedback: Based on the keypoints inputted, your pre-impact arc was...', 25, 470, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)  
        drawLabel(f"{preImpactArcFeedback}", 25, 510, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True) 
        drawLabel(f"In addition, your post-impact arc was...", 25, 550, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)
        drawLabel(f"{postImpactArcFeedback}", 25, 590, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)
        drawLabel(f"Finally, your impact position was...", 25, 630, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)
        drawLabel(f"{impactFeedback}", 25, 670, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)
        drawLabel("Good job and keep practicing!", 25, 710, align='left', font='montserrat', size=37, border='white', borderWidth=1.5, bold=True)
        # Note: Pre-impact and backstroke are synonyms, and so are post-impact and forwardstroke
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
        copyVideo(app, "/Users/andy/Term Project/finalOutput.mp4", "/Users/andy/Term Project/previousRecording.mp4")
        # app.replayFrames = cv2_to_cmu_frames(app.cap)
        app.replaying = True
    if key == 'n' and app.allDots == [] and app.useVideo and app.importedFile != "/Users/andy/Term Project/previousRecording.mp4/":
        print('!!!!')
        print(app.importedFile)
        app.currentFrameIndex += app.frameInterval
    if key == 'n' and app.allDots == [] and (app.live or app.importedFile == "/Users/andy/Term Project/previousRecording.mp4/"):
        app.currentFrameIndex += 1
    if key == 'n' and ((app.replaying and app.counter == 4) or (app.recorded and (app.useVideo == True or app.live) and app.counter == 4)):
        if app.currentFrameIndex < len(app.frames) - app.frameInterval and app.useVideo and app.importedFile != "/Users/andy/Term Project/previousRecording.mp4/":
            app.currentFrameIndex += app.frameInterval
        elif app.currentFrameIndex < len(app.frames) - app.frameInterval and (app.live or app.importedFile == "/Users/andy/Term Project/previousRecording.mp4/"):
            app.currentFrameIndex += 1
        else:
            app.currentFrameIndex = len(app.frames) - 1
            app.keyPointsFilled = True
        app.counter = 0
        app.allDots.extend(app.dots)
        app.dots = []
    if key == 'b' and (app.replaying or app.recorded and app.useVideo) and app.counter != 0:
        app.dots.pop()
        app.counter -= 1
    if key == 'd' and not app.keyPointsFilled and app.replaying and app.counter == 4:
        app.keyPointsFilled = True
    if key == 'd' and (app.useVideo or app.live) and app.counter == 4:
        app.dots = []
        app.keyPointsFilled = True
    if key == 'x' and app.keyPointsFilled:
        reset(app)
    
    # if key == 'q':
    
def onMousePress(app, mouseX, mouseY):
    
    if app.counter != 4 and not app.keyPointsFilled and app.recorded and not app.wantToOpen:
        app.dots.append((mouseX, mouseY))
        app.counter += 1
    
    # if :
    if app.wantToOpen and 735 - 800 / 2 < mouseX < 735 + 800 / 2 and 100 - 691 / app.length / 2 < mouseY < 100 + 691 / app.length / 2:
        
        app.importedFile = fileFilter(app.mp4List[0])
        app.useVideo = True
        app.recorded = True
        app.wantToOpen = False
    if app.wantToOpen and 735 - 800 / 2 < mouseX < 735 + 800 / 2 and 100 + (691 / app.length) < mouseY < 100 + (691 / app.length) * app.length:
        app.importedFile = fileFilter(app.mp4List[int(mouseY // (691 / app.length))])
        app.useVideo = True
        app.recorded = True
        app.wantToOpen = False
        
    if (app.wantToOpen or app.helpOpen) and app.redBackX < mouseX < app.redBackX + app.redBackWidth and app.redBackY < mouseY < app.redBackY + app.redBackHeight:
        app.wantToOpen = False
        app.helpOpen = False
    if not app.live and not app.useVideo:
        if app.importRectX - app.greenRectWidth / 2 < mouseX < app.importRectX + app.greenRectWidth / 2 and app.importRectY - app.greenRectHeight / 2 < mouseY < app.importRectY + app.greenRectHeight / 2:
            gatherMP4Files(app)
            app.wantToOpen = True
        elif app.liveRectX - app.greenRectWidth / 2 < mouseX < app.liveRectX + app.greenRectWidth / 2 and app.liveRectY - app.greenRectHeight / 2 < mouseY < app.liveRectY + app.greenRectHeight / 2:
            app.live = True
        elif app.helpX - app.helpWidth / 2 < mouseX < app.helpX + app.helpWidth and app.helpY - app.helpHeight / 2 < mouseY < app.helpY + app.helpHeight / 2:
            app.helpOpen = True
    

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
    app.overallScore = (algHelper(app, topLeftList, 0) + algHelper(app, bottomLeftList, 1) + algHelper(app, topRightList, 2) + algHelper(app, bottomRightList, 3)) / 4
    app.algorithmCalculated = True
    
        
def sortByX(point):
    return point[0]
    
def sortByY(point):
    return point[1]

def algHelper(app, coordinates, cycle):
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
        # idealMean = 0.12
        if cycle == 0:
            # idealMinArc = 0.25 # Top left
            # idealMaxArc = 0.7 # Top left
            # idealMean = (idealMinArc + idealMaxArc) / 2
            idealMean = 0.0445 # Value chosen based on ideal arc for top left keypoint
        elif cycle == 1:
            # idealMinArc = 0.02 # Bottom left
            # idealMaxArc = 1.94 # Bottom left
            # idealMean = (idealMinArc + idealMaxArc) / 2
            idealMean = 0.086 # Value chosen based on ideal arc for bottom left keypoint
        elif cycle == 2:
            # idealMinArc = 0.0003 # Top Right
            # idealMaxArc = 0.29 # Top Right
            # idealMean = (idealMinArc + idealMaxArc) / 2
            idealMean = 0.062 # Value chosen based on ideal arc for top right keypoint 
        elif cycle == 3:
            # idealMinArc = 0.065 # Bottom Right
            # idealMaxArc = 0.75 # Bottom Right
            # idealMean = (idealMinArc + idealMaxArc) / 2
            idealMean = 0.3 # Value chosen based on ideal arc for bottom right keypoint 
        print('Ideal Mean: ' + str(idealMean))
        print('Arc Height' + str(arcHeight))
        return 100 - abs(idealMean - arcHeight) * 500
        # if arcHeight < idealMinArc:
        #     return 100 - (idealMinArc - arcHeight) * 100 # scaling the differences
        # elif arcHeight > idealMaxArc:
        #     return 100 - (arcHeight - idealMaxArc) * 100 
        # else:
        #     return 100
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
    if cycle == 0:
        app.postImpactArcTL = postImpactArcConsistency
        app.preImpactArcTL = preImpactArcConsistency
        app.impactSetupComparisonTL = impactSetupComparisonScore
    elif cycle == 1:
        app.postImpactArcBL = postImpactArcConsistency
        app.preImpactArcBL = preImpactArcConsistency
        app.impactSetupComparisonBL = impactSetupComparisonScore
    elif cycle == 2:
        app.postImpactArcTR = postImpactArcConsistency
        app.preImpactArcTR = preImpactArcConsistency
        app.impactSetupComparisonTR = impactSetupComparisonScore
    elif cycle == 3:
        app.postImpactArcBR = postImpactArcConsistency
        app.preImpactArcBR = preImpactArcConsistency
        app.impactSetupComparisonBR = impactSetupComparisonScore

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

def findImpactPoint(coordinates): #debugged
    setupY = coordinates[0][1]
    for i, (x, y) in enumerate(coordinates):
        if y < setupY and i > 0.55 * len(coordinates):
            return coordinates[i]

def gatherMP4Files(app):
    path = os.getcwd() 
    dirList = os.listdir(path) 

    mp4List = []
    for file in dirList:
        if file[-4:] == '.mp4':
            mp4List.append(file)
    app.length = len(mp4List)
    app.mp4List = mp4List

  
def fileFilter(file):
    path = os.getcwd() 
    temp = str(path) + '/' + str(file) +'/'
    return temp


def copyVideo(app, inputPath, outputPath):
    originalCap = cv2.VideoCapture(inputPath)
    
    out = cv2.VideoWriter(outputPath, app.fourcc, 20.0, app.frame_size)
    
    while True:
        ret, frame = originalCap.read()
        if not ret: 
            break
        out.write(frame)
    
    originalCap.release()
    out.release
    
def reset(app):
    app.bgPILImage = (Image.open(urlopen('https://www.hjgt.org/wp-content/uploads/2024/02/Putting.jpg')))
    app.bgImage = CMUImage(app.bgPILImage.resize((1470, 891)))
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
    
    app.redBackX = 70
    app.redBackY = 750
    app.redBackWidth = 225
    app.redBackHeight = 100
    
    app.overallScore = None
    app.algorithmCalculated = False
    app.ratingColor = None
    
    app.count = 0
    
    app.length = None
    app.mp4List = None
    app.wantToOpen = False
    app.panelOpened = False
    app.chosen = False
    app.helpOpen = False
        
    app.postImpactArcTL = None
    app.postImpactArcBL = None
    app.postImpactArcTR = None
    app.postImpactArcBR = None
    
    
    app.preImpactArcTL = None
    app.preImpactArcBL = None
    app.preImpactArcTR = None
    app.preImpactArcBR = None
    
    app.impactSetupComparsonTL = None
    app.impactSetupComparsonBL = None
    app.impactSetupComparsonTR = None
    app.impactSetupComparsonBR = None
    
runApp(width=1470, height=891)