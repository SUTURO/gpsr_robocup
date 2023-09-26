#!/usr/bin/env python

from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import functionAudio
from gpsr_robocup import _nlpCommands
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import start_gpsr
import rospy
from std_msgs.msg import String

# probably no longer used?
def callback(data):
    checktask = data.data
    global CmndNum
    print('******')
    if checktask == 'DONE' or checktask == 'FAIL':
        print('TASK : ' + checktask)
        CmndNum = CmndNum + 1
        print(CmndNum)
        if CmndNum <= gpsrstage1-1:
            print('------Next Task-----')
            functionAudio(15)
        else:
            print('-----All Commands are Done-----')
           # MyAudioreader.speak("All" + str(gpsrstage1) + " task are done")

    else:
        print(checktask)

#very ugly
cram_state = ""
def cram_msgs(data):
    cram_state = data.data

########################## MAIN CODE Audio ##########################################
if __name__ == "__main__":
    try:
        rospy.init_node("NLP_Whisper_node")
        gpsrstage1  = 10 #TODO make better #int(input("Enter the total number of task: ")) ### INPUT set number of challanges
        cram_sub = rospy.Subscriber('/CRAMpub', String, cram_msgs, queue_size=10)

        MyAudioreader.speak("Speech Mode is activated")
        CmndNum = 0 # no idea what this does tbh
        while not rospy.is_shutdown():
            rospy.loginfo("[NLP-W]: Waiting for listening signal ...")
            cram_feedback = rospy.wait_for_message("CRAMpub", String)
            #rospy.Subscriber('/CRAMpub', String, cram_msgs, queue_size=10)
            if cram_feedback.data == "Listen":
            #if cram_sub.data == "Listen":
                MyAudioreader.speak("Please tell me what to do")
                functionAudio(7)

            #rospy.loginfo("[NLP-W]: waiting to listen.")

        #rospy.spin()

    except rospy.ROSInterruptException:
        pass




