from utils import *
import time
import cv2

if __name__ == "__main__":
    myDrone = initTello()
    myDrone.takeoff()
    time.sleep(1)
    myDrone.streamon()
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)

    while True:
        img = frame_read.frame
        cv2.imshow("drone", img)
        keyboard = cv2.waitKey(1)
        print(keyboard)
        if keyboard & 0xFF == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            exit(0)
            break
        if keyboard == ord('w'):
            myDrone.move_forward(20)
        if keyboard == ord('s'):
            myDrone.move_back(20)
        if keyboard == ord('a'):
            myDrone.move_left(20)
        if keyboard == ord('d'):
            myDrone.move_right(20)
