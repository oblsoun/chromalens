from _testinternalcapi import get_config
from django.shortcuts import render
from django.http import StreamingHttpResponse
import yolov8

import cv2
from collections import Counter

from PIL import Image as im
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
from ultralytics.yolo.utils.torch_utils import select_device


# Create your views here.
def index(request):
    return render(request, 'webcam.html')

model = YOLO('best.pt')

def stream():
    cap = cv2.VideoCapture(0)
    colors = ['brown', 'green', 'orange', 'purple', 'red', 'yellow']
    cs = ['brown', 'green', 'orange', 'purple', 'red', 'yellow']
    cal = []
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        results = model(frame, augment=True)
        # 여기서부터
        tensor_list = results[0].boxes.data
        detection = tensor_list.tolist()
        for det in detection:
            x, y, w, h = int(det[0]), int(det[1]), int(det[2]), int(det[3])
            confidence = det[4]
            cls = det[5]
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
            cv2.putText(frame, colors[int(cls)], (x, y - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5 ,color=(255, 255, 255), thickness=2)

        # 여기 위까지
        cv2.imwrite('demo.jpg', frame)
        cv2.imshow('demo.jpg', frame)
        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')