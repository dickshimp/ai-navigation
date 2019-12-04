#!/usr/bin/env python

import rospy
import pyaudio  
import wave 
import speech_recognition as sr
import sys
import os.path
import time
from playsound import playsound
import vlc
from std_msgs.msg import Bool, String
from sensor_msgs.msg import NavSatFix


class speech_recognition_core(object):

    def __init__(self):
        self.active = 0
        self.text_passing = False
        self.ping_in_sound = vlc.MediaPlayer("/home/jeffercize/catkin_ws/src/ai-navigation/cart_endpoints/scripts/ping_in.mp3")
        self.ping_out_sound = vlc.MediaPlayer("/home/jeffercize/catkin_ws/src/ai-navigation/cart_endpoints/scripts/ping_out.mp3")
        self.emergency_sound = vlc.MediaPlayer("/home/jeffercize/catkin_ws/src/ai-navigation/cart_endpoints/scripts/Emergency.mp3")
        
        rospy.init_node('speech_recognition')
        rospy.loginfo("Starting Speech Recognition Node!")
        self.pullover_pub = rospy.Publisher('/pullover', Bool, queue_size=10)
        self.speech_text_pub = rospy.Publisher('/speech_text', String, queue_size=10)
        self.location_speech_sub = rospy.Subscriber('/location_speech', Bool, self.location_speech_callback)
        
        #This loops helps to identify all avaliable microphones
        for device_index, device_name in enumerate(sr.Microphone.list_microphone_names()):
            print(device_name)

        self.m = sr.Microphone() #can set the microphone index here
        self.r = sr.Recognizer()
        
        #experimental ambient noise adjustment
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            self.loop()
            rate.sleep()

    def loop(self):
        print("Listening for a Command Phrase")
        #First listen for any sound loud enough listen for a maximum of 5 seconds
        #and then process it through google, then process the resulting string
        with self.m as source:
            try:
                audio = self.r.listen(source, phrase_time_limit=5)
                text = self.r.recognize_google(audio)
                text = text.lower()
                text_array = text.split()
                if self.text_passing:
                    speech_text_pub.publish(text)
                print(text)
                #Alucard, autocorrect, autocart possible other words that need added
                for x in range(len(text_array)):
                    #checks for single words like autocart and skips looking for individual words if it is found
                    if self.active <= 0:
                        if text_array[x] == "alucard" or text_array[x] == "autocorrect" or text_array[x] == "autocart" or text_array[x] == "autocar" or text_array[x] == "omega" or text_array[x] == "mega":
                            self.ping_in_sound.stop()
                            self.ping_in_sound.play()
                            self.active = 2
                    #checks for two words that together form autocart
                    if self.active > 0 or text_array[x] == "auto":
                        if (self.active > 0 or len(text_array) > x+1 and (text_array[x+1] == "cart" or text_array[x+1] == "part" 
                            or text_array[x+1] == "parts" or text_array[x+1] == "carton" or text_array[x+1] == "kurt" or text_array[x+1] == "card")):
                            #The user can make a full request in one go or two goes, (ie "Auto cart help" or "Auto cart...'ping in'... help")
                            #self.active basically allows the speech to be recongized for one loop after saying auto cart to support this design
                            print("Activated on: " + text)
                            for y in range(x, len(text_array)):
                                if text_array[y] == "terminate":
                                    print("Termination")
                                    #end the ride... do we still want/need this functionality?
                                    break
                                if text_array[y] == "help" or text_array[y] == "stop" or text_array[y] == "emergency":
                                    self.emergency_sound.stop()
                                    self.emergency_sound.play()
                                    time.sleep(2)
                                    print("Emergency Issued")
                                    self.active = 2
                                    self.pullover_pub.publish(True)
                                    break
                                if text_array[y] == "cancel" or text_array[y] == "resume":
                                    print("Emergency Canceled")
                                    self.active = 1
                                    self.pullover_pub.publish(False)
                                    break
                                
                            if self.active > 0:
                                self.active -= 1
                                if self.active <= 0:
                                    self.ping_out_sound.stop()
                                    self.ping_out_sound.play()
                            else:
                                #stop is done first as the previous play must be ended to play again
                                self.ping_in_sound.stop()
                                self.ping_in_sound.play()
                                self.active = 1
                            break

            except Exception as e:
                if self.active > 0:
                    self.active -= 1
                    if self.active <= 0:
                        self.ping_out_sound.stop()
                        self.ping_out_sound.play()
                print("Error in processing speech, typically means there was no registered english speech: " + str(e))
         
         
    def location_speech_callback(self, data):
        if data:
            #send text to server
            self.text_passing = True
        else:
            self.text_passing = False
            #stop sending text to server
            
        
if __name__ == "__main__":
    try:
        speech_recognition_core()
    except rospy.ROSInterruptException:
        pass