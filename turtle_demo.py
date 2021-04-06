#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

from rospeex_if import ROSpeexInterface
import sys, termios, re

a = '9'


rospeex = None
turtle_pub = None

OPERATION_TIME = 100
TARGET_SPEED = 0.2
TARGET_TURN = 0.2

_target_speed = 0.0
_control_speed = 0.0
_target_turn = 0.0
_control_turn = 0.0
_operation_count = 0
_start_flag = False

def set_operation( target_speed, control_speed, target_turn, control_turn ):
    global _target_speed, _control_speed, _target_turn, _control_turn, _operation_count
    _target_speed = target_speed
    _control_speed = control_speed
    _target_turn = target_turn
    _control_turn = control_turn
    _operation_count = 0

def timer_callback(event):
    global _target_speed, _control_speed, _target_turn, _control_turn,  _operation_count, OPERATION_TIME, TARGET_SPEED
    _operation_count += 1
    if _operation_count < OPERATION_TIME:
        turtle_move( _target_speed, _control_speed, _target_turn, _control_turn )
    elif _start_flag == True:
        turtle_move( TARGET_SPEED, TARGET_SPEED, 0, 0 )
    else:
        turtle_move( 0, 0, 0, 0 )

def sr_response(message):
    global TARGET_SPEED, TARGET_TURN, _start_flag, a
    print 'you said : %s' %message
    rule = re.compile(u'(?P<operation>(안녕|손님|점심|고마워|그래))')
    uni_msg = unicode(message, 'utf-8')
    m = rule.match(uni_msg)
    global operation
    if m is not None:
        operation = m.group('operation')
        if operation == u"안녕":
            rospeex.say("누구에게 메세지를 전달할까요?")
            
        elif operation == u"손님":
            rospeex.say("어떤 메세지를 전달할까요?")
            
        elif operation == u"점심":
            rospeex.say("임무를 시작합니다")
	    depart_talker(1) #ok
	#publish to Nav to move
	    #when arrive at user2, subscribe from Nav string '1'	    
	    arr_listener()

        elif operation == u"고마워":#To MSB: ok msg send. MSB: navigation send. break
           rospeex.say("전 돌아가겠습니다")
	   while True:
		2depart_talker(4)
	    	
		2arr_listener()
		
		if a== '5':
			break

            # after arrival from user2, subscribe from Nav string '0'
       #    rospeex.say("메세지 전달을 완료 했습니다")
        elif operation == u"그래":
            rospeex.say("알겠습니다.") 

def callback(data):
	global a
	global operation
	a = data.data
	if a == '2':
		rospeex.say("손님, 식사 하실 시간입니다.")
		rospy.sleep(10)
		while True:
			depart_talker(3)
	elif a == '9':
		rospeex.say("오류 입니다.")

def 2callback(data):
	global a
	global operation
	a = data.data
	if a == '5':
		rospeex.say("메세지 전달을 완료 했습니다")
		rospy.sleep(10)
		while True:
			2depart_talker(6)
	elif a == '9':
		rospeex.say("오류 입니다.")


def arr_listener():
	global a
	#rospy.init_node('arr_listener',anonymous=True)
	rospy.Subscriber('MSB__arrival',String, callback)

def 2arr_listener():
	global a
	#rospy.init_node('arr_listener',anonymous=True)
	rospy.Subscriber('2MSB__arrival',String, 2callback)
	
def depart_talker(data):
        pub = rospy.Publisher('departure__MSB', String, queue_size=10)
        #rospy.init_node('departure_talker', anonymous=True)
        rate = rospy.Rate(10) 
        str="%s"%data
        rospy.loginfo(str)
        pub.publish(str)
        rate.sleep()

def 2depart_talker(data):
        pub = rospy.Publisher('2departure__MSB', String, queue_size=10)
        #rospy.init_node('departure_talker', anonymous=True)
        rate = rospy.Rate(10) 
        str="%s"%data
        rospy.loginfo(str)
        pub.publish(str)
        rate.sleep()


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('main_turtlebot2')
    rospeex = ROSpeexInterface()
    rospeex.init()
    rospeex.register_sr_response( sr_response )
    rospeex.set_spi_config(language='ko',engine='nict')
   
    try:
        rospy.spin();
    except Exception as e:
        print str(e)


    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
