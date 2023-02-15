#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
from subprocess import Popen
import os
import signal
import ctypes
import random
import csv
import time
from pprint import pprint
import pandas as pd
##########################################################

###############
# Wim Pouw (wim.pouw@donders.ru.nl)
# This script generates a stimulilist

##################################debugging 
#(if debugging than we do no start all streams)
debugging = True

##################################general variables
timepress_but = []
butvalue = []
buticon = []
trialnum = []

##################################Folders to save to
motfol = os.getcwd()
	#outputfolder
output = motfol+'/stimuli_lists/'

#### add participant number
ppn             = input("ppn: ")
print('Participant number and random seed: ' + ppn)
repetitions            = input("how many repetitions: ")
print('Number of repetitions per movement condition: ' + repetitions)
random.seed(ppn)
repetitions = int(repetitions)
##################################Conditions and settings experiment
#repetitions = 10						#how many times they do the same trial (we will do 5)
#conditions_voc = ['expire', 'vocalize']
conditions_mov = ['no_movement', 'internal_rotation_stop', 'external_rotation_stop', 'extension_stop',  'flexion_stop'] 
#conditions_weight = ['no_weight', 'weight']
trialtotal = repetitions*len(conditions_mov)

########################################create a triallist for exp with blocks of condition weights nd vocalization (and randomized order for movement conditions)
#list of variables plus calibration trials

trialn = ['trialnumber', 'practice1', 'practice2', 'practice3', 'practice4', 'practice5']
#condition_voc = ['condition_voc', 'vocalize', 'vocalize','vocalize', 'vocalize', 'vocalize']
#condition_weight = ['no_weight','no_weight', 'no_weight', 'no_weight', 'no_weight', 'no_weight']
condition_mov = ['condition_movement', 'no_movement', 'flexion_stop', 'extension_stop', 'internal_rotation_stop', 'external_rotation_stop']
trialtype = ['trialtype', 'practice', 'practice', 'practice', 'practice', 'practice']
trnums = len(trialn)

trialsmov = []
trialst= []
for i in range(0, trialtotal):
    trialn.extend([str(i)])
    trialsmov.extend(conditions_mov)
    for j in range(0, len(conditions_mov)):
        trialst.extend(['main'])

#randomize the list
random.shuffle(trialsmov)

#add to the variables
condition_mov.extend(trialsmov)
trialtype.extend(trialst)

 
	#lets open a csv file to write the triallist as a blank file to the blank file list
fileto = open(output + 'blank/traillist_'+ppn+'.csv', 'w+', newline='')
with fileto:
    write = csv.writer(fileto, delimiter = ',')
    for i in range(0, trialtotal+trnums):
        write.writerow([trialn[i], condition_mov[i], trialtype[i]])