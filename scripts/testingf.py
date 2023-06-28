#!/usr/bin/env python
from gpsr_robocup.Audioreader import MyAudioreader
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import ProcessTaskTextInput
from gpsr_robocup.Audioreader.SpeechLanguageInterpretator import start_gpsr
from gpsr_robocup import _nlpCommands
import rospy
from std_msgs.msg import String

########################## MAIN CODE TEXT ##########################################
#rospy.init_node("NLP_node")

#MyAudioreader.speak("Enter the total number of tasks")  ## 9 june
#gpsrstage1 = int(input("Enter the total number of task: "))  ### INPUT set number of challanges

#start_gpsr()  # 9 june
#MyAudioreader.speak("Text mode is activated... ")  # 9june
#MyAudioreader.speak("Performing GPSR challange ...")  ## 9 june
#MyAudioreader.speak("Please enter the task ...")  ## 9 june


# MyAudioreader.speak("hello i am H S R")
# MyAudioreader.speak("Text mode is activated... ")
# gpsrstage1  = int(input("Enter the total number of task: ")) ### INPUT set number of challanges

# list_cmnds = ['fetch a bowl','place the bowl', 'drop the spoon'] ### for 3 commands
# global variables
CmndNum = 0
gpsrstage1 = ''

class text_input:
    def __init__(self, text_cmd, num_tx):
        self.text_cmd = text_cmd
        self.num_tx = num_tx


def taking_input(number):
    MyAudioreader.speak("Enter the task now")
    task_1 = input("Enter the Task " + str(number) + " :")
    MyAudioreader.speak('Doing the following task ...')
    MyAudioreader.speak(task_1)
    # send the typed in text to be processed
    ProcessTaskTextInput(task_1)

# function which waits for the Feedback from CRAM, if a task was performed or not
def callback(data):
    checktask = data.data
    rospy.loginfo("[NLP] CRAM Feedback received: " + data.data)
    print('******')
    if checktask == 'DONE' or checktask == 'FAIL':
        print('TASK : ' + checktask)
        if CmndNum <= gpsrstage1 - 1:
            MyAudioreader.speak("Give me the new task")
            print('------Next Task-----')
            #taking_input(CmndNum + 1)
        else:
            print('-----All Commands are Done-----')

    else:
        rospy.loginfo("[NLP] Didn't understand the feedback. Checktask: " + checktask)





if __name__== "__main__":
    try:
        rospy.init_node("NLP_node")
        rospy.loginfo("[NLP]: startup...")
        MyAudioreader.speak("Enter the total number of tasks")

        rospy.loginfo("[NLP]: Enter the total number of tasks (3 for stage1) (5 for stage2).")

        # gpsrstage1 = int(input("Enter the total number of task: "))  ### INPUT set number of challanges from command line

        counter = 3
        while counter >= 0:
            try:
                rospy.loginfo("[NLP]: Waiting for CRAMpub....")
                gpsrstage1 = rospy.wait_for_message("CRAMpub", String)
                gpsrstage1 = int(gpsrstage1.data)
                break
            except ValueError:
                rospy.logwarn("[NLP]: wrong intput. expected int, got string. Please try again")
                counter = counter - 1
                rospy.sleep(1)

        #ensure first input is a number

        rospy.loginfo("[NLP]: amount of tasks to be received: " + str(gpsrstage1))
        start_gpsr()

        # here starts the loop for the amount of tasks
        while not rospy.is_shutdown() and gpsrstage1 != 0:
            rospy.loginfo("[NLP]: Start task")
            CmndNum = CmndNum + 1
            taking_input(CmndNum)
            rospy.loginfo("[NLP]: Waiting for Feedback from CRAM ...")
            cram_feedback = rospy.wait_for_message("CRAMpub", String)
            rospy.loginfo("[NLP]: Got feedback from CRAM. Task was: " + cram_feedback.data)
            callback(cram_feedback)
            gpsrstage1 = gpsrstage1 - 1
            rospy.loginfo("[NLP]: Done.")

        rospy.loginfo("[NLP]: Done with all tasks")

    except rospy.ROSInterruptException:
        pass
