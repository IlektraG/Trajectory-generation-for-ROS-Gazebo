# Trajectory-generation-for-ROS-Gazebo
A Python script for generating the trajectory of a Turtlebot3 robot in ROS. The script uses the 'Linear function with parabolic blends' method to generate the trajectory. 

Using Gazebo we can simulate the trajectory of the robot.
![gazebo](https://user-images.githubusercontent.com/25688222/135135306-dac9fb3e-ce47-481c-a9d3-606f05b2039f.png)

The trajectory consists of five parts:
  * Part 1: Rotation of the robot(0.43414 rad anti-clockwise).
  * Part 2: Linear part(stops at 19.9 m).
  * Part 3: Rotation of the robot(4.712 rad anti-clockwise).
  * Part 4: Linear part(stops at -22 m).
  * Part 5: Rotation of the robot (2.165 rad clockwise).

For each part the robot moves according to the velocities that are calculated and published to the topic /cmd/vel.
