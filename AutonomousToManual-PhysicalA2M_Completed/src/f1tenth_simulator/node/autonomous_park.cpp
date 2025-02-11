#include <ros/ros.h>
#include <ackermann_msgs/AckermannDriveStamped.h>

class Autonomous_Park {
private:
    ros::NodeHandle n;
    ros::Publisher drive_pub;
    ros::Subscriber odom_sub;
ros::Subscriber deadman_sub_;
ackermann_msgs::AckermannDriveStamped drive_msg;


void deadman_callback(const ackermann_msgs::AckermannDriveStamped::ConstPtr& msg) {
    drive_msg = *msg;
}



public:
    Autonomous_Park() {
        n = ros::NodeHandle("~");

        std::string drive_topic,auto_topic;
        n.getParam("autonomous_park_topic", auto_topic);
	n.getParam("drive_paramater_topic", drive_topic);


        drive_pub = n.advertise<ackermann_msgs::AckermannDriveStamped>(auto_topic, 10);
	deadman_sub_ = n.subscribe(drive_topic, 1, &Autonomous_Park::deadman_callback, this);

    }

   
   void pub_auto() 
{
	drive_pub.publish(drive_msg);
}


};

int main(int argc, char** argv) {
    ros::init(argc, argv, "autonomous_park");
    Autonomous_Park autonomous_park;

    ros::Rate loop_rate(10); // 10 Hz loop rate

    while (ros::ok()) {
        autonomous_park.pub_auto();
        ros::spinOnce();
        loop_rate.sleep();
    }

    return 0;
}

