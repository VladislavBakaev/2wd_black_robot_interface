import os
from threading import Thread

import sys
import pathlib
import json

from web_socket_control_app.action_feedback_node import ActionFeedback
from cmd_vel_joy.cmd_vel_node import CmdVelPublisher, rclpy

def update_vel(vel):
    vel = json.loads(vel)
    vel = json.loads(vel['value'])
    cmd_vel_pub.publish_vel(vel)

class ActionFeedbackManager():
    def __init__(self):
        self.a_f = ActionFeedback()
        self.rate = 1
        self.ros_th = Thread(target = self.start_node, args=(self.a_f, )).start()
    
    def start_node(self, node):
        rclpy.spin(node)
    
    def get_feedback(self):
        return self.a_f.data

rclpy.init()
cmd_vel_pub = CmdVelPublisher()
action_feedback_manager = ActionFeedbackManager() 