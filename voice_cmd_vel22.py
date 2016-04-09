#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy
import math
from drone_controller import BasicDroneController

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Empty       	 # for land/takeoff/emergency


class voice_cmd_vel:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.speed = 0.2*0.2
        self.msg = Twist()

        # publish to cmd_vel, subscribe to speech output
        self.pub_ = rospy.Publisher('cmd_vel', Twist)
        rospy.Subscriber('recognizer/output', String, self.speechCb)

        r = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            self.pub_.publish(self.msg)
            r.sleep()
        
    def speechCb(self, msg):
        rospy.loginfo(msg.data)

	if msg.data.find("full speed") > -1:
		self.pubTakeoff = rospy.Publisher('/ardrone/takeoff',Empty)
		self.pubTakeoff.publish(Empty())

	if msg.data.find("half speed") > -1:
		self.pubLand    = rospy.Publisher('/ardrone/land',Empty)
		self.pubLand.publish(Empty())


        #if msg.data.find("full speed") > -1:
         #   if self.speed == 0.2:
          #      self.msg.linear.x = self.msg.linear.x*2
           #     self.msg.angular.z = self.msg.angular.z*2
            #    self.speed = 0.4
       # if msg.data.find("half speed") > -1:
        #    if self.speed == 0.4:
         #       self.msg.linear.x = self.msg.linear.x/2
          #      self.msg.angular.z = self.msg.angular.z/2
           #     self.speed = 0.2

        if msg.data.find("forward") > -1:    
            self.msg.linear.x = self.speed
            self.msg.angular.z = 0
        elif msg.data.find("left") > -1:
            self.msg.linear.x = self.speed*0.5
            self.msg.linear.y = self.speed*0.5
                    
            
        elif msg.data.find("right") > -1:    
            self.msg.linear.x = self.speed*0.5
            self.msg.linear.y = -self.speed*0.5

        elif msg.data.find("back") > -1:
            self.msg.linear.x = -self.speed
            self.msg.angular.z = 0
        elif msg.data.find("stop") > -1 or msg.data.find("halt") > -1:          
            self.msg = Twist()
        
        self.pub_.publish(self.msg)

    def cleanup(self):
        # stop the robot!
        twist = Twist()
        self.pub_.publish(twist)

if __name__=="__main__":
    rospy.init_node('voice_cmd_vel')
    try:
        voice_cmd_vel()
    except:
        pass

