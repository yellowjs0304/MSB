#!/usr/bin/env python
import rospy
import roslib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import String

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	##rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(180)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

#    def shutdown(self):
#        if self.goal_sent:
#            self.move_base.cancel_goal()
#        rospy.loginfo("Stop")
#        rospy.sleep(1)

global s  # departure state variable
s = None

def callback(data):
	global s
	s = data.data

def listener():
	
	rospy.init_node('departure_listener',anonymous=True)
	rospy.Subscriber("MSB__departure",String,callback)

def arriv_pub(data):
	#rospy.init_node('arriv_pub',anonymous=True)
	pub = rospy.Publisher('arrival__MSB',String,queue_size=10)
	arr_st = "%s"%data
	pub.publish(arr_st)


if __name__ == '__main__':
	global s
    	try:
		listener()
		while True:
			if s == '1':
       				navigator = GoToPose()
				break
        	#if s == '1':
        	position1 = {'x': -3.54 ,'y' :5.63 }
		quaternion1 = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
		rospy.loginfo(s)
        	rospy.loginfo("Go to (%s, %s) pose", position1['x'], position1['y'])
        	success = navigator.goto(position1, quaternion1)
		

		position2 = {'x': -9.13 ,'y' : 1.33 }
		quaternion2 = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
        	rospy.loginfo("Go to (%s, %s) pose", position2['x'], position2['y'])
        	success = navigator.goto(position2, quaternion2)
        	

		position3 = {'x': -17.6 ,'y' : 2.08 }
		quaternion3 = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
        	rospy.loginfo("Go to (%s, %s) pose", position3['x'], position3['y'])
        	success = navigator.goto(position3, quaternion3)

		if success:
			rospy.loginfo("Hooray, reached the desired pose")
			while True:
				arriv_pub(2)
				
				listener()
				if s == '3':
					break
        	else:
            		rospy.loginfo("The base failed to reach the desired pose")

			

        	# Sleep to give the last log messages time to be sent
        	rospy.sleep(1)

    	except rospy.ROSInterruptException:
        	rospy.loginfo("Ctrl-C caught. Quitting")

