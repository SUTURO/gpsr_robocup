#!/usr/bin/env python

from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.WhisperNltkRasa import Whisper_NLTK_RASA
from gpsr_robocup.DataEntering import Data_entering
from gpsr_robocup.PlansCheck.plancheck import PlansToBeRun
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String
import wave
from audio_common_msgs.msg import AudioData
import time



def interruption_action(text):
    if ("Stop" or "Stop.") in text:
        MyAudioreader.speak("Process is stopped")
        value_ia = True
    else:
        value_ia = False
    return value_ia

def confirmation(outputtext):
    if interruption_action(outputtext):
        check = 2
    else:
        check = 0
    MyAudioreader.speak("you said")
    MyAudioreader.speak(outputtext)
    k = 1
    while k < 3:
        if check != 2 :
            #MyAudioreader.speak("right? Say yes or no")
            hsr_microphone(6, "right? Say yes or no")
            yes_no = Whisper_NLTK_RASA.whisper_decodingnew()
            MyAudioreader.speak("okay")
            print(yes_no)
            if ("Yes." or "Yes" or "Yes?" or "Yes yes") in yes_no:
                print("Yes")
                MyAudioreader.speak("I am doing the task")
                check = True
                break
            elif ("No." or "No" or "No?" or "No no") in yes_no:
                check = False
                MyAudioreader.speak("Unable to understand")
                break
            else:
                check = False
                MyAudioreader.speak("Unable to understand")
                break
            k += 1
        else:
            break
    return check


# was functiontext
def ProcessTaskTextInput(taskInputText):
    planlist = PlansToBeRun(taskInputText)
    pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10, latch=True) #TODO make sure latch behaves as expected
    pub.publish(planlist)
    print("*Task in progress*")
    Data_entering.CmdIntre(taskInputText) #HERE


##### Use HSR microphone for speech command
def functionAudio(timedaurt):
    #MyAudioreader.speak("Give me the task")
    hsr_microphone(timedaurt,"Give me the task")
    outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
    print(outputtext)
    i = 1
    texttext = outputtext
    while i < 5:
        if outputtext == "...":
            #MyAudioreader.speak("No Voice is detected. Give me the task again")
            MyAudioreader.speak("No Voice is detected. Give me the task in the text form")
            MyAudioreader.speak("type now")
            outputtext = input("Enter the Task : ")
            MyAudioreader.speak('Doing the following task ...')
            MyAudioreader.speak(outputtext)
            ProcessTaskTextInput(outputtext)
            print(outputtext)
            break

        else:
            checkval = confirmation(outputtext)
            if checkval == False:
                #MyAudioreader.speak(" Speak clearly. Give me the task again")
                MyAudioreader.speak(" Give me the task in the text form")
                MyAudioreader.speak("type now")
                outputtext = input("Enter the Task : ")
                MyAudioreader.speak('Doing the following task ...')
                MyAudioreader.speak(outputtext)
                ProcessTaskTextInput(outputtext)
                break
                
            if checkval == True:
                planlist = PlansToBeRun(outputtext)
                pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10)
                (rospy.Rate(5)).sleep()
                pub.publish(planlist)
                print("*Task in progress*")
                Data_entering.CmdIntre(outputtext)
                break
            if checkval == 2:
                break
            i += 1
        if i == 4:
            MyAudioreader.speak("Unable to do the task")





#### Hsr Listner
def hsr_microphone(p_time,texttospeak):

    global frames
    global record
    MyAudioreader.speak(texttospeak)
    record = True
    print('start recording...')
    time.sleep(p_time)
    record = False
    print('recording stop...')
    print(len(frames))
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames = []


def callback(data):
    global record
    if record:
        frames.append(data.data)


record = False
frames = []


#rospy.init_node('mic')
rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)


def start_gpsr():  # 9 june
    rospy.loginfo("[SLP]: starting gpsr...")
    MyAudioreader.speak("Hi I am Toya")
    MyAudioreader.speak("waiting to start...")
    MyAudioreader.speak("please type start... ")
    # wait for starting signal from CRAM
    pubstart = rospy.Publisher('NLPchatter',_nlpCommands.nlpCommands, queue_size=10)
    rospy.loginfo("[SLP]: waiting for starting signal from cram on topic CRAMpub ...")
    cram_sync = rospy.Publisher('NLPfeedback', String, queue_size=10, latch=True)
    cram_sync.publish("start cram")
    counter = 3
    while counter >= 0:
        try:
            ready_check = rospy.wait_for_message('CRAMpub', String)
            if ready_check.data == 'START':
                rospy.loginfo("[SLP]: got starting signal: " + ready_check.data)
                break
        except:
            rospy.roswarn("[SLP]: Wrong Starting signal received, try again")
            counter = counter - 1


    pubstart.publish([ready_check.data, 'TASK'])
    rospy.loginfo("[SLP]: done starting gpsr")




