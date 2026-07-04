from setuptools import setup
import os
from glob import glob

package_name = 'four_bar_linkage'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mayank',
    maintainer_email='mayank@example.com',
    description='Four-bar linkage mechanism URDF and ROS2 simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_state_publisher = four_bar_linkage.joint_state_publisher:main',
        ],
    },
)
