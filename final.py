# Citation: https://www.youtube.com/watch?v=Jvf5y21ZqtQ&list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq&ab_channel=sentdex partially inspired 
# Citation: cv2 to pil to CMU image info drawn from demo-pil-scaling.py from CS academy

import cv2
from cmu_graphics import *
from PIL import Image

# recording = False
# recorded = False

def onAppStart(app):
    app.capLive = cv2.VideoCapture(0)
    # app.cap = cv2.VideoCapture("/Users/andy/Term Project/finalOutput.mp4")
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
  

    
def onStep(app):
    # frame = cv2.imread(app.cap)
    if not app.replaying:
        ret, frame = app.capLive.read()
        # print(frame)
        colorFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pilFrame = Image.fromarray(colorFrame)
        app.frame = CMUImage(pilFrame)
        
    if app.replaying and not app.copied:
        app.videoPath = "/Users/andy/Term Project/finalOutput.mp4"
        app.pilFrames = cv2_to_pil_frames(app, app.videoPath)
        app.frameCount = int(cv2.VideoCapture("/Users/andy/Term Project/finalOutput.mp4").get(cv2.CAP_PROP_FRAME_COUNT))
        for frame in app.pilFrames:
            app.frames.append(CMUImage(frame))
            app.copied = True
 
    if app.recording == True:
        app.out.write(frame)
  
    
def redrawAll(app):
    # if not app.live and not app.useVideo:
    #     drawLabel("Welcome to Putting Analysis", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    #     drawRect(400, 540, 200, 100, fill='green')
    #     drawRect(800, 540, 200, 100, fill='green')
    #     print(app.width, app.height)
    if app.frame != None and not app.replaying:
        drawImage(app.frame, 0, 0)
        if not app.recording and not app.recorded:
            
            drawLabel("Press 's' to begin recording and 'e' to end recording", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recording:
        drawLabel("Recording... (press 'e' to end recording)", 410, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    if app.recorded and not app.keyPointsFilled:
        drawLabel("Press 'r' to replay and draw keypoints on your putter", 700, 30, font='montserrat', size=42, border='white', borderWidth=1.5)

    if app.replaying and not app.keyPointsFilled:
    #     for frame in app.replayFrames:
    #         drawImage(frame, 0, 0)
        if app.currentFrameIndex < len(app.frames):
            drawImage(app.frames[app.currentFrameIndex], 0, 0)
            drawLabel("Click on each of the four corners of your putter and press 'n' for the next frame", 735, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
    # if app.keyPointsFilled:
    #     drawLabel('Result of ')
    if app.keyPointsFilled:
        drawLabel("Result", 200, 30, font='montserrat', size=42, border='white', borderWidth=1.5)
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
    if key == 'n' and app.replaying and app.counter == 4:
        if app.currentFrameIndex < len(app.frames) - app.frameInterval:
            app.currentFrameIndex += app.frameInterval
        else:
            app.currentFrameIndex = len(app.frames) - 1
            app.keyPointsFilled = True
            
        app.counter = 0
        app.allDots.extend(app.dots)
        app.dots = []
    if key == 'x' and app.keyPointsFilled:
        reset(app)
    
    # if key == 'q':
    
def onMousePress(app, mouseX, mouseY):
  
    if app.counter != 4 and not app.keyPointsFilled and app.recorded:
        app.dots.append((mouseX, mouseY))
        app.counter += 1
        
def cv2_to_pil_frames(app, video_path):
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

def reset(app):
    app.capLive = cv2.VideoCapture(0)
    # app.cap = cv2.VideoCapture("/Users/andy/Term Project/finalOutput.mp4")
    app.frame = None
    app.frame2 = None
    app.recording = False
    app.recorded = False
    app.frameInterval = 3 # Default to 1 
    
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
        
runApp(width=1470, height=891)