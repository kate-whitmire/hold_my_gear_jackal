import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CircleDrive(Node):
    def __init__(self):
        super().__init__('circle_drive')
        self.publisher = self.create_publisher(TwistStamped, '/j100_0000/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.twist.angular.z = 1.5
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircleDrive()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        stop = TwistStamped()
        stop.header.frame_id = 'base_link'
        node.publisher.publish(stop)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()