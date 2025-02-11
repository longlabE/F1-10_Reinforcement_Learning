#!/usr/bin/env python

from __future__ import print_function
import sys
import math
import numpy as np

#ROS Imports
import rospy
from sensor_msgs.msg import Image, LaserScan
from wall_following.msg import drive_param
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive


#PID CONTROL PARAMS
kp = 0.8
ki = 0.0001
kd = 0.5
turn_factor = 4.5
last_turn_correction = 0
turn_decay_rate=0.1

servo_offset = 0.0
prev_error = 0.0 
error = 0.0
integral = 0.0

#WALL FOLLOW PARAMS
ANGLE_RANGE = 270 # Hokuyo 10LX has 270 degrees scan
DESIRED_DISTANCE_RIGHT = 0.2 # meters
DESIRED_DISTANCE_LEFT = 0.1  #meters
VELOCITY = 20 # meters per second
CAR_LENGTH = 0.50 # Traxxas Rally is 20 inches or 0.5 meters
TIME_INCREMENT = 0.1

class WallFollow:
    """ Implement Wall Following on the car
    """
    def __init__(self):
        #Topics & Subs, Pubs
        lidarscan_topic = '/scan'
        param_name = rospy.search_param ('wall_follow_topic')
        #drive_topic = '/nav'
        drive_topic = rospy.get_param (param_name)
        self.speed = 0

        self.lidar_sub = rospy.Subscriber(lidarscan_topic, LaserScan, self.lidar_callback)
        #self.drive_pub = rospy.Publisher(drive_topic, AckermannDriveStamped, queue_size=1)
	self.drive_pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)
	



    def getRange(self, data, angle):
        # data: single message from topic /scan
        # Outputs length in meters to object with angle in lidar scan field of view
        # make sure to take care of nans etc.
        # TODO: implement


        ranges = data.ranges
        range_max = data.range_max
        range_min = data.range_min
        valid_ranges = np.clip(ranges, range_min, range_max) #get rid of bad data


        index = np.arange(valid_ranges.size)


        angle_array = data.angle_min + index * data.angle_increment


        idx = (np.abs(angle_array - angle)).argmin()
        desired_range = valid_ranges[idx]
        desired_angle = angle_array[idx]
        #print("distance: ",  data.ranges[900])
        return {"range": desired_range, "angle": desired_angle}

    def pid_control(self, error, velocity):
        global integral
        global prev_error
        global kp
        global ki
        global kd
	global turn_factor
	global last_turn_correction
        P = kp * error
        I = integral + ki * error * TIME_INCREMENT
        D = kd * (error - prev_error) / TIME_INCREMENT
        angle = P + I + D
	print("angle: ", angle)
        #print(" Error:" + str(error))
        #TODO: Use kp, ki & kd to implement a PID controller for 
        #drive_msg = AckermannDriveStamped()
        #drive_msg.header.stamp = rospy.Time.now()
        #drive_msg.header.frame_id = "laser"
        #drive_msg.drive.steering_angle = angle
	#drive_msg.drive.speed = velocity
	#drive_msg.drive.speed = velocity - abs(1.5*angle)


       
        drive_msg = drive_param()
	#temporarily changes velocity and angle for testing
	drive_msg.velocity = velocity - abs(1.5*angle)
	
	drive_msg.angle =  angle
	self.drive_pub.publish(drive_msg)
        self.speed = velocity - abs(1.5*angle) #allow use of velocity in followLeft
        prev_error = error
        integral = I

    def followLeft(self, data, leftDist):
        #Follow left wall as per the algorithm 
        #TODO:implement

        a = self.getRange(data, math.pi/6) #30 degrees
        b = self.getRange(data, math.pi/2) #90 degrees

        theta = abs(a["angle"]-b["angle"])

        alpha = math.atan((b["range"]-a["range"]*math.cos(theta))/(a["range"]*math.sin(theta)))

        look_ahead_dist = self.speed * TIME_INCREMENT #(rospy.Time.now() - data.header.stamp)  

        pred_dist = b["range"]*math.cos(alpha) - look_ahead_dist*math.sin(alpha)
        error = leftDist - pred_dist
        
        #print("A: " + str(a["range"]) + " B: " + str(b["range"])+  " Alpha:" + str(alpha) + " Error: " + str(-1 * error))

        return 1 * error

    def lidar_callback(self, data):
        """ 
        """
        error = self.followLeft(data, DESIRED_DISTANCE_LEFT) #TODO: replace with error returned by followLeft
        #send error to pid_control
        self.pid_control(error, VELOCITY)

def main(args):
    rospy.init_node("WallFollow_node", anonymous=True)
    wf = WallFollow()
    rospy.sleep(TIME_INCREMENT)
    rospy.spin()

if __name__=='__main__':
	main(sys.argv)

