# 201835541 표지성
# 201835542 한성구

from djitellopy import Tello
import time
import cv2
from threading import Thread
from datetime import datetime

import pose
import pose_clear

import face_recognition
import cv2
import numpy as np

keepRecording = True
recorder = 0
path_name = ""
file_name = ""

han1 = None
han2 = None
han_face_encoding_1 = None
han_face_encoding_2 = None
known_face_encodings = None
known_face_names = None
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


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
    file_name = now.strftime('%Y-%m-%d-%H-%M-%S')  # 2021-12-22-15-46-26

    han_1 = face_recognition.load_image_file(
        "/Users/pyojisung/Documents/GitHub/2022-Drones-and-Robotics-RunningMate/face_data/han_3.jpg")

    han_2 = face_recognition.load_image_file(
        "/Users/pyojisung/Documents/GitHub/2022-Drones-and-Robotics-RunningMate/face_data/han_4.jpg")

    han_face_encoding_1 = face_recognition.face_encodings(han_1)[0]
    han_face_encoding_2 = face_recognition.face_encodings(han_2)[0]

    known_face_encodings = [
        han_face_encoding_1,
        han_face_encoding_2
    ]
    known_face_names = [
        "han sung goo",
        "han sung goo"
    ]

    # video_path = '../pose_input/2022-11-05/11_5.mov'
    video_path = '../pose_input/' + path_name + "/" + file_name + ".avi"

    # out_path = '../pose_output/video/2022-11-05/11_5.avi'
    out_path = '../pose_output/video/' + path_name + "/" + file_name + ".avi"

    # csv_path = '../pose_output/csv/2022-11-05/11_5.csv'
    csv_path = '../pose_output/csv/' + path_name + "/" + file_name + ".csv"

    # clear_out_path = '../pose_output/clear_video/2022-11-05/11_5.mp4'
    clear_out_path = '../pose_output/clear_video/' + path_name + "/" + file_name + ".mp4"

    print(path_name)
    print(file_name)
    myDrone = initTello()
    myDrone.takeoff()
    myDrone.move_up(70)
    time.sleep(1)
    myDrone.streamon()
    cv2.namedWindow("drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)

    while True:
        img = frame_read.frame
        cv2.imshow("drone", img)

        if process_this_frame:
            small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                print(str(matches) + " " + str(matches[0]) + " " + str(matches[1]))
                # name = "Unknown"

                if (matches[0] == True & matches[1] == True):
                    myDrone.flip_right()
                    process_this_frame = not process_this_frame
                    break
                else:
                    myDrone.flip_left()

                # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #     name = known_face_names[best_match_index]
                #
                # face_names.append(name)

        # Todo : 이 부분에서 찍기 위한 드론의 위치로 옮기기

        keyboard = cv2.waitKey(1) & 0xFF

        if keyboard == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            keepRecording = False
            break

        if keyboard == ord('w'):
            myDrone.move_forward(20)

        if keyboard == ord('s'):
            myDrone.move_back(20)

        if keyboard == ord('a'):
            myDrone.move_left(20)

        if keyboard == ord('d'):
            myDrone.move_right(20)

        if keyboard == ord('g'):
            myDrone.move_up(10)

        if keyboard == ord('h'):
            myDrone.move_down(10)

        if keyboard == ord('v'):
            if recorder == 0:
                recorder = Thread(target=videoRecorder)
                recorder.start()

    pose.pose(video_path, out_path, csv_path)
    pose_clear.clear_pose(video_path, clear_out_path, csv_path)

    exit(0)
    recorder.join()
