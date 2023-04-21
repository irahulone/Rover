import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16
from geometry_msgs.msg import Twist

global lx, az
lx = 0.0; az = 0.0

class get_move_cmds(Node):

    def __init__(self):
        super().__init__('rover_driver')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.move_cmd_callback,
            5)
        self.subscription  # prevent unused variable warning

        self.pub_du1 = self.create_publisher(Int16, 'r4/du1/pwr', 5)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.du1_callback)
        self.i = 0

        self.pub_du2 = self.create_publisher(Int16, 'r4/du2/pwr', 5)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.du2_callback)
        self.i = 0

    def move_cmd_callback(self, msg):
        global lx, az
        lx = msg.linear.x
        az = msg.angular.z
        #print(lx)

    def du1_callback(self):
        global lx, az
        msg = Int16()
        msg.data = int(lx*100)
        self.pub_du1.publish(msg)
        self.i += 1

    def du2_callback(self):
        global lx, az
        msg = Int16()
        msg.data = int(az*100)
        self.pub_du2.publish(msg)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    sub_move_cmds = get_move_cmds()

    rclpy.spin(sub_move_cmds)

    sub_move_cmds.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()