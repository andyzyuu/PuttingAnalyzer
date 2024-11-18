#Citation: https://www.youtube.com/watch?v=Jvf5y21ZqtQ&list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq&ab_channel=sentdex partially inspired lines 
import cv2

# cap = cv2.VideoCapture('defaultStroke.mov')
cap = cv2.VideoCapture(0)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_size = (width, height)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 30.0, frame_size)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, frame_size)



recording = False
recorded = False

if not cap.isOpened():
    print("Error, couldn't open file or camera")
    exit()

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('Live Video', frame)

    keyPress = cv2.waitKey(1) & 0xFF 
    if keyPress == ord('s') and not recording:
        print('Recording started')
        # out = cv2.VideoWriter('output.mp4', fourcc, 20.0, frame_size)
        recording = True
        
    if recording == True:

        out.write(frame)
        cv2.putText(frame, "Recording...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # cv2.imshow('Recording...', frame)
        
    if keyPress == ord('e') and recording:
        print('Recording ended')
        recording = False
        recorded = True
        out.release()
        out = None
        cap_recording = cv2.VideoCapture('output.mp4')
        # print(cap.isOpened())
    
    if keyPress == ord('r') and recorded:
        print('Replaying recording')
        while (cap_recording.isOpened()):
            ret, frame = cap_recording.read()
            cv2.imshow('Replay', frame)
        
    # if recording == False:
    #     cv2.imshow('Not Recording', frame)
        # replay_cap = cv2.VideoCapture('output.mp4')
        
        
            # print('!!!!!')
            # if not out:
            #     cap.release()
            #     if not replay_cap.isOpened(): 
            #         print('Error: Could not open recorded video file for replay')
            #         cap = cv2.VideoCapture(0)  
            #         continue
            #     while replay_cap.isOpened():
            #         ret, frame = replay_cap.read()
            #         print('!!!')
            #         cv2.imshow('Recorded', frame)
        # if out:
        #     out.release()
        #     out = None
    if keyPress == ord('q'):
        break
    
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)