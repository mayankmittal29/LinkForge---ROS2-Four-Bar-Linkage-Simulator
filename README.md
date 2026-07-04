# Four-Bar Linkage ROS2 Simulation

This repository contains the complete implementation of a **Mechatronics System Design - Assignment 1** project. It translates a Fusion 360 four-bar linkage mechanism (crank-rocker configuration) into a fully functional dynamic simulation in ROS2 Humble using RViz2.

## 📂 Directory Structure

```text
.
├── README.md                      # This documentation file
├── install_ros2.sh                # Automated ROS2 Humble setup script
├── build_and_run.sh               # Single-click build and launch script
├── four_bar_linkage.urdf          # High-fidelity URDF geometry file
├── MSD_Assignment1_Report.pdf     # Detailed LaTeX-generated mathematical report
└── four_bar_linkage_ws/           # Primary ROS2 Colcon Workspace
    └── src/
        └── four_bar_linkage/
            ├── package.xml        # ROS2 package dependencies
            ├── setup.py           # Python package installer
            ├── config/
            │   └── rviz_config.rviz  # Custom RViz2 UI layout and camera configuration
            ├── launch/
            │   └── display.launch.py # Launches RViz, robot_state_publisher, and our node
            ├── urdf/
            │   └── four_bar_linkage.urdf # Core geometrical structure mapped from Fusion360
            └── four_bar_linkage/
                └── joint_state_publisher.py # Custom Kinematics solver engine
```

## ⚙️ Core Files Explained

- **`install_ros2.sh`**: A robust shell script customized for Ubuntu 22.04 that fixes corrupted system repositories and automatically installs ROS2 Humble and all required simulation dependencies.
- **`build_and_run.sh`**: Automates the underlying ROS2 `colcon build`, sources the local workspace, and runs the display launch file.
- **`joint_state_publisher.py`**: The "brain" of the simulation. Because native URDF cannot process closed-loop mechanisms out of the box, this Python node uses the **Law of Cosines** to calculate "elbow-up" inverse kinematics in real time. It drives the crank $\pm 30°$ and forces the rocker to connect continuously back to the ground.
- **`four_bar_linkage.urdf`**: We use exact geometric `<box>` primitives to construct the mechanism natively. This guarantees exact mathematical precision avoiding coordinate misalignments caused by flawed `.stl` mesh exporters.
- **`rviz_config.rviz`**: A pre-saved visualization state that removes unnecessary TF axes and perfectly aligns the camera in a 2D top-down view to match the CAD sketches.

## 🎨 Color Coding Taxonomy

The simulation strictly models the color structure established in the initial Fusion 360 designs to guarantee traceability between CAD and RViz2:

| Link Name             | Length | Visual Color | Focus Area                  |
| --------------------- | ------ | ------------ | --------------------------- |
| **Ground (L1)**       | 80 mm  | 🟡 **Yellow** | Horizontal Fixed Bottom     |
| **Crank Driver (L2)** | 50 mm  | 🔴 **Pink**   | Rotating Input Mechanism    |
| **Coupler (L3)**      | 100 mm | ⚫ **Black**   | Connecting Link             |
| **Rocker Output (L4)**| 80 mm  | 🔵 **Blue**   | Oscillating right-hand side |


## 🚀 How to Run the Simulation

If this is your first time setting up the environment, or your ROS2 installation is broken, run the setup script:
```bash
sudo chmod +x install_ros2.sh
sudo ./install_ros2.sh
```
cd
**To build the workspace and launch the simulation:**
```bash
chmod +x build_and_run.sh
./build_and_run.sh
```
*(This commands handles the workspace compilation, overlay sourcing, and triggers the RViz2 environment automatically!)*
