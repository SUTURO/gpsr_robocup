#!/usr/bin/env python3

import hsrb_interface

robot = hsrb_interface.Robot()
tts = robot.get('default_tts')
tts.language = tts.ENGLISH
tts.say(u'')

