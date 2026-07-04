#!/bin/bash
# ============================================================
# Build and Run the Four-Bar Linkage ROS2 Package
# Run AFTER installing ROS2 Humble
# Usage: cd ~/Desktop/SEM8/Mecha/Mayank/four_bar_linkage_ws && ./build_and_run.sh
# ============================================================

set -e

echo "=========================================="
echo "  Building Four-Bar Linkage ROS2 Package"
echo "=========================================="

# Source ROS2
source /opt/ros/humble/setup.bash

echo ""
echo "[1/3] Building workspace with colcon..."
colcon build --symlink-install

echo ""
echo "[2/3] Sourcing workspace..."
source install/setup.bash

echo ""
echo "[3/3] Launching visualization..."
echo ""
echo "  RViz2 will open with the four-bar linkage."
echo "  Joint B is oscillating between -30° and +30°."
echo "  Press Ctrl+C to stop."
echo ""

ros2 launch four_bar_linkage display.launch.py
