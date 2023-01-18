import cv2 as c 
import time
from emailing import send_email
import glob
import os
from threading import Thread

video = c.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list=[]
count= 1

def clean_folder():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)
        
while True:
    status=0
    check, frame = video.read()

    gray_fram = c.cvtColor(frame, c.COLOR_BGR2GRAY)
    gray_fram_GAU = c.GaussianBlur(gray_fram, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_fram_GAU

    delta_frame = c.absdiff(first_frame, gray_fram_GAU)
    thresh_frame = c.threshold(delta_frame, 100, 500, c.THRESH_BINARY)[1]
    dil_frame = c.dilate(thresh_frame, None, iterations=2)
    c.imshow("My video", dil_frame)

    contours, check = c.findContours(dil_frame, c.RETR_EXTERNAL, c.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if c.contourArea(contour) < 10000:
            continue
        x, y, w, h = c.boundingRect(contour)
        rectangle=c.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status=1
            c.imwrite(f"images/{count}.png",frame)
            count+=1
            all_images=glob.glob("images/*.png")
            index=int(len(all_images)/2)
            image_with_object=all_images[index]

    status_list.append(status)
    status_list=status_list[-2:]

    if status_list[0]==1 and status_list[1]==0:
        email_thread=Thread(target=send_email,args=(image_with_object, ))
        email_thread.daemon=True
        clean_thread=Thread(target=clean_folder)
        email_thread.daemon=True
        email_thread.start()

    c.imshow("Video", frame)
    key = c.waitKey(1)

    if key == ord("q"):
        break

video.release()
clean_thread.start()
