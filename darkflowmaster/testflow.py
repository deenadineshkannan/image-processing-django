# import sys
# from darkflow.cli import cliHandler
# argv = "flow --imgdir sample_img/ --model cfg/yolo.cfg --load bin/yolov2.weights  --gpu 1.0"
# sys.argv[0] = 
# cliHandler(sys.argv)

# import sys
# import os
# from subprocess import call
# #os.chdir("darkflowmaster")
# call("flow --imgdir sample_img/ --model cfg/yolo.cfg --load bin/yolov2.weights  --gpu 1.0",shell=True)

# cliHandler(sys.argv)
from darkflow.net.build import TFNet
import cv2

options = {"model": "cfg/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)

imgcv = cv2.imread("sample_img/sample_dog.jpg")
result = tfnet.return_predict(imgcv)
print(result)
