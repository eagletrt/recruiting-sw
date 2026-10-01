from glob import glob

from setuptools import setup

package_name = 'eagle_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/can', ['../../can/eagle_task.dbc']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Eagle AS',
    maintainer_email='angelo.nutu@eagletrt.it',
    description='Simulation for the Eagle controls recruitment task',
    license='MIT',
    entry_points={
        'console_scripts': [
            'fake_perception = eagle_sim.fake_perception:main',
            'track_publisher = eagle_sim.track_publisher:main',
            'vehicle_sim = eagle_sim.vehicle_sim:main',
            'lateral_controller = eagle_sim.lateral_controller:main',
            'can_gateway = eagle_sim.can_gateway:main',
        ],
    },
)
