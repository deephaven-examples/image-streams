#pip3 install opencv-python
#Run from the terminal in Mac

import sys
import os
import cv2
import time

if len(sys.argv) != 3:
    print("Usage: <video_capture_source_number> <sleep_sec>")
    sys.exit(1)

video_source = int(sys.argv[1])
sleep_sec = int(sys.argv[2])

outdir = "./data/images/"

if not os.path.exists(outdir):
    os.makedirs(outdir)

# video capture source.  video_source=0 is usually the main webcam.
webcam = cv2.VideoCapture(video_source)
print(f"WEBCAM: {webcam}")

try:
    while(True):
        # Get an image from the webcam
        ret, frame = webcam.read()

        if ret:
            time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            f = f"{outdir}/image-{time_str}.png"
            print(f"WRITING IMAGE: {f}")
            cv2.imwrite(f, frame)
        else:
            print("NO FRAME RETURNED")
        time.sleep(sleep_sec)
except KeyboardInterrupt:
    print("CAMERA: SHUTDOWN")
    cv2.destroyAllWindows()
    webcam.release()