"""
    Minimal code for wall follower 
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
from sensor_msgs.msg import LaserScan

class Follow(Node):
    def __init__(self):
        super().__init__('follow')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        self.subscription= self.create_subscription(
            LaserScan,
            '/scan',  ## Read
            self.listener_callback,
            qos_profile,
        )
        timer_period = 0.5 # seconds
        self.i = 0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.msg = Twist()
        
        
    def getch(self, timeout=0.5):
        import sys, tty, termios, select
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                ch = sys.stdin.read(1)
            else:
                ch = None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def timer_callback(self):
        '''
        Publisher callback function
        TODO: implement
        '''
        # msg = Twist()
        key = self.getch()
        if key == 'w':
            self.msg.linear.x = 1.0  
        elif key == 'x':
            self.msg.linear.x = -1.0  
        elif key == ' ':
            self.msg.linear.x = 0.0
        self.publisher_.publish(self.msg)

    def listener_callback(self,msg):
        '''
        Subscription Callback 
        TODO: implement
        '''
        self.get_logger().info('I heard : Range[0] "%f" Ranges[50]: "%f"' %(msg.ranges[0] ,msg.ranges[50]))
        

def main(args=None):
    rclpy.init(args=args)
    my_follower = Follow()
    rclpy.spin(my_follower)
    my_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()