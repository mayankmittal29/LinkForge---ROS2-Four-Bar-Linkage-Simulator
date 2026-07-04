#!/bin/bash
# ============================================================
# ROS2 Humble Installation Script for Ubuntu 22.04
# Run: sudo ./install_ros2.sh
# ============================================================

# Don't exit on first error - we'll handle errors manually
set +e

echo "=========================================="
echo "  ROS2 Humble Installation for Ubuntu 22.04"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Please run this script with sudo:"
    echo "  sudo ./install_ros2.sh"
    exit 1
fi

ACTUAL_USER=${SUDO_USER:-$USER}
ACTUAL_HOME=$(eval echo ~$ACTUAL_USER)

echo ""
echo "[0/7] Fixing broken apt sources..."
# Install apt-transport-https first (needed for https repos)
apt-get install -y apt-transport-https ca-certificates 2>/dev/null || true

# Disable problematic repos temporarily
if [ -f /etc/apt/sources.list.d/anydesk-stable.list ]; then
    mv /etc/apt/sources.list.d/anydesk-stable.list /etc/apt/sources.list.d/anydesk-stable.list.bak 2>/dev/null || true
    echo "  Disabled anydesk repo (will restore later)"
fi
if [ -f /etc/apt/sources.list.d/mysql.list ]; then
    mv /etc/apt/sources.list.d/mysql.list /etc/apt/sources.list.d/mysql.list.bak 2>/dev/null || true
    echo "  Disabled mysql repo (will restore later)"
fi
# Fix the broken archive.ubuntu.com/ubuntu stable entry if it exists
if grep -r "archive.ubuntu.com/ubuntu stable" /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null; then
    echo "  Found broken 'stable' entry in apt sources, commenting it out..."
    sed -i '/archive.ubuntu.com\/ubuntu stable/s/^/#/' /etc/apt/sources.list 2>/dev/null || true
    find /etc/apt/sources.list.d/ -name "*.list" -exec sed -i '/archive.ubuntu.com\/ubuntu stable/s/^/#/' {} \; 2>/dev/null || true
fi

echo ""
echo "[1/7] Updating system packages..."
apt-get update -y 2>&1 | tail -5

echo ""
echo "[2/7] Installing prerequisites..."
apt-get install -y software-properties-common curl gnupg lsb-release apt-transport-https ca-certificates

echo ""
echo "[3/7] Adding ROS2 GPG key..."
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "  ✓ GPG key added"

echo ""
echo "[4/7] Adding ROS2 repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
echo "  ✓ Repository added"

echo ""
echo "[5/7] Updating package index..."
apt-get update -y 2>&1 | tail -5

echo ""
echo "[6/7] Installing ROS2 Humble Desktop (this may take 10-15 minutes)..."
apt-get install -y ros-humble-desktop
if [ $? -ne 0 ]; then
    echo "ERROR: ROS2 installation failed!"
    echo "Try running: sudo apt-get update && sudo apt-get install -y ros-humble-desktop"
    exit 1
fi

echo ""
echo "[7/7] Installing additional tools..."
apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete \
    ros-humble-xacro \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-state-publisher

# Initialize rosdep
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    rosdep init 2>/dev/null || true
fi
su - $ACTUAL_USER -c "rosdep update" 2>/dev/null || true

# Add ROS2 to bashrc
if ! grep -q "source /opt/ros/humble/setup.bash" "$ACTUAL_HOME/.bashrc"; then
    echo "" >> "$ACTUAL_HOME/.bashrc"
    echo "# ROS2 Humble" >> "$ACTUAL_HOME/.bashrc"
    echo "source /opt/ros/humble/setup.bash" >> "$ACTUAL_HOME/.bashrc"
fi

# Restore disabled repos
if [ -f /etc/apt/sources.list.d/anydesk-stable.list.bak ]; then
    mv /etc/apt/sources.list.d/anydesk-stable.list.bak /etc/apt/sources.list.d/anydesk-stable.list 2>/dev/null || true
fi
if [ -f /etc/apt/sources.list.d/mysql.list.bak ]; then
    mv /etc/apt/sources.list.d/mysql.list.bak /etc/apt/sources.list.d/mysql.list 2>/dev/null || true
fi

echo ""
echo "=========================================="
echo "  ROS2 Humble Installation Complete! ✓"
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Open a NEW terminal"
echo "  2. Run:  cd ~/Desktop/SEM8/Mecha/Mayank/four_bar_linkage_ws && ./build_and_run.sh"
echo ""
