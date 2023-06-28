#!/usr/bin/env python

from gpsr_robocup.DataEntering.Data_entering import CmdIntre
import rospy
from std_msgs.msg import String
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup import _nlpCommands

checkvar = ""

def Task_Update_to_CRAM(text):
    pubwords = rospy.Publisher('NLPchatter', _nlpCommands.nlpCommands, queue_size=10, latch=True)
    #(rospy.Rate(5)).sleep()
    for i in range(1): pubwords.publish([text, 'Task'])


def callback2(data2):
    #global checkvar
    checkvar = data2.commands
    rospy.loginfo("command received")


global cram_speaker
cram_speaker = []


def callback(data):
    rospy.loginfo("data received: " + data.data)
    cram_cmd = data.data
    planlist = checkvar
    if cram_cmd == 'done':
        print('----')
        print(cram_cmd)
        print('----')
    elif cram_cmd == 'fail':
        print('----')
        print(cram_cmd)
        print('----')
        MyAudioreader.speak("Unable to do the task")
        Task_Update_to_CRAM('Fail')
        cram_speaker.clear()
    if cram_cmd in planlist:
        cram_speaker.append(cram_cmd)
        print(cram_speaker)
    if (cram_speaker == planlist) and not (cram_cmd == 'fail'):
        MyAudioreader.speak("I have done the task")
        MyAudioreader.speak("Going back to initial position")
        Task_Update_to_CRAM('Done')
        cram_speaker.clear()


if __name__== "__main__":
    try:
        rospy.init_node('CRAM_listener', anonymous=True)
        rospy.loginfo("[CL]: CRAM Listener Initializing....")
        cram_listner = rospy.Subscriber('CRAMpub', String, callback)
        cram_listner = rospy.Subscriber('PlanList', _nlpCommands.nlpCommands, callback2)
        rospy.loginfo("[CL]: CRAM Listener Initialized")
        rospy.spin()
    except rospy.ROSInterruptException:
        pass



