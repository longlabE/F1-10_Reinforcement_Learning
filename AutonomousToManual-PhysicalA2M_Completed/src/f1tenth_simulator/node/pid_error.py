#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from wall_following.msg import pid_input
import numpy as np
#import matplotlib.pyplot as plt

angle_range = 180
# angle_range = np.pi
car_length = 1.5

desired_trajectory = 0

vel = 100
path = [1,0,1,1,1]
turn = 0
preva = 0
flag = 0
errorList = [0,0,0,0,0]
turnStarted = 0
error = 0.0
alpha = 0.0
final_desired_trajectory = -1
final_direction = 1

left_dist = []
objbuffer = [-1]*25

flag_left = 0

pub = rospy.Publisher('error', pid_input, queue_size=10)

def getRange(data,angle):
	if angle > 179.9:
		angle = 179.9
	# if angle > np.pi-1e-4:
		# angle = np.pi-1e-4
	index = len(data.ranges)*angle/angle_range
	dist = data.ranges[int(index)]
	if math.isinf(dist) or math.isnan(dist):
		return 4.0
	return data.ranges[int(index)]


def followRight(data,desired_trajectory):
	global alpha

	a = getRange(data,60)
	b = getRange(data,0)
	swing = math.radians(60)
	alpha = math.atan((a*math.cos(swing)-b)/(a*math.sin(swing)))
	#print "a","b", a, b
	#print "Alpha right",math.degrees(alpha)
	curr_dist = b*math.cos(alpha)

	future_dist = curr_dist+car_length*math.sin(alpha)

	#print "Right : ",future_dist
	error = desired_trajectory - future_dist
	#print "Error : ",error
	return error, curr_dist

def followLeft(data,desired_trajectory):
	global alpha

	a = getRange(data,120)
	b = getRange(data,179.9)
	swing = math.radians(60)
	#print "a","b", a, b

	#####################
	# CHANGE THIS TO GET THE LIDAR DATA
	# 0 degrees (straight ahead) ray's index is 540
	#print data.ranges[]

	
	print data.ranges[540],



	alpha = -math.atan((a*math.cos(swing)-b)/(a*math.sin(swing)))
	#print "Alpha left",math.degrees(alpha)
	curr_dist = b*math.cos(alpha)
	future_dist = curr_dist-car_length*math.sin(alpha)

	#print "Left : ",future_dist

	error = future_dist - desired_trajectory
	return error, curr_dist


def followCentre(data,desired_trajectory):
	global alpha

	a = getRange(data,130)
	b = getRange(data,179.9)
	swing = math.radians(50)
	#print "center distances: ", a, b
	alpha = -math.atan((a*math.cos(swing)-b)/(a*math.sin(swing)))
	#print "Alpha left",math.degrees(alpha)
	curr_dist1 = b*math.cos(alpha)
	future_dist1 = curr_dist1-car_length*math.sin(alpha)



	a = getRange(data,50)
	b = getRange(data,0)
	swing = math.radians(50)
	alpha = math.atan((a*math.cos(swing)-b)/(a*math.sin(swing)))
	#print "Alpha right",math.degrees(alpha)
	curr_dist2 = b*math.cos(alpha)
	future_dist2 = curr_dist2+car_length*math.sin(alpha)

	desired_trajectory = (future_dist1 + future_dist2)/2

	#print "dist 1 : ",future_dist1
	#print "dist 2 : ",future_dist2
	# print "dist : ",future_dist
	error = future_dist1 - future_dist2
	#print "Error : ",error
	return error, curr_dist2-curr_dist1


def callback(data):
	global error
	global alpha
	print " "
	global flag_obstacle
	global final_desired_trajectory
	global final_direction
	global prev_direction
	global flag_left

	error_right, curr_dist_right = followRight(data,0.4)
	#followRight(data,2.)
	error_left, curr_dist_left = followLeft(data,0.8)
	#followLeft(data,1.)
	# error_center, curr_dist_center = followCentre(data,1.)
	if curr_dist_right >= curr_dist_left:
		error = error_left
		print 'Following Left'
		#print 'Error', error
	else:
		# error = followRight(data,final_desired_trajectory)
		error = error_right
		print 'Following Right'
		#print 'Error', error

	# if curr_dist_center:

	#print 'Is error same?', error
	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	pub.publish(msg)
	

if __name__ == '__main__':
	#print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
