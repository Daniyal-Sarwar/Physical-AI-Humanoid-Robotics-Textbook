#!/usr/bin/env python3
"""Minimal ROS 2 Subscriber Node Example.

This example demonstrates the basic structure of a ROS 2 subscriber node
that subscribes to String messages from a topic.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    """A minimal ROS 2 subscriber node."""

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.get_logger().info('MinimalSubscriber node started')

    def listener_callback(self, msg: String):
        """Handle incoming messages."""
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    """Initialize and spin the node."""
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    
    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
