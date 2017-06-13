#!/usr/bin/env python
import roslib
roslib.load_manifest('teleop_twist_keyboard')
import rospy

from std_srvs.srv import Empty as EmptySrv
from bebop_vicon_control.srv import FlyTo

from std_msgs.msg import Empty, String, Float64, Bool
from geometry_msgs.msg import TransformStamped

import thread
turtle_pad_x = 0
turtle_pad_y = 0


def turtle_pad_callback(data):
    global turtle_pad_x, turtle_pad_y
    turtle_pad_x = data.transform.translation.x
    turtle_pad_y = data.transform.translation.y


class Bebop(object):
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self, name):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.name = name
        bebop_ns = name

    def takeoff(self):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        print('**Takeoff**')
        takeoff_call = rospy.ServiceProxy('bebop1/takeoff', EmptySrv)
        takeoff_call()
        return True

    def land(self):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        print('**Landing**')
        land_call = rospy.ServiceProxy('bebop1/land', EmptySrv)
        land_call()
        return True

    def turtlebot_land(self):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        print('**Landing on Turtlebot**')
        land_call = rospy.ServiceProxy('bebop1/turtlebot_land', EmptySrv)
        land_call()
        return True

    def fly_to(self, x, y, z):
        """Return the balance remaining after depositing *amount*
        dollars."""
        theta = 0
        print("fly to " + str(x) + ',' + str(y) + ',' + str(z))
        fly_to_call = rospy.ServiceProxy('bebop1/fly_to', FlyTo)
        response = fly_to_call(x, y, z, theta)
        print(response)
        return response

    def chase(self):
        """Return the balance remaining after depositing *amount*
        dollars."""
        fly_to_call = rospy.ServiceProxy('bebop1/chase', EmptySrv)
        fly_to_call()
        return True


goal_location = None


def publishGoals(goal_location):
    print('Set goal to: ' + str(goal_location))
    pub_x_goal.publish(Float64(goal_location[0]))
    pub_y_goal.publish(Float64(goal_location[1]))
    pub_z_goal.publish(Float64(goal_location[2]))
    pub_yaw_goal.publish(Float64(goal_location[3]))
    pub_enable_goal.publish(Bool(True))


def waitForKeyPress():

    global goal_location, turtle_pad_x, turtle_pad_y

    empty = Empty()
    off = Bool(False)

    # default enable goal False
    pub_enable_goal.publish(off)

    while True:
        key = getKey()
        pub_enable_auto_land.publish(Bool(False))

        if key == '\x03':  # control-c!
            print('### Reset ###')
            goal_location = None
            pub_emergency.publish(empty)
            pub_enable_goal.publish(off)
            break

        elif key == '0':
            print('### Reset ###')
            goal_location = None
            pub_emergency.publish(empty)
            pub_enable_goal.publish(off)

        elif key == '1':
            print('**Takeoff**')
            goal_location = None
            pub_takeoff.publish(empty)
            pub_enable_goal.publish(off)

        elif key == '2':
            print('**Landing**')
            goal_location = None
            pub_land.publish(empty)
            pub_enable_goal.publish(off)

        elif key == '3':
            goal_location = [-1.0, 1.0, 0.75, 1]
            publishGoals(goal_location)

        elif key == '4':
            goal_location = [-1.0, 1.0, 1.3, 1]
            publishGoals(goal_location)

        elif key == '5':
            goal_location = [turtle_pad_x, turtle_pad_y, 0.8, 0]
            pub_enable_auto_land.publish(Bool(True))
            publishGoals(goal_location)

        elif key == '6':
            goal_location = [-0.25, -0.25, 1.3, 1]
            publishGoals(goal_location)

        elif key == '7':
            goal_location = [-0.25, 0.25, 1.3, 1]
            publishGoals(goal_location)


if __name__ == "__main__":

    rospy.init_node('bebop_api')

    bebop1 = Bebop('bebop1')

    rospy.spin()

    # thread.start_new_thread(waitForKeyPress, ())

    # bebop_ns = rospy.get_param("/bebop_ns")

    # settings = termios.tcgetattr(sys.stdin)

    # sub_pad = rospy.Subscriber(
    #     "vicon/turtle_pad/turtle_pad", TransformStamped, turtle_pad_callback)
    #
    # pub_x_goal = rospy.Publisher(
    #     bebop_ns + '/setpoint/x', Float64, queue_size=10)
    # pub_y_goal = rospy.Publisher(
    #     bebop_ns + '/setpoint/y', Float64, queue_size=10)
    # pub_z_goal = rospy.Publisher(
    #     bebop_ns + '/setpoint/z', Float64, queue_size=10)
    # pub_yaw_goal = rospy.Publisher(
    #     bebop_ns + '/setpoint/yaw', Float64, queue_size=10)
    # pub_enable_goal = rospy.Publisher(
    #     bebop_ns + '/setpoint/enable', Bool, queue_size=10)
    # pub_takeoff = rospy.Publisher(bebop_ns + '/takeoff', Empty, queue_size=10)
    # pub_land = rospy.Publisher(bebop_ns + '/land', Empty, queue_size=10)
    # pub_emergency = rospy.Publisher(bebop_ns + '/reset', Empty, queue_size=10)
    #
    # pub_enable_auto_land = rospy.Publisher(bebop_ns + '/setpoint/enable_auto_land',
    #                                        Bool, queue_size=10)
    # waitForKeyPress()

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
