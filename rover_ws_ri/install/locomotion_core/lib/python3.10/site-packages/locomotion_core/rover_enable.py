import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import Bool

global flag
flag = False

contactorPin = 23
# open the gpio chip and set the LED pin as output
try:
    import lgpio
    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, contactorPin)
    flag=True
except:
    pass

class duEnable(Node):

    def __init__(self):
        super().__init__('rover_enable')
        self.inCmd = 0.0
        self.subscription = self.create_subscription(
            Bool,
            'r4/enable',
            self.enable_callback,
            5)
        self.subscription  # prevent unused variable warning

    def contactor_ctrl(self, val):
        if flag:
            lgpio.gpio_write(h, contactorPin, val)
        else:
            print("Flag disabled.")

    def enable_callback(self, msg):
        inCmd = msg.data
        self.contactor_ctrl(inCmd)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = duEnable()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
