from ultralytics import YOLO
import cv2
from collections import Counter

def counter(classes):
     counts = dict(Counter(classes))
     duplicates = {key:value for key, value in counts.items() if value > 1}
     return duplicates

def dict_to_str(dic):
    count_products = list(dic.items())
    print(count_products)
    products = []
    for item in count_products:
        x = ' : '.join(map(str, item))
        products.append(x)
    products = '\n'.join(products)
    return products

def colordetection(image_path):
    image = cv2.imread(image_path)
    colors = ['brown', 'green', 'orange', 'purple', 'red', 'yellow']
    cs = ['brown', 'green', 'orange', 'purple', 'red', 'yellow']
    cal = []

    try:
        model = YOLO('best.pt')  # model path
        results = model.predict(source = image_path, imgsz=640, conf=0.3)  # predict on an image
        tensor_list = results[0].boxes.data
        detection = tensor_list.tolist()
        total_product_count =  len(detection)
        print("Found Products:", total_product_count)
        if len(detection) == 0:
            print("Detected 0 Products")
            return "Unknow","Found 0"
        else:
            for det in detection:
                x,y,w,h = int(det[0]),int(det[1]),int(det[2]),int(det[3])
                confidence = det[4]
                cls = det[5]
                cal.append(str(colors[int(cls)]))
                img = cv2.rectangle(image,(x,y),(w,h),(255,255,102),2)
                cv2.putText(img, colors[int(cls)], (x,y-10), fontFace = cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.3, color=(160,160,160), thickness=1)
                
            count_products = counter(cal)
            print(count_products)
            products = dict_to_str(count_products)
            cv2.imwrite(image_path, img)
            return products, total_product_count
    except Exception as e:
        print(e)
        return "ERORR","Unknown"


def colordetection_org(image_path):
    org_img = cv2.imread(image_path)
    return org_img