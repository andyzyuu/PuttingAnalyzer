from cmu_graphics import *


def onAppStart(app):
    print('onAppStart is being called')
    app.frames = []
    app.dots = []
    app.allDots = []
    app.counter = 0
    # app.currentFrameIndex = 0
    # app.frameDelay = 100  # Milliseconds between frame changes

    # for frame in pil_frames:
    #     app.frames.append(CMUImage(frame))
    
    # app.stepsPerSecond = 1000 // app.frameDelay

# def onStep(app):
#     # app.currentFrameIndex = (app.currentFrameIndex + 1) % len(app.frames) # Loops 
#     app.currentFrameIndex = app.currentFrameIndex + 1

def redrawAll(app):
    # print('redrawAll is working')
    # drawLabel('We got here', 200, 200)
    # # for i in range(len(app.frames)):
    # #     drawImage(app.frames[])
    # if app.currentFrameIndex < len(app.frames):
    #     drawImage(app.frames[app.currentFrameIndex], 0, 0)
    for i in range(len(app.dots)):
        drawCircle(app.dots[i][0], app.dots[i][1], 8, fill='red', border='black')
        
# def onStep(app):

def onMousePress(app, mouseX, mouseY):
    if app.counter != 4:
        app.dots.append((mouseX, mouseY))
        app.counter += 1
        
def onKeyPress(app, key):
    if key == 'n' and app.counter == 4:
        app.counter = 0
        app.allDots.extend(app.dots)
        app.dots = []
        # print(app.allDots)
        
# def algorithm(app, listDots):
#     beginning = listDots[:5] # Dots that mark the setup
    
    # for tL in range(0, len(listDots), 4)
    
    # for tR in range(1, len(listDots) - 1, 4)
    
def main():
    print('Run App is working')
    runApp(width=1920, height=1080)
    # runApp()
    


main()