from pyfirmata import Arduino, util
import time
import requests
import datetime
import cv2
from face_rec import Facerec

def report(content, position, name):
    url = ""
    requests.post('http://localhost/create-ticket', json={
        "content": content,
        "time": str(datetime.datetime.now()),
        "position": position,
        "name": name
    })

board_port = "/dev/tty20"

board = Arduino(board_port)

it = util.Iterator(board)

board.analog[0].enable_reporting()

it.start()

#load face rec

#test
if board.analog[0].read() != None:
    print(board.analog[0].read())
else:
    print("failed")
while True:
    data = board.analog[0].read()
    if data != None and data > 0.3:
        cap = cv2.VideoCapture(0)
        sfr = Facerec()
        sfr.load_encoding_images("faces/")
        ret, frame = cap.read()
        face_locations, face_name = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_name):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200  ), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if len(face_name) == 0:
            status = "Unidentified"
        else:
            status = face_name
        time.sleep(5)
        cv2.destroyAllWindows()

        content = ""
        position = ""
        report(content, position, status)
        print(data)
    else:
        continue
    time.sleep(1)
