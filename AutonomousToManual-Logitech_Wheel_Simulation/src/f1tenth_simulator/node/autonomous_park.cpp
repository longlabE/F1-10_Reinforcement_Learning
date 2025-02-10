#include <ros/ros.h>
#include <ackermann_msgs/AckermannDriveStamped.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/LaserScan.h>

class Autonomous_Park {
private:
     ros::NodeHandle n;
    ros::Publisher drive_pub;
    ros::Subscriber odom_sub;
    ros::Subscriber scan_sub_;
    ros::Timer timer_;
    sensor_msgs::LaserScan latest_scan_;

   static constexpr double car_length = 1.0;
    static constexpr double swing = M_PI / 3.0; // 60 degrees in radians
    double alpha_ = 0.0;


    
    double integral_error = 0;
    double previous_error = 0;

    double Kp = 0.5; // Proportional gain
    double Ki = 0.05; // Integral gain
    double Kd = 0.1; // Derivative gain

    double dt = 0.1; // Time step, assuming 10Hz rate

    double max_speed;
    double max_steering_angle;
    double desired_distance_from_wall = 1.0; // arbitrary desired distance from the wall



    nav_msgs::Odometry latest_odom_;
    bool received_first_odom_ = false;

    void odom_callback(const nav_msgs::Odometry::ConstPtr& msg) {
        latest_odom_ = *msg;
        received_first_odom_ = true;
    }
void scan_callback(const sensor_msgs::LaserScan::ConstPtr& msg) {
    latest_scan_ = *msg;
}


 std::pair<double, double> followRight(double desired_trajectory) 
 {

        //std::cout<<a<<std::endl;

        double a = latest_scan_.ranges[60]; 
        double b = latest_scan_.ranges[0];
        alpha_ = atan((a * cos(swing) - b) / (a * sin(swing)));
        double curr_dist = b * cos(alpha_);
        double future_dist = curr_dist + car_length * sin(alpha_);
        double error = desired_trajectory - future_dist;
        return {error, curr_dist};
}

    std::pair<double, double> followLeft(double desired_trajectory) 
    {
        double a = latest_scan_.ranges[120];
        double b = latest_scan_.ranges[latest_scan_.ranges.size() - 1];
        alpha_ = -atan((a * cos(swing) - b) / (a * sin(swing)));
        double curr_dist = b * cos(alpha_);
        double future_dist = curr_dist - car_length * sin(alpha_);
        double error = future_dist - desired_trajectory;
        return {error, curr_dist};
    }
 void timerCallback(const ros::TimerEvent&) 
 {
        follow_wall();
    }


    void follow_wall() 
  {
    if (!latest_scan_.ranges.empty()) 
   {
        double error_right, curr_dist_right, error_left, curr_dist_left, error;


        double a = latest_scan_.ranges[60]; 
        double b = latest_scan_.ranges[0];
        
        alpha_ = atan((a * cos(swing) - b) / (a * sin(swing)));
        double curr_dist = b * cos(alpha_);

        // alpha_ = -1.38
        // curr_dist = 2.75

        std::tie(error_right, curr_dist_right) = followRight(1);
        std::tie(error_left, curr_dist_left) = followLeft(1);

         std::cout<<"curr dist right:"<<curr_dist_right<<std::endl;

         std::cout<<"curr dist left:"<<curr_dist_left<<std::endl;

        /*if (curr_dist_right >= desired_distance_from_wall) {
            error = -1*error_left;
            
            //ROS_INFO("Following Left Wall");
        } else {
            error = -1*error_right;
            
            //ROS_INFO("Following Right Wall");
        }*/

        std::cout<<"error left:"<<error_left<<std::endl;

        std::cout<<"error right:"<<error_right<<std::endl;

         if (error_right < 0) 
         { // Car is too far from the right wall
           error = error_right;
         } else if (error_left > 0) { // Car is too close to the left wall
           error = error_left;
         } else {
           // Default behavior (e.g., continue with the smaller error or
           // maintain current trajectory)
           error = std::abs(error_right) < std::abs(error_left) ? error_right
                                                                : error_left;
         }

        integral_error += error * dt;
        double derivative_error = (error - previous_error) / dt;
        double control_output = Kp * error + Ki * integral_error + Kd * derivative_error;

        std::cout<<"control outputt:"<<control_output<<std::endl;

        ackermann_msgs::AckermannDriveStamped drive_msg;
        drive_msg.drive.speed = max_speed;
        //ROS_INFO("Error: %f", error);
        drive_msg.drive.steering_angle = max_steering_angle * control_output / desired_distance_from_wall;

        std::cout<<"steering angle:"<<max_steering_angle * control_output / desired_distance_from_wall<<std::endl;

        drive_pub.publish(drive_msg);
        previous_error = error;
    } 
    else 
    {
        ROS_WARN("No laser scan data received yet!");
    }
}



public:
    Autonomous_Park() {
        n = ros::NodeHandle("~");

        std::string autonomous_park_topic, odom_topic;
        n.getParam("autonomous_park_topic", autonomous_park_topic);
        n.getParam("odom_topic", odom_topic);

        n.getParam("max_speed", max_speed);
        n.getParam("max_steering_angle", max_steering_angle);

        drive_pub = n.advertise<ackermann_msgs::AckermannDriveStamped>(autonomous_park_topic, 10);
        odom_sub = n.subscribe(odom_topic, 1, &Autonomous_Park::odom_callback, this);
        scan_sub_ = n.subscribe("/scan", 1, &Autonomous_Park::scan_callback, this);

        timer_ = n.createTimer(ros::Duration(dt), &Autonomous_Park::timerCallback, this);
    }
};


int main(int argc, char** argv) {
    ros::init(argc, argv, "autonomous_park");
    Autonomous_Park autonomous_park;

    ros::spin();

    return 0;
}
