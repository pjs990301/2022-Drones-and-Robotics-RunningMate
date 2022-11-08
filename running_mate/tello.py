# 201835541 표지성
# 201835542 한성구

from djitellopy import Tello
import time
import cv2
from threading import Thread
from datetime import datetime

import pose
import pose_clear

keepRecording = True
recorder = 0
path_name = ""
file_name = ""
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
    path = "../pose_input/" + path_name + "/" + file_name + ".avi"
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


if __name__ == "__main__":
    now = datetime.now()
    path_name = now.strftime('%Y-%m-%d')  # 2021-12-22
    file_name = now.strftime('%Y-%m-%d-%H:%M:%S')  # 2021-12-22-15:46:26
    print(path_name)
    print(file_name)
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
            exit(0)
            recorder.join()
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

    # video_path = '../pose_input/2022-11-05/11_5.mov'
    video_path = '../pose_input/' + path_name + "/" + file_name + ".avi"

    # out_path = '../pose_output/video/2022-11-05/11_5.avi'
    out_path = '../pose_output/video/' + path_name + "/" + file_name + ".avi"

    # csv_path = '../pose_output/csv/2022-11-05/11_5.csv'
    csv_path = '../pose_output/csv/' + path_name + "/" + file_name + ".csv"

    # clear_out_path = '../pose_output/clear_video/2022-11-05/11_5.mp4'
    clear_out_path = '../pose_output/clear_video/' + path_name + "/" + file_name + ".mp4"

    pose.pose(video_path, out_path, csv_path)
    pose_clear.clear_pose(video_path, clear_out_path, csv_path)
