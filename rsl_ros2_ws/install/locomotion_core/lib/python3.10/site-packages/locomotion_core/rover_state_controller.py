import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool
from std_msgs.msg import String

import time

global lx, az, deadmanButtonState 

lx = 0.0; az = 0.0

deadmanButtonState = False

class get_move_cmds(Node):

    def __init__(self):
        super().__init__('rover_state_controler')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.move_cmd_callback,
            5)
        self.subscription  # prevent unused variable warning

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            5)
        self.subscription  # prevent unused variable warning

        self.subscription = self.create_subscription(
            Twist,
            '/r4/cmd_vel',
            self.move_cmd_callback,
            5)
        self.subscription  # prevent unused variable warning

        self.toggle_button = 0  # Toggle button to cycle between states.
        self.rover_modeC = "NEU_M"  # Assigned state of the rover.
        self.toggle_flag = 0     # if flag = 1; locked, flag = 0; free

        self.pub_core_cmdvel = self.create_publisher(Twist, 'r4/core_cmdvel', 5)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.core_cmdvel_callback)
        self.i = 0

        self.pub_du1_en = self.create_publisher(Bool, 'r4/du1/en', 1)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.du1_en_callback)
        self.i = 0

        self.pub_robot_modeC = self.create_publisher(String, 'r4/modeC', 1)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.robot_modeC_callback)
        self.i = 0

        

    def toggle(self):
        match self.toggle_button:
            case 0:
                self.rover_modeC = "NEW_M"
                self.toggle_button = 1
            case 1:
                self.rover_modeC = "TEA_M"
                self.toggle_button = 2
            case 2:
                self.rover_modeC = "PLY_M"
                self.toggle_button = 0

    def joy_callback(self, data):

        global deadmanButtonState
        deadmanButtonState = False
        if (data.buttons[4] == 1 or data.buttons[5] == 1):
            deadmanButtonState = True
    
        toggle_button = data.buttons[0]
        if toggle_button == 1:
            if self.toggle_flag == 0:
                self.toggle()
                print(self.rover_modeC)
                self.toggle_flag = 1
        else:
            self.toggle_flag = 0
        
    def move_cmd_callback(self, msg):
        global lx, az
        lx = msg.linear.x
        az = msg.angular.z
        #print(lx)

    def core_cmdvel_callback(self):
        global lx, az
        msg = Twist()
        msg.linear.x = lx
        msg.angular.x = az
        self.pub_core_cmdvel.publish(msg)
        self.i += 1

    def robot_modeC_callback(self):
        msg = String()
        msg.data = self.rover_modeC
        self.pub_robot_modeC.publish(msg)
        self.i += 1

    def du1_en_callback(self):
        global deadmanButtonState
        msg = Bool()
        msg.data = deadmanButtonState
        self.pub_du1_en.publish(msg)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sub_move_cmds = get_move_cmds()

    rclpy.spin(sub_move_cmds)

    sub_move_cmds.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()