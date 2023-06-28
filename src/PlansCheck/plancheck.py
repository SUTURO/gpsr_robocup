#!/usr/bin/env python
import rospy
from gpsr_robocup.DataEntering import Data_entering
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA

def PlansToBeRun(text):
    # returns list of plans (CRAM terminology)
    rospy.loginfo("[PLanList]: received data: " + text)
    myplanss = Whisper_NLTK_RASA.planinterpreter(text)
    print(myplanss)
    plannames = []
    for i in range(len(myplanss)):
        if i > 0:
            plannames.append(myplanss[i][0])
    rospy.loginfo("[PlanList]: plan list: " + ''.join(plannames))
    return plannames
