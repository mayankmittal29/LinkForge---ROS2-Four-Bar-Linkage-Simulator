#!/usr/bin/env python3
"""
Joint State Publisher for Four-Bar Linkage Mechanism
=====================================================
Drives the crank (Joint A) and computes Joint B & Joint C angles
using closed-loop kinematics so the rocker tip meets Joint D.

The crank angle is varied sinusoidally so that Joint B naturally
oscillates within approximately ±30 degrees.

Link dimensions:
  L1 (ground)  = 0.08m
  L2 (crank)   = 0.05m
  L3 (coupler) = 0.10m
  L4 (rocker)  = 0.08m
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker
import math
import time


class FourBarJointStatePublisher(Node):

    def __init__(self):
        super().__init__('four_bar_joint_state_publisher')

        # Link lengths (meters)
        self.L1 = 0.08   # Ground
        self.L2 = 0.05   # Crank
        self.L3 = 0.10   # Coupler
        self.L4 = 0.08   # Rocker

        # Publishers
        self.publisher = self.create_publisher(JointState, 'joint_states', 10)
        self.marker_pub = self.create_publisher(Marker, 'joint_b_annotation', 10)

        # Publish at 50 Hz for smooth animation
        self.timer = self.create_timer(0.02, self.timer_callback)
        self.start_time = time.time()

        # Oscillation parameters
        self.frequency = 0.5  # Hz

        self.get_logger().info('Four-bar linkage joint state publisher started!')

    def solve_four_bar(self, theta_A):
        """
        Given crank angle theta_A, compute Joint B and Joint C angles
        (in URDF relative frame) to close the four-bar loop.
        
        Returns (theta_B_rel, theta_C_rel) or None if no solution.
        
        Geometry:
          Joint A at (0, 0)
          Joint D at (L1, 0) = (0.08, 0)
          Joint B at (L2*cos(θA), L2*sin(θA))
          Joint C must be L3 from B and L4 from D
        """
        L1, L2, L3, L4 = self.L1, self.L2, self.L3, self.L4

        # Position of Joint B (end of crank)
        Bx = L2 * math.cos(theta_A)
        By = L2 * math.sin(theta_A)

        # Position of Joint D (fixed end of ground link)
        Dx = L1
        Dy = 0.0

        # Distance from B to D
        BDx = Dx - Bx
        BDy = Dy - By
        BD = math.sqrt(BDx * BDx + BDy * BDy)

        # Check triangle inequality: can L3 and L4 reach from B to D?
        if BD > (L3 + L4) or BD < abs(L3 - L4):
            return None

        # Angle of vector B->D
        angle_BD = math.atan2(BDy, BDx)

        # Law of cosines: angle at B in triangle BCD
        # cos(angle) = (L3^2 + BD^2 - L4^2) / (2 * L3 * BD)
        cos_angle_B = (L3 * L3 + BD * BD - L4 * L4) / (2.0 * L3 * BD)
        cos_angle_B = max(-1.0, min(1.0, cos_angle_B))
        angle_at_B = math.acos(cos_angle_B)

        # Absolute angle of coupler (B to C direction)
        # Use "elbow-up" configuration (add) to prevent crossed links 
        # and form a clean open quadrilateral
        theta_coupler_abs = angle_BD + angle_at_B

        # Position of Joint C
        Cx = Bx + L3 * math.cos(theta_coupler_abs)
        Cy = By + L3 * math.sin(theta_coupler_abs)

        # Absolute angle of rocker (C to D direction)
        theta_rocker_abs = math.atan2(Dy - Cy, Dx - Cx)

        # Convert to URDF relative angles:
        # Joint B relative angle = coupler_absolute - crank_absolute
        theta_B_rel = theta_coupler_abs - theta_A

        # Joint C relative angle = rocker_absolute - coupler_absolute
        theta_C_rel = theta_rocker_abs - theta_coupler_abs

        return (theta_B_rel, theta_C_rel)

    def timer_callback(self):
        t = time.time() - self.start_time

        # Initial crank angle = 90° (π/2), oscillating ±30° (π/6) around it
        # Range: 60° to 120° (π/3 to 2π/3)
        crank_center = math.pi / 2.0       # 90 degrees
        crank_amplitude = math.pi / 6.0    # 30 degrees
        theta_A = crank_center + crank_amplitude * math.sin(2.0 * math.pi * self.frequency * t)

        # Solve closed-loop kinematics
        result = self.solve_four_bar(theta_A)

        if result is None:
            # Skip this frame if no valid solution
            return

        theta_B_rel, theta_C_rel = result

        # Publish joint states
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint_A', 'joint_B', 'joint_C']
        msg.position = [theta_A, theta_B_rel, theta_C_rel]
        msg.velocity = [0.0, 0.0, 0.0]
        msg.effort = [0.0, 0.0, 0.0]

        self.publisher.publish(msg)

        # Draw a floating text marker at Joint B
        marker = Marker()
        marker.header.stamp = msg.header.stamp
        # joint_B connects crank to coupler, so its origin is the start of coupler_link
        marker.header.frame_id = 'coupler_link'
        marker.ns = 'angle_annotation'
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        
        # Position floating just above the joint
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.025
        
        marker.scale.z = 0.015  # Text height
        
        # Bright green text for high visibility
        marker.color.r = 0.2
        marker.color.g = 1.0
        marker.color.b = 0.2
        marker.color.a = 1.0
        
        angle_deg = math.degrees(theta_B_rel)
        marker.text = f"Joint B: {angle_deg:+.1f}°"
        
        self.marker_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = FourBarJointStatePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
