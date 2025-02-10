#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

class SimulatorPoseUpdater:
    def __init__(self):
        rospy.Subscriber("/simulator/pose", PoseStamped, self.update_pose)
        self.visual_marker_pub = rospy.Publisher("/visualization/car_pose", Marker, queue_size=10)
        rospy.loginfo("Simulator Pose Updater Initialized")

    def update_pose(self, data):
        # Create a marker for RViz to display the car's pose
        marker = Marker()
        marker.header.frame_id = "map"  # Ensure it matches the map frame
        marker.header.stamp = rospy.Time.now()
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        marker.pose = data.pose
        marker.scale.x = 0.5  # Arrow length
        marker.scale.y = 0.2  # Arrow width
        marker.scale.z = 0.2  # Arrow height
        marker.color.a = 1.0  # Alpha
        marker.color.r = 0.0  # Red
        marker.color.g = 1.0  # Green
        marker.color.b = 0.0  # Blue
        self.visual_marker_pub.publish(marker)

if __name__ == "__main__":
    rospy.init_node("simulator_pose_updater", anonymous=True)
    pose_updater = SimulatorPoseUpdater()
    rospy.spin()

