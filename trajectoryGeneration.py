#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
def calculate_linear_velocity(t_blend_x, t_fin_x, starting_time):           #function to calculate linear velocity (first part of trajectory)

    a = 0.01636    # linear acceleration on x_axis
    current_time = rospy.get_time()
    
    if (current_time-starting_time) <= t_blend_x:       #first parabolic part
        return a*(current_time-starting_time)
    elif (current_time-starting_time) <= (t_fin_x - t_blend_x):     #linear part
        return 0.2
    else:       #last parabolic part
        return a*(t_fin_x - (current_time - starting_time))


def calculate_angular_velocity(t_blend_z, t_fin_z, starting_time):          #function to calculate angular velocity (first part of trajectory)
    
    a = 9.461  # Angular acceleration on z_axis
    current_time = rospy.get_time()
    
    if current_time-starting_time >= t_fin_z:       #when the last parabolic part ends, speed == 0
        return 0
    if (current_time-starting_time) <= t_blend_z:   #first parabolic part
        return a*(current_time-starting_time)
    elif (current_time-starting_time) <= (t_fin_z - t_blend_z):     #linear part
        return 0.69813
    else:       #last parabolic part
        return a*(t_fin_z - (current_time - starting_time))


def calculate_linear_velocity_final_part(t_blend_x, t_fin_x, starting_time):        #function to calculate linear velocity (second part of trajectory)
    
    a = 0.01636    # linear acceleration on x_axis
    current_time = rospy.get_time() - 129.7232
    
    if (current_time-starting_time) <= t_blend_x:       #first parabolic part
        return a*(current_time-starting_time)
    elif (current_time-starting_time) <= (t_fin_x - t_blend_x):     #linear part
        return 0.2
    else:       #last parabolic part
        return a*(t_fin_x - (current_time - starting_time))



def calculate_angular_velocity_final_part(t_blend_z, t_fin_z, starting_time):       #function to calculate angular velocity (second part of trajectory)
    
    a = 1.025
    current_time = rospy.get_time() - 122.9132
    
    if current_time-starting_time >= t_fin_z:           #when the last parabolic part ends, speed == 0
        return 0
    if (current_time-starting_time) <= t_blend_z:       #first parabolic part
        return a*(current_time - starting_time)
    elif (current_time-starting_time) <= (t_fin_z - t_blend_z):     #linear part
        return 0.69813
    else:       #last parabolic part
        return a*(t_fin_z - (current_time - starting_time))


def calculate_angular_velocity_final_position(t_blend_z, t_fin_z, starting_time):       #function to calculate angular velocity of final part
    
    a = -1.7221  # Angular acceleration on z_axis
    current_time = rospy.get_time() - 251.9454   
    
    if current_time-starting_time >= t_fin_z:       #when the last parabolic part ends, speed == 0
        return 0
    if (current_time-starting_time) <= t_blend_z:   #first parabolic part
        return a*(current_time-starting_time)
    elif (current_time-starting_time) <= (t_fin_z - t_blend_z):     #linear part
        return -0.69813
    else:       #last parabolic part
        return a*(t_fin_z - (current_time - starting_time))


def main():
    print("Starting Trajectory Generation!")
    
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)    #node trajectory generation, publishes Twist type messages to node cmd_vel
    rospy.init_node('trajectory_generation', anonymous = True)
    
    r = rospy.Rate(100)     #setting the Rate
    
    velocity_message = Twist()  #create Twist type message
    
    stop_message = Twist()      #create message to stop the robot when needed
    stop_message.linear.x = 0
    stop_message.linear.y = 0
    stop_message.linear.z = 0
    stop_message.angular.x = 0
    stop_message.angular.y = 0
    stop_message.angular.z = 0    

    while not rospy.is_shutdown():
        
        velocity_message.linear.x = 0
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0
        velocity_message.angular.x = 0
        velocity_message.angular.y = 0  
        velocity_message.angular.z = 0
        
        velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
        r.sleep()
        starting_time = rospy.get_time()    #getting the starting time of the simulation

        
        ###########################
        #first part of trajectory##
        ###########################

        t_blend_z = 0.0691   #t_blend_z = 10%t_fin_z
        t_fin_z = 0.691

        simulation_time = 0     #getting the simulation time
        while (simulation_time - starting_time) <= t_fin_z:
            velocity_message.angular.z = calculate_angular_velocity(t_blend_z, t_fin_z, starting_time)
            velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
            r.sleep()
            
            simulation_time = rospy.get_time()      #getting current time
        velocity_publisher.publish(stop_message)     #publish message to stop

        
        ###########################
        #second part of trajectory##
        ###########################
        
        t_blend_x = 12.2222  #t_blend_x = 10%t_fin_x
        t_fin_x = 122.2222   
               
        while (simulation_time - starting_time - t_fin_z) <= t_fin_x:
            velocity_message.linear.x = calculate_linear_velocity(t_blend_x, t_fin_x, starting_time - t_fin_z)
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
            r.sleep()
            
            simulation_time = rospy.get_time()      #getting current time
        velocity_publisher.publish(stop_message)     #publish message to stop
        

        ###########################
        #third part of trajectory#
        ###########################
        
        t_blend_z = 0.681       #t_blend_z = 10%t_fin_z
        t_fin_z = 6.81

        simulation_time = rospy.get_time()  #getting the simulation time
        while (simulation_time - starting_time - 122.9132) <= t_fin_z:
            velocity_message.linear.x = 0
            velocity_message.angular.z = calculate_angular_velocity_final_part(t_blend_z, t_fin_z, starting_time)
            
            velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
            r.sleep()
            
            simulation_time = rospy.get_time()      #getting current time
        velocity_publisher.publish(stop_message)    #publish message to stop


        ##########################
        #fourth part of trajectory#
        ##########################
        
        t_blend_x = 12.22222     #t_blend_x = 10%t_fin_x
        t_fin_x = 122.2222

        simulation_time = rospy.get_time()  #getting the simulation time
        while (simulation_time - starting_time - 122.9132 - t_fin_z) <= t_fin_x:
            velocity_message.linear.x = calculate_linear_velocity_final_part(t_blend_x, t_fin_x, starting_time)
            velocity_message.angular.z = 0
            
            velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
            r.sleep()
            
            simulation_time = rospy.get_time()      #getting current time
        velocity_publisher.publish(stop_message)    #publish message to stop

        
        ##########################
        #fifth part of trajectory#
        ##########################
        
        t_blend_z = 0.4054      #t_blend_z = 10%t_fin_z
        t_fin_z = 4.054    

        while (simulation_time - starting_time - t_fin_x - t_fin_x - 7.501) <= t_fin_z:
            velocity_message.angular.z = calculate_angular_velocity_final_position(t_blend_z, t_fin_z, starting_time)
            velocity_publisher.publish(velocity_message)    #publishing to node cmd_vel
            r.sleep()
            
            simulation_time = rospy.get_time()      #getting current time        
        velocity_publisher.publish(stop_message)    #publish message to stop
        break
    
    print("The trajectory is over!!")


if __name__ == '__main__':
    try:
        main()
        
    except rospy.ROSInterruptException:
        pass
