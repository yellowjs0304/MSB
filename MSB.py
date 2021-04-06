#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import roslib
from std_msgs.msg import String

a='99'

def callback(data):
	global a
	a = data.data

#----------------------Subscibe1----------------------

def listener1():  # demo-->MSB
	global a
	#rospy.init_node('departure_listener',anonymous=True)
	rospy.Subscriber("departure__MSB",String,callback)

def listener2():  # go-->MSB 
	global a
	#rospy.init_node('arr_listener',anonymous=True)
	rospy.Subscriber('arrival__MSB',String, callback)

#----------------------Subscibe2----------------------

def 2listener1():  # demo-->MSB
	global a
	#rospy.init_node('departure_listener',anonymous=True)
	rospy.Subscriber("2departure__MSB",String,callback)

def 2listener2():  # go-->MSB 
	global a
	#rospy.init_node('arr_listener',anonymous=True)
	rospy.Subscriber('2arrival__MSB',String, callback)


#----------------------Publish1----------------------

def talker1(data):  # MSB-->go 
        pub = rospy.Publisher('MSB__departure', String, queue_size=10)
        #rospy.init_node('departure_talker', anonymous=True)
        rate = rospy.Rate(10) 
	str="%s"%data
        rospy.loginfo(str)
        pub.publish(str)
        rate.sleep()

def talker2(data):  # MSB-->demo
	#rospy.init_node('arriv_pub',anonymous=True)
	pub = rospy.Publisher('MSB__arrival',String,queue_size=10)
	str="%s"%data
	pub.publish(str)

#----------------------Publish2----------------------

def 2talker1(data):  # MSB-->go 
        pub = rospy.Publisher('2MSB__departure', String, queue_size=10)
        #rospy.init_node('departure_talker', anonymous=True)
        rate = rospy.Rate(10) 
	str="%s"%data
        rospy.loginfo(str)
        pub.publish(str)
        rate.sleep()

def 2talker2(data):  # MSB-->demo
	#rospy.init_node('arriv_pub',anonymous=True)
	pub = rospy.Publisher('2MSB__arrival',String,queue_size=10)
	str="%s"%data
	pub.publish(str)





if __name__ == '__main__':
	global a
	rospy.init_node('MSB')
	
	try:
		while True:
			listener1()
			print a
			talker1(a)
			
			listener2()
			print a
			if a == '2':
				while True:
					talker2(a)
				
					listener1()
					if a== '3':
						while True:
							talker1(a)
		#go end------------------------------------------------------------------
			
		2listener1()
		if a == '4':
			while True:
				2talker1(a)
		
				2listener2() #navi success
				if a== '5':
					while True:
						2talker2(a) #send demo '5'
						
						2listener1()
						if a== '6':
							while True:
								
				
					
		#while True:
		#	talker2(a)
		#	
		#	listener3()
		#	print a
		#	if a == '3':
		#	 	talker3(a)
		#		break

		#while True:
		#	print a
		#	talker
	

		#while True:
		#	listener3()
		#	if a == '7':
		#		talker3(a)
		#		break

	except rospy.ROSInterruptException:
        	rospy.loginfo("Ctrl-C caught. Quitting")
	
