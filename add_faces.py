import cv2
import pickle
import numpy as np
import os


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0


name = input("Enter Your Name: ").strip()

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = gray[y:y+h, x:x+w]  
        resized_img = cv2.resize(crop_img, (50, 87))  

        if len(faces_data) < 100 and i % 10 == 0:
            faces_data.append(resized_img)

        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()


faces_data = np.asarray(faces_data)  # Shape: (100, 50, 87)
faces_data = faces_data.reshape(len(faces_data), -1)  # flatten to (100, 4350)


if not os.path.exists('data'):
    os.makedirs('data')


if os.path.exists('data/names.pkl'):
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
else:
    names = []

names.extend([name] * len(faces_data))  

with open('data/names.pkl', 'wb') as f:
    pickle.dump(names, f)


if os.path.exists('data/faces_data.pkl'):
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)

    if faces.shape[1] != faces_data.shape[1]:  
        print(f"Error: Dimension mismatch! Existing data: {faces.shape[1]}, New data: {faces_data.shape[1]}")
        exit()

    faces = np.append(faces, faces_data, axis=0)  
else:
    faces = faces_data  

with open('data/faces_data.pkl', 'wb') as f:
    pickle.dump(faces, f)

print(f"Successfully saved {len(faces_data)} images for {name}!")
