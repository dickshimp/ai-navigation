#!/usr/bin/env python

import serial
import rospy
import bitstruct
from navigation_msgs.msg import VelAngle
from navigation_msgs.msg import EmergencyStop
CART_PORT = '/dev/ttyACM0' #hardcoded depending on computer

class MotorEndpoint(object):

    def __init__(self):
        global SPEED_PORT
        self.killswitch = False
        self.current_speed = 0.0
        self.goal_speed = 0.0
        self.goal_angle = 0.0

        self.cmd_msg = None
        """ Set up the node. """
        rospy.init_node('motor_endpoint')
        rospy.loginfo("Starting motor node!")
        #Connect to arduino for sending speed
        '''try:
            self.speed_ser = serial.Serial(CART_PORT, 9600, write_timeout=0)
        except Exception as e:
            print "Motor_endpoint: " + str(e)
            rospy.logerr("Motor_endpoint: " + str(e))
            #exit(0)'''

        rospy.loginfo("Speed serial established")
        """
        Connect to arduino for steering
        """
        self.speed_string = ''
        self.motion_subscriber = rospy.Subscriber('/nav_cmd', VelAngle, self.motion_callback,
                                                  queue_size=10)
        self.killswitch_subscriber = rospy.Subscriber('/emergency_stop', EmergencyStop,
                                                      self.kill_callback, queue_size=10)

        rate = rospy.Rate(5)

        while not rospy.is_shutdown():
            if self.cmd_msg is not None:
                self.send_to_motors()
            rate.sleep()

    def motion_callback(self, planned_vel_angle):
        if not self.killswitch:
            self.cmd_msg = planned_vel_angle      
        else:
            self.cmd_msg.vel_curr = planned_vel_angle.vel_curr  


    def kill_callback(self, data):
        self.killswitch = data.emergency_stop
        if self.killswitch:
            self.cmd_msg.vel = -100


    def send_to_motors(self):
        target_speed = int(self.cmd_msg.vel) #float64
        current_speed = int(self.cmd_msg.vel_curr) #float64
        target_angle = int(( (self.cmd_msg.angle - -70) / (70 - -70) ) * (100 - 0) + 0)

        rospy.loginfo(str(target_speed) + " " + str(current_speed) + " " + str(target_angle))

        data = (target_speed,current_speed,target_angle)
        data = bytearray(b'\x00' * 6)
        rospy.loginfo(data)
                          #('u8u8u8', data, 0, throttle, brake, steering)
        if target_speed < 0:
            bitstruct.pack_into('u8u8u8', data, 0, 0, target_speed, target_angle)
        else:
            bitstruct.pack_into('u8u8u8', data, 0, target_speed, 0, target_angle)

        #self.speed_ser.write(data) 
        #rospy.loginfo(data)

if __name__ == "__main__":
    try:
        MotorEndpoint()
    except rospy.ROSInterruptException:
        pass
