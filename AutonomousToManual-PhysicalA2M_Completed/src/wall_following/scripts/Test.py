#!/usr/bin/env python

from wall_following.msg import drive_param
import rospy

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)



