#!/usr/bin/env python

## GPSR NLP commands interpretation
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
import rospy
from std_msgs.msg import String, Int32MultiArray
from gpsr_robocup import _nlpCommands

def Plansorting(sentence_plan):
    planinfo1 = sentence_plan
    plan1 = planinfo1[0]
    parameters1 = planinfo1[1]
    objectname = 'nil'
    objecttype = 'nil'
    locations = []
    rooms = []
    personname = 'nil'
    persontype = 'nil'
    personaction = 'nil'
    features = 'nil'
    color = 'nil'
    number = 'nil'
    from_location = 'nil'
    to_location = 'nil'
    from_room = 'nil'
    to_room = 'nil'
    for element in parameters1:
        pr_name = parameters1[element][0]
        pr_value = parameters1[element][1]
        if pr_name == 'object':
            objectname = pr_value
        if pr_name == 'object category':
            objecttype = pr_value
        if pr_name == 'location':
            locations.append(pr_value)
        if pr_name == 'room':
            rooms.append(pr_value)
        if pr_name == 'person name':
            personname = pr_value
        if pr_name == 'person':
            persontype = pr_value
        if pr_name == 'attributes':
            features = pr_value
        if pr_name == 'gestures':
            personaction = pr_value
        if pr_name == 'colours':
            color = pr_value
        if pr_name == 'number':
            number = pr_value
    if len(locations) == 1:
        from_location = locations[0]
    if len(locations) == 2:
        from_location = locations[0]
        to_location = locations[1]
    if len(rooms) == 1:
        from_room = rooms[0]
    if len(rooms) == 2:
        from_room = rooms[0]
        to_room = rooms[1]

    return [plan1, objectname, objecttype, personname, persontype, features, personaction, color, number, from_location,
            to_location, from_room, to_room]

# publishes detailed plan
def planseparator(text):
    pub = rospy.Publisher('Planchatter', _nlpCommands.nlpCommands, queue_size=10, latch=True)
    sorted_plan = Plansorting(text)
    print(sorted_plan)
    pub.publish(sorted_plan) #publishes full plan list
    plan_name = sorted_plan[0]
    rospy.loginfo("[Planseparator]: plan name: " + plan_name)
    return (plan_name)

def SpeechToCram(text):
    rospy.loginfo("[SpeechToCRAM]: input: " + text)
    text_plan = Whisper_NLTK_RASA.planinterpreter(text)  ## text to data labeling
    print(text_plan)
    for plan_count in range(len(text_plan)): #?!?
        if plan_count > 0:
            text = text_plan[plan_count]
            planseparator(text)




# TODO: wth???
def CmdIntre(text):
    rospy.loginfo("[CmdIn]: " + text)
    plansToBePerformed = [text]
    for q in range(len(plansToBePerformed)):
        print(plansToBePerformed[q])
        SpeechToCram(plansToBePerformed[q])
