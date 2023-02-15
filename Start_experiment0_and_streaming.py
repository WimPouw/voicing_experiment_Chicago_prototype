#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import os
import csv
import pandas as pd

###############
# Wim Pouw (wim.pouw@donders.ru.nl)

##################################debugging
#(if debugging than we do no start all streams)
debugging = False

##################################general variables
timepress_but = []
butvalue = []
buticon = []
trialnum = []

##################################Folders to save to
motfol = os.getcwd()
    #outputfolder
output = motfol+'/output_files/'                           #where do the written files go (and where are the blank traillist)
movstimvidfol = "./stimuli_videos/motions_example_masked/" #videos for the movement

#general info ask before experiment
ppn                = input("ppn: ")

#example movements
def getexampleevid(conditionmov):
    movstimvids = {'flexion_stop': os.path.join(motfol,movstimvidfol+"flexion_vocalize"+".mp4"),
                'extension_stop': os.path.join(motfol, movstimvidfol+"extension_vocalize"+".mp4"),
                'external_rotation_stop': os.path.join(motfol,movstimvidfol+"external_vocalize"+".mp4"),
                'internal_rotation_stop': os.path.join(motfol,movstimvidfol+"internal_vocalize"+".mp4"),
                'no_movement': os.path.join(motfol, movstimvidfol+"nomovement_vocalize"+".mp4")}
    return(movstimvids[conditionmov])

############Experiment texts
#newscreen
starttext0 = 'Prese "N" to proceed, press "C" to repeat a trial, press F1 to quit experiment'

#make a window
win = visual.Window([1900, 1050], fullscr= False, units = 'pix', color = 'white')
#Start screen with starttext0
startscreen0 = visual.TextStim(win, text = starttext0, color = 'black')
startscreen0.draw()
win.flip()

####################################Screen texts procedure
def trialstartmultimedia(videop, text, positiontext):
    """We here have a trial with an example movement shown as mp4 and some text. When 'C' is pressed
    it should go towards a recording trial
    """
    trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = text, color= 'black', pos=positiontext)
    vid = visual.VlcMovieStim(win, videop, loop=True, pos=(150,50), size = (720/2, 1280/2))
    continueloop = True
    while continueloop:
        keys = event.getKeys()
        vid.draw()
        trialscreen.draw()
        win.flip()
        #pprint(dir(visual.VlcMovieStim))
        check = round(vid.getPercentageComplete())
        if check > 85: #if video is 85% completed set up video again
            vid.loadMovie(videop)
        if 'n' in keys:
            continueloop = False


def getinposition(movcon):
    """We here have a trial with an example movement shown as mp4 and some text. When 'C' is pressed
    it should go towards a recording trial
    """
    pressednprev = True
    trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = 'Get in \n this position', color= 'black', pos=(-300,0))
    im = visual.ImageStim(win, os.path.join(motfol+'/stimuli_images/getready/getready_'+movcon+'.PNG'), pos=(150,50), size = (720/2, 1280/2))
    trialscreen.draw()
    im.draw()
    win.flip()
    event.waitKeys(keyList=['n']) #ait for n is pressed

def inhale(movcon):
    timer = core.Clock()
    timer.add(3) #inhalation time is set a little shorter
    curtime = timer.getTime()
    pressednprev = True
    im = visual.ImageStim(win, os.path.join(motfol+'/stimuli_images/getready/getready_'+movcon+'.PNG'), pos=(150,50), size = (720/2, 1280/2))
    while True:
        if timer.getTime() < 0:
            trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = 'inhale \n\n' 'We start in: ' + str(round(timer.getTime())), color= 'black', pos=(-300,100))
            trialscreen.draw()
            im.draw()
            win.flip()
        if timer.getTime() > 0:
            break

def dovoc(movcon):
    timer = core.Clock()
    timer.add(3)
    curtime = timer.getTime()
    pressednprev = True
    im = visual.ImageStim(win, os.path.join(motfol+'/stimuli_images/vocalize'+'/'+movcon+'.PNG'), pos=(150,50), size = (720/2, 1280/2))
    while True:
        if timer.getTime() < 0:
            trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = 'vocalize' + ' NOW!', color= 'black', pos=(-300,100))
            trialscreen.draw()
            im.draw()
            win.flip()
        if timer.getTime() > 0:
            break

def domov(movcon):
    im = visual.ImageStim(win, os.path.join(motfol+'/stimuli_images/movements/'+movcon+'_vocalize'+'.PNG'), pos=(150,50), size = (720/2, 1280/2))
    timer = core.Clock()
    timer.add(4)
    curtime = timer.getTime()
    while True:
        if timer.getTime() < 0:
            trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = 'And move NOW!', color= 'black', pos=(-300,100))
            if movcon == "no_movement":
                trialscreen = visual.TextStim(win, font = 'Arial', height=40, text = 'Stay in position', color= 'black', pos=(-300,100))
            trialscreen.draw()
            im.draw()
            win.flip()
        if timer.getTime() > 0:
            break

def homescreen(trn, cmov, trialt, fontsz):
    text1 = "UPCOMING TRIAL" + '\n\n' + \
    'Trialtype:  '             + trialt + '\n' +\
    'trial number:  '         + trn + '\n' + \
    'Condition movement:  '    + cmov
    startscreen1 = visual.TextStim(win, font = 'Arial', height=fontsz, text = text1, color= 'red', pos=(0,0))
    startscreen1.draw()
    win.flip()

##################################experiment run
fileto = open(output + '/traillist_'+ppn+'.csv', 'w+', newline='')
with fileto:
    write = csv.writer(fileto, delimiter = ';')
    write.writerow(['timestamp', 'trialindex', 'trial', 'trialstarted','trialended', 'duration','trial_type', 'button_pressed',
     'pressed_icon', 'sample_button', 'movement_condition'])


trialdframe = pd.read_csv('./stimuli_lists/blank/traillist_'+ppn+'.csv')

keypress = event.waitKeys(keyList=['n']) #space will start the experiment
trial = 0

myClock = core.Clock()
while True:
    pressedn = False
    pressedc = False
    #get a key press from the button box or an exit key 'f1'
    keypress2 = event.getKeys(keyList=['f1', 'c', 'n']) #exit

    if (keypress2 == 'f1'):
        break

    #This will allow us to repeat a trial
    if (keypress2 == 'c') & (pressedc == False):
        pressedc = True
        trial = trial - 1
        #calibration respiration

    #collect trialinfo
    curtrialnum =     str(trialdframe['trialnumber'][trial])
    curconmov   =     str(trialdframe['condition_movement'][trial])
    curcontype     =     str(trialdframe['trialtype'][trial])

    #standard start window that shows the weight condition
    #if (keypress2 == "n"):
    #    pressedn = False #this means there was no c pressed
        #home screen
        #standard start window
    homescreen(curtrialnum, curconmov, curcontype, 30)

    #get into the main trials
    if event.waitKeys(keyList=['n']):
        pressedn = True
        trial = trial + 1
        print('test')
        #if calibration is
        if curcontype == 'practice':
            trialstart = myClock.getTime()
            getreadytovocmov = "PRACTICE\n\n\n Get ready \n and do this: \n " + curconmov
            trialstartmultimedia(videop = getexampleevid(curconmov), text= getreadytovocmov, positiontext= (-300,0))
            getinposition(curconmov)
            inhale(curconmov)
            trialstart = myClock.getTime() #we sample from the inlet to get the trial end info
            dovoc(curconmov)
            domov(curconmov)
            trialend = myClock.getTime() #we sample from the inlet to get the trial end info
            duration = trialend-trialstart
        if curcontype == 'main':
            getreadytovocmov = "Get ready and do this " +curconmov
            trialstartmultimedia(videop = getexampleevid(curconmov), text= getreadytovocmov, positiontext= (-300,0))
            getinposition(curconmov)
            inhale(curconmov)
            #when they start vocalizing that is the trialstart
            trialstart = myClock.getTime() #we sample from the inlet to get the trial end info
            dovoc(curconmov)
            domov(curconmov)
            trialend = myClock.getTime() #we sample from the inlet to get the trial end info
            duration = trialend-trialstart
        #save the row of info

        #open file for saving experimentinfo
        fileto = open(output + 'traillist_'+ppn+'.csv', 'a', newline='')
        with fileto:
            write = csv.writer(fileto, delimiter = ',')
            write.writerow([trial, curtrialnum, trialstart, trialend, duration, curcontype,
                curconmov])

#wrapping up
win.close() #close psychopy window
core.quit() #close psychopy core
fileto.close()
