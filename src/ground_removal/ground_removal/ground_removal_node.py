import rclpy
import numpy as np
from rclpy.node import Node

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32


class GroundRemoval(Node):

    def __init__(self):

        super().__init__('ground_removal_node')
        self.z_threshold = -0.1

        self.subscription = self.create_subscription(
            PointCloud,
            '/carmaker/pointcloud',
            self.pointcloud_callback,
            10
        )

        self.publisher = self.create_publisher(
            PointCloud,
            '/pointcloud_no_ground',
            10
        )
        self._logger

    def pointcloud_callback(self, msg):

        filtered_cloud = PointCloud()

        filtered_cloud.header = msg.header

        filtered_points = []

        for p in msg.points:

            if p.z > self.z_threshold:
                filtered_points.append(Point32(x=p.x, y=p.y, z=p.z))

        filtered_cloud.points = filtered_points

        self.publisher.publish(filtered_cloud)


def main():

    rclpy.init()

    node = GroundRemoval()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()