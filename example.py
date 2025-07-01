from retico_core import *
from retico_core.debug import DebugModule
from retico_vision.vision import WebcamModule 
from retico_screen.screen import ScreenModule
from retico_screen.converter import Convert_DetectedObjectsIU_ImageIU
from retico_yolov11.yolov11 import Yolov11

webcam = WebcamModule()
yolo = Yolov11()  
converter = Convert_DetectedObjectsIU_ImageIU(num_obj_to_display=5)
screen = ScreenModule()
debug = DebugModule()  

webcam.subscribe(yolo)
yolo.subscribe(converter)
converter.subscribe(screen)

network.run(webcam)

print("Network is running")
input()

network.stop(webcam)