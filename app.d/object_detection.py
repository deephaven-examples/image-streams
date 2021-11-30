import os
import numpy
import pandas as pd
import cv2
import tensorflow as tf
import tensorflow_hub as hub

# Carregar modelos
# https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1
# https://towardsdatascience.com/object-detection-with-tensorflow-model-and-opencv-d839f3e42849

detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
# detector = hub.load("/object_detection/efficientdet_lite2_detection_1.tar.gz")
# labels = pd.read_csv('/object_detection/labels.csv',sep=';',index_col='ID')['OBJECT (2017 REL.)']
labels = pd.read_csv("https://raw.githubusercontent.com/gabrielcassimiro17/raspberry-pi-tensorflow/main/labels.csv",sep=';',index_col='ID')['OBJECT (2017 REL.)']

def image_file_name(file:str, image_name) -> str:
    file_base = os.path.splitext(file)[0]
    dir, fname = os.path.split(file_base)
    dir = os.path.join(os.path.split(dir)[0], "identified_objects")
    os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, f"{fname}_{image_name}.jpg")


def analyze_image(file:str, min_score:float=0.5) -> tuple:
    #Load the image
    img = cv2.imread(file)
    
    #Resize to respect the input_shape
    # width = 512
    # height = 512
    # inp = cv2.resize(img, (width , height ))

    inp = img

    #Convert img to RGB
    rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)

    #Is optional but i recommend (float convertion and convert img to tensor image)
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

    #Add dims to rgb_tensor
    rgb_tensor = tf.expand_dims(rgb_tensor , 0)
    
    boxes, scores, classes, num_detections = detector(rgb_tensor)
    
    pred_labels = [labels[i] for i in classes.numpy().astype('int')[0]]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]
   
    #loop throughout the detections and place a box around it
    out_scores = []
    out_labels = []
    out_files = []
    count = 0

    for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < min_score:
            continue
            
        # cropped_image = img[ymin:ymax, xmin:xmax]
        cropped_image = inp[ymin:ymax, xmin:xmax]
        cropped_file = image_file_name(file, count)
        cv2.imwrite(cropped_file, cropped_image)

        out_scores.append(score)
        out_labels.append(label)
        out_files.append(cropped_file)
        count += 1

    return (jpy.array("double", out_scores), jpy.array("java.lang.String", out_labels), jpy.array("java.lang.String", out_files))


#TODO: Jianfeng fix indexing so this isn't needed or pull the latest image

get_contents = lambda contents, i: contents[i]

detected_images = file_events \
    .where("Type = `created`", "!IsDir") \
    .view("Timestamp", "SourceImage = Path") \
    .update(
        "Contents = analyze_image(SourceImage)", 
        "Score = (double[]) get_contents(Contents,0)", 
        "Label = (String[]) get_contents(Contents,1)", 
        "ObjectImage = (String[]) get_contents(Contents,2)"
        ) \
    .dropColumns("Contents") \
    .ungroup()
