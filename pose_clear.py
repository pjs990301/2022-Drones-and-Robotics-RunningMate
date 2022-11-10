# import the libraries
from scipy import signal
import pandas as pd
import numpy as np
import math
import progressbar
import cv2, os
import scipy
import csv
from datetime import datetime


def angle_between(p1, p2):  # 두점 사이의 각도:(getAngle3P 계산용) 시계 방향으로 계산한다. P1-(0,0)-P2의 각도를 시계방향으로
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    res = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    return res


def getAngle3P(p1, p2, p3, direction="CW"):  # 세점 사이의 각도 1->2->3
    pt1 = (int(p1[0]) - int(p2[0]), int(p1[1]) - int(p2[1]))
    pt2 = (int(p3[0]) - int(p2[0]), int(p3[1]) - int(p2[1]))
    res = angle_between(pt1, pt2)
    res = (res + 360) % 360
    if direction == "CCW":  # 반시계방향
        res = (360 - res) % 360
    return res


def angle(x1, y1, x2, y2, x3, y3):
    return math.atan((y2 - y1) / (x2 - x1)) - math.atan((y3 - y1) / (x3 - x1)) * 180 / math.pi


circle_color, line_color = (0, 255, 255), (0, 255, 0)
window_length, polyorder = 11, 2

now = datetime.now()
# path_name = now.strftime('%Y-%m-%d')  # 2021-12-22
file_name = now.strftime('%Y-%m-%d-%H-%M-%S')  # 2021-12-22-15-46-26

# video_path = 'pose_input/2022-11-06.mp4'
video_path = 'pose_input/2022-11-10/2022-11-10-19-58-41.mp4'
out_path = 'pose_output/clear_video/2022-11-10/2022-11-10-19-58-41.mp4'
csv_path = 'pose_output/csv/2022-11-10/2022-11-10-19-58-41.csv'

df = pd.read_csv(csv_path)

for i in range(30):
    df[str(i)] = signal.savgol_filter(df[str(i)], window_length, polyorder)

cleaned_points = []

for i in range(df.shape[0]):
    row = np.array(df.values[i], int)
    points = list(zip(row[:15], row[15:]))

    if points[2][0] > points[5][0]:
        # temp = points[2]
        # points[2] = points[5]
        # points[5] = temp

        temp = points[3]
        points[3] = points[6]
        points[6] = temp

        temp = points[4]
        points[4] = points[7]
        points[7] = temp

        temp = points[2]
        points[2] = points[5]
        points[5] = temp

        temp = points[8]
        points[8] = points[11]
        points[11] = temp

        temp = points[9]
        points[9] = points[12]
        points[12] = temp

        temp = points[10]
        points[10] = points[13]
        points[13] = temp

    cleaned_points.append(points)

cap = cv2.VideoCapture(video_path)
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
ok, frame = cap.read()
(frameHeight, frameWidth) = frame.shape[:2]
h = 500
w = int((h / frameHeight) * frameWidth)

# Define the output
output = cv2.VideoWriter(out_path, 0, fps, (w, h))
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
writer = None
(f_h, f_w) = (h, w)
zeros = None

# There are 15 points in the skeleton
pairs = [[0, 1],  # head
         [1, 2], [1, 5],  # sholders
         [2, 3], [3, 4], [5, 6], [6, 7],  # arms
         [1, 14], [14, 11], [14, 8],  # hips
         [8, 9], [9, 10], [11, 12], [12, 13]]  # legs

frame_number = 0

while True:
    ok, frame = cap.read()

    if ok != True:
        break

    frame = cv2.resize(frame, (w, h), cv2.INTER_AREA)
    frame_copy = np.copy(frame)

    points = cleaned_points[frame_number]
    for i in range(len(points)):
        xy = tuple(np.array([points[i][0], points[i][1]], int))
        # print(str(frame_number) + " " + str(i) + " " + str(xy))
        # print(str(frame_number) + " " + str(i) + " " + str(xy[0]) + " " + str(xy[1]))
        cv2.circle(frame_copy, xy, 2, circle_color, -1)

    for pair in pairs:
        partA = pair[0]
        partB = pair[1]
        cv2.line(frame_copy, points[partA], points[partB], line_color, 1, lineType=cv2.LINE_AA)

    if writer is None:
        writer = cv2.VideoWriter(out_path, fourcc, fps,
                                 (f_w, f_h), True)
        zeros = np.zeros((f_h, f_w), dtype="uint8")

    writer.write(cv2.resize(frame_copy, (f_w, f_h)))

    cv2.imshow('frame', frame_copy)

    # 무릎 각도
    point8 = None
    point9 = None
    point10 = None
    point11 = None
    point12 = None
    point13 = None

    # 팔꿈치 각도
    point2 = None
    point3 = None
    point4 = None
    point5 = None
    point6 = None
    point7 = None

    # 몸통 각도
    point1 = None
    point0 = None
    point14 = None

    for i in range(len(points)):
        xy = tuple(np.array([points[i][0], points[i][1]], int))
        # print(str(frame_number) + " " + str(i) + " " + str(xy))
        # print(str(frame_number) + " " + str(i) + " " + str(xy[0]) + " " + str(xy[1]))

        if i == 8:
            point8 = (xy[0], xy[1])

        elif i == 9:
            point9 = (xy[0], xy[1])

        elif i == 10:
            point10 = (xy[0], xy[1])

        elif i == 11:
            point11 = (xy[0], xy[1])

        elif i == 12:
            point12 = (xy[0], xy[1])

        elif i == 13:
            point13 = (xy[0], xy[1])

        elif i == 2:
            point2 = (xy[0], xy[1])

        elif i == 3:
            point3 = (xy[0], xy[1])

        elif i == 4:
            point4 = (xy[0], xy[1])

        elif i == 5:
            point5 = (xy[0], xy[1])

        elif i == 6:
            point6 = (xy[0], xy[1])

        elif i == 7:
            point7 = (xy[0], xy[1])

        elif i == 1:
            point1 = (xy[0], xy[1])

        elif i == 0:
            point0 = (xy[0], xy[1])

        elif i == 14:
            point14 = (xy[0], xy[1])

    # print(angle(point12[0], point12[1], point11[0], point11[1], point13[0], point13[1]))
    img_path = 'pose_output/img/' + "2022-11-10" + "/" + file_name + "-" + str(frame_number) + ".jpg"

    # fontColor
    blue = (255, 0, 0)
    black = (0, 0, 0)
    red = (0, 0, 255)
    white = (255, 255, 255)

    # font
    font = cv2.FONT_HERSHEY_COMPLEX
    check = [0, 0, 0, 0, 0]

    # 무릎 각도
    if not ((150 < getAngle3P(point11, point12, point13, "CW") < 160) or (200 < getAngle3P(point11, point12, point13,
                                                                                           "CCW") < 210)):
        check[0] = 1
        cv2.circle(frame_copy, point11, 2, red, -1)
        cv2.circle(frame_copy, point12, 2, red, -1)
        cv2.circle(frame_copy, point13, 2, red, -1)

    if not ((150 < getAngle3P(point8, point9, point10, "CW") < 160) or (200 < getAngle3P(point8, point9, point10,
                                                                                         "CCW") < 210)):
        check[1] = 1
        cv2.circle(frame_copy, point8, 2, red, -1)
        cv2.circle(frame_copy, point9, 2, red, -1)
        cv2.circle(frame_copy, point10, 2, red, -1)

    # 몸통 각도
    if not ((160 < getAngle3P(point0, point1, point14, "CW") < 180) or (180 < getAngle3P(point0, point1, point14,
                                                                                         "CCW") < 200)):
        check[2] = 1
        cv2.circle(frame_copy, point0, 2, red, -1)
        cv2.circle(frame_copy, point1, 2, red, -1)
        cv2.circle(frame_copy, point14, 2, red, -1)

    # 팔꿈치 각도
    if not ((260 < getAngle3P(point5, point6, point7, "CW") < 280) or (80 < getAngle3P(point5, point6, point7,
                                                                                       "CCW") < 100)):
        check[3] = 1
        cv2.circle(frame_copy, point5, 2, red, -1)
        cv2.circle(frame_copy, point6, 2, red, -1)
        cv2.circle(frame_copy, point7, 2, red, -1)

    if not ((260 < getAngle3P(point2, point3, point4, "CW") < 280) or (80 < getAngle3P(point2, point3, point4,
                                                                                       "CCW") < 100)):
        check[4] = 1
        cv2.circle(frame_copy, point2, 2, red, -1)
        cv2.circle(frame_copy, point3, 2, red, -1)
        cv2.circle(frame_copy, point4, 2, red, -1)

    print(check)
    count = 0
    for num in range(len(check)):
        count += check[num]

    # print(count)
    message = ""
    for i in range(len(check)):
        if count > 3:
            # print(str(i) + " " + str(check[i]))

            if i == 0 and check[i] == 1:
                message += "Left knee angle\n"

            if i == 1 and check[i] == 1:
                message += "Right knee angle\n"

            if i == 2 and check[i] == 1:
                message += "body (waist) angle\n"

            if i == 3 and check[i] == 1:
                message += "Left elbow angle\n"

            if i == 4 and check[i] == 1:
                message += "Right elbow angle"

    # print(message)

    y0, dy = 30, 20
    for i, line in enumerate(message.split('\n')):
        y = y0 + i * dy
        frame_copy = cv2.putText(frame_copy, line, (500, y), font, 0.5, blue, 1, cv2.LINE_AA)

    cv2.imwrite(img_path, frame_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    frame_number += 1

cap.release()
cv2.destroyAllWindows()
