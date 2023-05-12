import sys
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist,Point
from nav_msgs.msg import Odometry
from math import *


class RobotGoToGoal(Node):

    def __init__(self):
        super().__init__('goal_movement_node')
        self.velocity_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Odometry,'/odom',self.pose_callback,10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.go_to_goal_function)
        self.robot_pose = Point()
        self.goal_pose = Point()
        self.distance_to_goal =0
        self.angle_to_goal = 0

    def pose_callback(self,data):
        robot_pose_x = data.pose.pose.position.x
        robot_pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation.z
        (roll,pitch,yaw) = self.euler_from_quaternion(quaternion.x, quaternion.y, quaternion.z, quaternion.w)
        self.robot_pose.z = yaw
        # msg = Twist()
        # msg.linear.x = 0.2
        # msg.angular.z = 0.7

        # self.velocity_pub.publish(msg)
        
    def go_to_goal_function(self):
        self.goal_pose.x = float(sys.argv[1])
        self.goal_pose.y = float(sys.argv[2])

        self.distance_to_goal = sqrt(pow((self.goal_pose.x-self.robot_pose.x),2)+pow((self.goal_pose.y-self.robot_pose.x),2))
        self.angle_to_goal= atan2((self.goal_pose.y-self.robot_pose.y),(self.goal_pose.x-self.robot_pose.x))

        msg ='X:{:3f} Y:{:3f}'.format(self.distance_to_goal,self.angle_to_goal)
        self.get_logger().info(msg)


    def euler_from_quaternion(self,x,y,z,w):
        t0 = 2 * (w * x + y * z)
        t1 = 1 - 2 * (x * x + y * y)
        roll_x = atan2(t0,t1)
        t2 = 2 * (w * y - z * x)


def main(args=None):
    rclpy.init(args=args)

    gtg_node = RobotGoToGoal()

    rclpy.spin(gtg_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gtg_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
