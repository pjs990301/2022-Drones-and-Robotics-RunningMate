#201835541 표지성
#201835542 한성구

from djitellopy import Tello
import time
import cv2
from threading import Thread

keepRecording = True
recorder = 0

def initTello():
    myDrone = Tello()

    # drone connection
    myDrone.connect()

    # set all speed to 0
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0

    print("\n * Drone battery percentage : " + str(myDrone.get_battery()) + "%")
    myDrone.streamoff()

    return myDrone

def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

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
        if keyboard & 0xFF == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            keepRecording = False
            recorder.join()
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
        if keyboard == ord('v'):
            if recorder == 0:
                recorder = Thread(target=videoRecorder)
                recorder.start()