from setuptools import setup

package_name = 'my_turtle_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='imaan',
    maintainer_email='imaan@email.com',
    description='Turtle controller package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'move_turtle = my_turtle_package.move_turtle:main',
        'circle_turtle = my_turtle_package.circle_turtle:main',
        'task2 = my_turtle_package.task2:main',
        
    ],
},
)
