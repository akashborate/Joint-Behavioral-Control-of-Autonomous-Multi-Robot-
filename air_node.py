
#include <std_msgs/Empty.h>

int main(int argc, char **argv){

init(argc, argv, "takeoff_fly");
Nodehandle n;
std_msg::Empty myMsg;
Publisher takeOff=n.advertise<std_msgs::Empty>("/ardrone/takeoff",1);
takeOff.publish(myMsg);
spinOnce();

return 0;
}


Publisher takeOff=n.advertise<std_msgs::Empty>("/ardrone/takeoff",1,true);



system( "rostopic pub /ardrone/land std_msgs/Empty");



air drone stuff

rostopic pub /ardrone/takeoff std_msgs/Empty

rostopic pub /ardrone/land std_msgs/Empty 




#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math

from geometry_msgs.msg import Twist
from std_msgs.msg import String

class air_node:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        #self.speed = 0.2
        #self.msg = Twist()

        # publish to ardrone/takeoff , subscribe to speech output
        self.pub_ = rospy.Publisher('ardrone/takeoff', String )
        rospy.Subscriber('recognizer/output', String, self.speechCb)

        r = rospy.Rate(10.0)
        while not rospy.is_shutdown():
            self.pub_.publish(self.msg)
            r.sleep()
        
    def speechCb(self, msg):
        rospy.loginfo(msg.data)

       

        if msg.data.find("forward") > -1:    
           self.pub_.publish(Empty)

        #elif msg.data.find("stop") > -1 or msg.data.find("halt") > -1:          
		#self.pub_.publish(Empty) 
            

#self.msg = String()
        
 #       self.pub_.publish(self.msg)

  #  def cleanup(self):
        # stop the robot!
   #     twist = Twist()
    #    self.pub_.publish(twist)

if __name__=="__main__":
    rospy.init_node('air_node')
    try:
        voice_cmd_vel()
    except:
        pass

