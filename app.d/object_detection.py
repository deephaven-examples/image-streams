import os
import numpy
import pandas as pd
import jpy
import cv2
import tensorflow as tf
import tensorflow_hub as hub

# Load the object detection model and labels.  For more details see:
# https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1
# https://towardsdatascience.com/object-detection-with-tensorflow-model-and-opencv-d839f3e42849

detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
labels = pd.read_csv("https://raw.githubusercontent.com/gabrielcassimiro17/raspberry-pi-tensorflow/main/labels.csv", sep=';', index_col='ID')['OBJECT (2017 REL.)']

def identified_object_file(file:str, object_name) -> str:
    """ Gets the path to write detected object images to. """
    file_base = os.path.splitext(file)[0]
    dir, fname = os.path.split(file_base)
    dir = os.path.join(os.path.split(dir)[0], "identified_objects")
    os.makedirs(dir, exist_ok=True)
    return os.path.join(dir, f"{fname}_{object_name}.jpg")


def analyze_image(file:str, min_score:float=0.1) -> tuple:
    """ Load an image, identify objects in the image, save cropped images of the 
    detected objects, and return information describing the identified objects. """

    # Load the image and convert it to a tensor usable by the object detector
    img = cv2.imread(file)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)
    input_tensor = tf.expand_dims(rgb_tensor , 0)
    
    # Perform object detection on the image
    boxes, scores, classes, num_detections = detector(input_tensor)
    
    pred_labels = [labels[i] for i in classes.numpy().astype('int')[0]]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]
   
    # Process the identified objects.  Cropped images are saved for the identified objects.
    out_scores = []
    out_labels = []
    out_files = []
    count = 0

    for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < min_score:
            continue
            
        cropped_image = img[ymin:ymax, xmin:xmax]
        cropped_file = identified_object_file(file, count)
        cv2.imwrite(cropped_file, cropped_image)

        out_scores.append(score)
        out_labels.append(label)
        out_files.append(cropped_file)
        count += 1

    # Pack the values into Java arrays so that the data can be ungrouped
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
