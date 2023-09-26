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
import pyaudio



def interruption_action(text):
    if ("Stop" or "Stop.") in text:
        MyAudioreader.speak("Process is stopped")
        value_ia = True
    else:
        value_ia = False
    return value_ia

def confirmation(outputtext):
    check = False
    MyAudioreader.speak("you said")
    MyAudioreader.speak(outputtext)
    MyAudioreader.speak("Was this correct? Please say Yes or No")
    hsr_microphone(4)
    yes_no = Whisper_NLTK_RASA.whisper_decodingnew()
    MyAudioreader.speak("okay")
    print(yes_no)
    if ("Yes." or "Yes" or "Yes?" or "Yes yes") in yes_no:
        print("Yes")
        MyAudioreader.speak("I am going to do the task")
        check = True
    elif ("No." or "No" or "No?" or "No no") in yes_no:
        check = False
        MyAudioreader.speak("Sorry, I did not understand the task. ")
    return check


# was functiontext
## publishes the plan to PlanList
def ProcessTaskTextInput(taskInputText):
    planlist = PlansToBeRun(taskInputText)
    pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10, latch=True) #TODO make sure latch behaves as expected
    pub.publish(planlist)
    print("*Task in progress*")
    Data_entering.CmdIntre(taskInputText) #HERE

frames=[]
record = False

#callback for receiving data from hsr
def callback(data):
    global record
    if record:
        frames.append(data.data)

#### Hsr Listner
def hsr_microphone(p_time):
    global frames
    global record
    #MyAudioreader.speak(texttospeak)
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
    #clear state after recording
    frames = []
    record = False

def hsr_microphone_new(p_time):
    mic_subscriber = rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = p_time
    filename = "output.wav"
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    rospy.loginfo('[MIC] Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    #frames = []  # Initialize array to store frames
    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print('Finished recording')
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames = []

##### Use HSR microphone for speech command

def functionAudio(rec_time):
    rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)
    hsr_microphone(rec_time) #TODO REMOVE TIME SET TO timedaurt
    checkval = False
    try:
        MyAudioreader.speak("Okay. Please give me some time to think about it.")
        outputtext = Whisper_NLTK_RASA.whisper_decodingnew()
        print(outputtext)
        checkval = confirmation(outputtext)

        if checkval == False:
            MyAudioreader.speak("I am sorry I did not understand you correctly.")

        if checkval == True:
            planlist = PlansToBeRun(outputtext)
            pub = rospy.Publisher('PlanList', _nlpCommands.nlpCommands, queue_size=10, latch=True)
            # (rospy.Rate(5)).sleep()
            pub.publish(planlist)
            print("*Task in progress*")
            Data_entering.CmdIntre(outputtext)
    except RuntimeError:
        MyAudioreader.speak("I am sorry I did not understand you correctly.")


def callback(data):
    global record
    if record:
        frames.append(data.data)
#record = False
#frames = []


#rospy.init_node('mic')
#rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)


def start_gpsr():
    rospy.loginfo("[SLP]: starting gpsr...")
    MyAudioreader.speak("Hi I am Toya")
    # wait for starting signal from CRAM
    pubstart = rospy.Publisher('NLPchatter',_nlpCommands.nlpCommands, queue_size=10)
    rospy.loginfo("[SLP]: waiting for starting signal from cram on topic CRAMpub ...")
    cram_sync = rospy.Publisher('NLPfeedback', String, queue_size=10, latch=True)
    cram_sync.publish("start cram")
    counter = 3
    #rospy.Subscriber('/audio/audio', AudioData, callback, queue_size=10)
    while counter >= 0:
        try:
            ready_check = rospy.wait_for_message('CRAMpub', String)
            if ready_check.data == 'START':
                rospy.loginfo("[SLP]: got starting signal: " + ready_check.data)
                break
        except:
            rospy.logwarn("[SLP]: Wrong Starting signal received, try again")
            counter = counter - 1


    pubstart.publish([ready_check.data, 'TASK'])
    rospy.loginfo("[SLP]: done starting gpsr")




