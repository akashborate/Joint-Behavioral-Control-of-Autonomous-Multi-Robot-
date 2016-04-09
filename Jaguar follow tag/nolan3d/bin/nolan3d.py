#!/usr/bin/env python
import roslib; roslib.load_manifest('nolan3d')
import rospy
 
#from ar_recog.msg import Tag, Tags
from ar_recog.msg import Tags
from ar_recog.msg import Tag

#Getting data from jaguar
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from time import time
 
class Delta:
	def __init__(self):
		self.old_value = 0
		self.old_time = 0
		self.old_vel = 0
 
	def get_velocity(self, new_value):
		new_time = time()
 
		# velocity = distance / time
		vel = (new_value - self.old_value) / (new_time - self.old_time)
 
		# smooth velocity
		self.old_vel = self.old_vel + (vel - self.old_vel) * 0.1
 
		# save values for next time
		self.old_time = new_time
		self.old_value = new_value
 
		return self.old_vel
 
distance = Delta()
yRot = Delta()

#Determining height and width from ar_recog tags
def handleTags(msg):
	global pub
	global lastDir
	global lastSeen
 
	width = msg.image_width
	height = msg.image_height
 	
	biggest = Tag()
	for tag in msg.tags:
		if (tag.diameter > biggest.diameter):
			biggest = tag
		
#To only rotate when tag not detected
	if biggest.diameter == 0:
		twist = Twist()
		twist.linear.x = 0
		if (time() - lastSeen > .5):
			twist.angular.z = .75*lastDir
		pub.publish(twist)
		print twist
 
		# reset velocity and distance
		distance.get_velocity(0)
		yRot.get_velocity(0)
		return
 
	lastSeen = time()

#Determines the co-ordinates of corners in the ar_image square
	cx = 0; cy = 0
	for i in [0,2,4,6]:
		cx = cx + biggest.cwCorners[i]
		cy = cy + biggest.cwCorners[i+1]
	cx = cx / 4. / width
	cy = cy / 4. / height

 
	twist = Twist()
 
	# move foward and backward, trying to stop at stopping_dist
	stopping_dist = 2000.
	dist = (biggest.distance - stopping_dist) / stopping_dist
	print biggest.distance
	print dist
	dist_vel = distance.get_velocity(dist)
	if abs(dist) < 0.25:
		# if we are close enough to the stopping distance, just try to stop
		twist.linear.x = dist_vel * 0.5
		twist.angular.z = 0
	else:
		# otherwise try to move within stopping_dist
		twist.linear.x = dist * 0.5
		twist.angular.z = 0
	print twist.linear.x

	pub.publish(twist)
		twist.angular.z = (-(cx - .5)/.25)

	#Keep itself from the tag at certain distance
	if (twist.angular.z < 0):
		lastDir = -1
		twist.linear.x =0.35
		if (biggest.diameter>120):
			twist.linear.x=-0.35
		if (biggest.diameter<120 and biggest.diameter>100):
			twist.linear.x=0
	else:
		lastDir = 1
		twist.linear.x =0.35
		if (biggest.diameter>120):
			twist.linear.x=-0.35
		if (biggest.diameter<120 and biggest.diameter>100):
			twist.linear.x=0
	pub.publish(twist)
	print twist

if __name__ == "__main__":
	global pub
	global lastDir 
	global lastSeen
 
	lastSeen = 0
	lastDir = -1
 
	rospy.init_node('nolan', anonymous=True)
	pub = rospy.Publisher('drrobot_player1/drrobot_cmd_vel', Twist)
	rospy.Subscriber("tags", Tags, handleTags)	
	takeoff_pub =rospy.Publisher('/ardrone/takeoff', Empty)
	rospy.spin()

