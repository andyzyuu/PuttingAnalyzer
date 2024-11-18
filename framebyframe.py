import cv2 
cap = cv2.VideoCapture('defaultStroke.mov')

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
current_frame = 0
while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    ret, frame = cap.read()
    if not ret:
        print('Video ends')
        break
    # file_name = str(frameNum) + '.jpg'
    # file_name = f'{frameNum}.jpg'
    # cv2.imwrite(file_name, frame)
    # cv2.imshow('Frame', cv2.imread(file_name))
    cv2.imshow('Frame', frame)
    while True:
        keyPress = cv2.waitKey(0) & 0xFF 
        if ret and keyPress == ord('n'):
            print('Next frame')
            current_frame = min(current_frame + 5, frame_count - 1)
        
            # frameNum += 1
            break
        # cv2.imshow('Frame', cv2.imread(file_name))
        elif ret and keyPress == ord('b'):
            print('Previous frame')
            current_frame = max(current_frame - 5, 0)
            # frameNum -= 1
            break
        elif keyPress == ord('q'):
            print('Exited')
            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            exit()
            break
    # else:
    #     break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)