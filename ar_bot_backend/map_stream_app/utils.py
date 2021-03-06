import cv2
import os
from threading import Thread
import time

import sys
import pathlib

from map_to_pic.map_to_pic import MapToPic, rclpy
        
def get_image(static_folder,name): 
    load_path =  os.path.join(pathlib.Path(__file__).parent.parent,"static",static_folder,name)
    return load_path

class MapStreamManager():
    def __init__(self):
        self.load = cv2.imread(get_image("images","lazy-load.jpg"))
        self.rate = 10
        self.m_t_p = MapToPic(0.3)
        self.ros_th = Thread(target = self.start_node, args=(self.m_t_p, )).start()
        self.map_shape = [0,0]
        
    def start_node(self, node):
        rclpy.spin(node)

    def get_map_stream(self):
        last_time = time.time()
        try:
            while True:
                while (1/(time.time()-last_time) > self.rate):
                    time.sleep(0.001)
                map_ = self.m_t_p.get_map()
                if isinstance(map_, bool):
                    map_ = self.load
                self.map_shape = list(map_.shape[:-1])
                ret, buffer = cv2.imencode('.jpg', map_)
                frame = buffer.tobytes()
                last_time = time.time()
                yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except KeyboardInterrupt:
            self.ros_th.join()

    def save_map(self):
        self.m_t_p.save_map()
    
    def get_resolution(self):
        return self.m_t_p.get_map_resolution()
    
    def get_origin(self):
        return self.m_t_p.get_map_origin()

    def get_frames_cam(self):
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                frame = cv2.resize(frame,(320,240))
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

rclpy.init()
map_stream_manager = MapStreamManager()
        