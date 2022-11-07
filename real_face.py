import face_recognition
import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
pyo_1 = face_recognition.load_image_file("face_data/pyo_1.jpg")
# pyo_2 = face_recognition.load_image_file("face_data/pyo_2.jpg")
# pyo_3 = face_recognition.load_image_file("face_data/pyo_3.jpg")
# pyo_4 = face_recognition.load_image_file("face_data/pyo_4.jpg")
# han_1 = face_recognition.load_image_file("face_data/han_1.jpg")
# han_2 = face_recognition.load_image_file("face_data/han_2.jpg")
han_3 = face_recognition.load_image_file("face_data/han_3.jpg")

pyo_face_encoding_1 = face_recognition.face_encodings(pyo_1)[0]
# pyo_face_encoding_2 = face_recognition.face_encodings(pyo_2)[0]
# pyo_face_encoding_3 = face_recognition.face_encodings(pyo_3)[0]
# pyo_face_encoding_4 = face_recognition.face_encodings(pyo_4)[0]

# han_face_encoding_1 = face_recognition.face_encodings(han_1)[0]
# han_face_encoding_2 = face_recognition.face_encodings(han_2)[0]
han_face_encoding_3 = face_recognition.face_encodings(han_3)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    pyo_face_encoding_1,
    # pyo_face_encoding_2,
    # pyo_face_encoding_3,
    # pyo_face_encoding_4
    han_face_encoding_3
]
known_face_names = [
    "pyo ji sung",
    # "pyo ji sung",
    # "pyo ji sung",
    # "pyo ji sung",
    "han sung goo"
    # "han sung goo"
    # "han sung goo"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
