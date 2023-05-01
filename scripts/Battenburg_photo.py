#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""     Battenburg: Photo -- Version 6.1.4
Last edit:  2023/01/28
Author(s):  Geysen, Steven (SG)
Notes:      - Foto experiment (Herkenbaarheid)
            - Reaction time task for VIAS
            - Release notes:
                * Drop '.jpg'
To do:      - Clean for submission
                * Move settings to top
Comments:   SG: Now saved are
                * 'id' - Pc number and time stamp
                * 'trial' - Trials 0-12 are practice trials
                * 'task' - Button practice, car practice, task
                * 'politie' - Politie, Burger
                * 'type' - Geen, Half, Full, Fed, Brand, Mug
                * 'voertuig' - Voertuig type
                * 'aanzicht' - Voor, Zij, Achter, Isometrisch
                * 'expResp' - Expected response
                * 'rawRT' - Response time, NaN if missed
                * 'actResp' - Pressed button, NaN if missed
                * 'accuracy' - NaN if missed
                * 'missed' - True if participant was slower than 3 seconds
                * 'completed' - True if all trials are done
Sources:    https://www.psychopy.org/online/
            FLatten list of lists: https://stackoverflow.com/a/952952
"""



#%% ~~ Imports ~~ %%#


import os
import random
import time

import numpy as np
import pandas as pd

from pathlib import Path
from psychopy import visual, monitors, core, event


# Directories
SPINE = Path.cwd().parent
STIM_DIR = SPINE / 'stimuli'
INST_DIR = STIM_DIR / 'instructions_feedback'
PRAC_DIR = STIM_DIR / 'car_prac'
TASK_DIR = STIM_DIR / 'car_task'
DATA_DIR = SPINE / 'data'
if not Path.exists(DATA_DIR):
    Path.mkdir(DATA_DIR)



#%% ~~ Functions ~~ %%#


def text_keys(win, text, key_list):
    """
    Display text, key to continue
    Waits forever, or until key is pressed.
    """
    text.draw()
    win.flip()
    event.waitKeys(keyList=key_list)

def display_instructions(win, instruction, filename, key_list):
    """
    Show  instruction slides
    From Esther De Loof and Kate Ergo
    """
    instruction.image = filename
    instruction.draw()
    win.flip()
    event.clearEvents(eventType='keyboard')
    event.waitKeys(keyList=key_list)

def add_itt(data, ppid, trial_nr, task_type):
    """
    Add id, trial number, task type to data frame
    """
    data['id'].append(ppid)
    data['trial'].append(trial_nr)
    data['task'].append(task_type)



#%% ~~ Set-up ~~ %%#
####################


##SG: Set to True when using real participants
Fullscreen = True
## How far is subject from screen (cm)?
PP_DIST = 40
## Response mapping
YES_response = '1'  # Blue
NO_response = '2'  # White
## Durations (s)
TRIAL_DUR = 3
FB_DUR = 1
## PC name
pc_name = os.getlogin()


# Print settings for final check
print(' Laatste check '.center(20, '='))
print('Fullscreen: ', Fullscreen)
print('Knoppen')
print('* BLAUW: ', YES_response)
print('* WIT: ', NO_response)
print('PC naam: ', pc_name)



#%% ~~ Data frame ~~ %%#
#----------------------#


trial_information = [
    'id', 'trial', 'task', 'expResp', 'rawRT', 'actResp', 'accuracy', 'missed'
    ]
##SG: Columns in same order as in stimulus name, for easy loop to store data.
stimulus_information = ['politie', 'type', 'voertuig', 'aanzicht']

column_list = trial_information + stimulus_information
dataDict = {keyi: [] for keyi in column_list}



#%% ~~ Psychopy ~~ %%#
#--------------------#


# Force quit
##SG: In case something somewhere goes wrong
for key in ['escape', 'q']:
    event.globalKeys.add(key, func=core.quit)


# Screen
mon = monitors.Monitor('This screen')
mon.setDistance(PP_DIST)
## How wide is the screen (cm)?
mon.setWidth(38)
## Pixel size
mon.setSizePix((1920, 1080))

win = visual.Window(
    fullscr=Fullscreen, units='norm', monitor=mon, color='#616267'
    )
win.mouseVisible = False


# Data
## Current date
dateStr = time.strftime('%d_%b_%H%M%S', time.localtime())
## New file for every new participant and session
file_name = f'pc{pc_name}_{dateStr}'
pp_file = DATA_DIR/(file_name + '_foto.csv')


# Interaction
conBut = ['space', 'escape', 'q', YES_response]
respBut = [YES_response, NO_response, 'escape', 'q']

# Clock for RT
my_clock = core.Clock()

# On screen text
## Instructions
instruction = visual.ImageStim(
    win, size=(2, 2), image=(INST_DIR/'welkom.png')
    )
## Practice
bpText = visual.TextStim(win, text='Druk ESCAPE.')
## Feedback
feedback = visual.Rect(
    win, width=2, height=2, lineWidth=40, units='norm',
    lineColor='blue', fillColor=None
    )
fb_colours = ['red', 'green']
fbText = visual.TextStim(win, text='Er ging even iets mis')
end = visual.TextStim(win, text='Bedankt voor uw deelname')

# Stimuli 1 
pracList = [filei.name for filei in Path.iterdir(PRAC_DIR)]
stimulus = visual.ImageStim(win, size=(2, 2), image=(PRAC_DIR/pracList[0]))



#%% ~~ Task ~~ %%#
#----------------#


# Fixed practice trials
corresp_buttonPrac = [
    YES_response, NO_response, YES_response,
    YES_response, NO_response, NO_response
    ]
corresp_carPrac = [
    NO_response, NO_response, YES_response,
    NO_response, YES_response, YES_response
    ]


# Randomisation
# -------------

# Group stimili on pattern
civiList = [
    filei.name for filei in Path.iterdir(TASK_DIR)
    if filei.name.upper().startswith('BURGER')
    ]
battList = [
    filei.name for filei in Path.iterdir(TASK_DIR)
    if 'FULL' in filei.name.upper()
    ]
silList = [
    filei.name for filei in Path.iterdir(TASK_DIR)
    if 'SILLITOE' in filei.name.upper()
    ]
halfList = silList + [
    filei.name for filei in Path.iterdir(TASK_DIR)
    if 'HALF' in filei.name.upper()
    ]
noList = [
    filei.name for filei in Path.iterdir(TASK_DIR)
    if not filei.name in (civiList + battList + halfList)
    ]

# Shuffle lists
listList = [civiList, battList, halfList, noList]
for listi in listList:
    random.shuffle(listi)

# Make groups of 4 different stimuli
## Split civilian list in two
civil1 = civiList[:len(civiList)//2]
civil2 = civiList[len(civiList)//2:]

## Alternate Half and Full Battenburg stimuli
balfList = []
for batti, silli in zip(battList, halfList):
    balfList.append([batti, silli])
balfList = [stimi for pairi in balfList for stimi in pairi]

## Select one of each and randomise the order
stimuList = []
for blocki in zip(civil1, civil2, balfList, noList):
    blocki = list(blocki)
    random.shuffle(blocki)
    stimuList.append(blocki)
stimuList = [stimi for blocki in stimuList for stimi in blocki]



#%% ~~ Experiment ~~ %%#
########################


# Greeting and instruction
display_instructions(win, instruction, (INST_DIR/'welkom.png'), conBut)
display_instructions(win, instruction, (INST_DIR/'goal.png'), conBut)

# Button practice
# ---------------
# Instructions
display_instructions(win, instruction, (INST_DIR/'photo_pb.png'), conBut)
# Trial loop
for bp_triali, bp_corresp in enumerate(corresp_buttonPrac):
    ## Add id, trial, task type, and correct response to data frame
    add_itt(dataDict, file_name, bp_triali, 'buttonPrac')
    dataDict['expResp'].append(bp_corresp)
    
    missed = False
    if bp_corresp == YES_response:
        bp_text = 'Druk BLAUW.'
    else:
        bp_text = 'Druk WIT'
    ## Trial text
    bpText.text = bp_text
    bpText.draw()

    event.clearEvents(eventType='keyboard')
    win.flip()
    my_clock.reset()

    # Response and feedback
    ## No time limit for 2 first trials
    if bp_triali < 2:
        wait_dur = float('inf')
        ## Only correct answer to continue
        respList = [bp_corresp, 'escape', 'q']
    else:
        wait_dur = TRIAL_DUR
        ## Also wrong answer to continue possible
        respList = respBut
    resp = event.waitKeys(keyList=respList, maxWait=wait_dur)
    rt = my_clock.getTime()
    ## Determine feedback
    if not resp is None:
        resp = resp[0]
        ## Escape from button practice
        if resp == 'escape':
            break
        else:
            acc = int(resp == bp_corresp)
            feedback.lineColor = fb_colours[acc]
            fbText.text = ''
    else:
        fbText.text = 'U heeft niet snel genoeg gedrukt'
        feedback.lineColor = fb_colours[0]
        rt, resp, acc = np.full((3, ), np.nan)
        missed = True
    # Save trial information
    dataDict['rawRT'].append(rt)
    dataDict['actResp'].append(resp)
    dataDict['accuracy'].append(acc)
    dataDict['missed'].append(missed)
    ## Not available in button practice
    for coli in stimulus_information:
        dataDict[coli].append(bp_text)
    
    # Show feedback
    feedback.draw()
    fbText.draw()
    win.flip()
    time.sleep(FB_DUR)


# Car practice
# --------------
# Instructions
display_instructions(win, instruction, (INST_DIR/'photoprac.png'), conBut)
display_instructions(win, instruction, (INST_DIR/'photoprac2.png'), conBut)
# Trial loop
for cp_triali, cp_respinfo in enumerate(
    zip(pracList, corresp_carPrac), start=len(dataDict['trial'])
    ):
    ## Add id, trial, task type, and correct response to data frame
    add_itt(dataDict, file_name, cp_triali, 'carPrac')
    ## Stimulus information
    cp_stim, cp_corresp = cp_respinfo
    dataDict['expResp'].append(cp_corresp)
    
    missed = False
    stimulus.image = PRAC_DIR / cp_stim
    stimulus.draw()

    event.clearEvents(eventType='keyboard')
    win.flip()
    my_clock.reset()

    # Response and feedback
    ## No time limit for 2 first trials (5+2=7)
    if cp_triali < 8:
        wait_dur = float('inf')
        ## Only correct answer to continue
        respList = [cp_corresp, 'escape', 'q']
    else:
        wait_dur = TRIAL_DUR
        ## Also wrong answer to continue possible
        respList = respBut
    resp = event.waitKeys(keyList=respList, maxWait=wait_dur)
    rt = my_clock.getTime()
    ## Determine feedback
    if not resp is None:
        resp = resp[0]
        ## Escape from button practice
        if resp == 'escape':
            break
        else:
            acc = int(resp == cp_corresp)
            feedback.lineColor = fb_colours[acc]
            fbText.text = ''
    else:
        fbText.text = 'U heeft niet snel genoeg gedrukt'
        feedback.lineColor = fb_colours[0]
        rt, resp, acc = np.full((3, ), np.nan)
        missed = True
    # Save trial information
    dataDict['rawRT'].append(rt)
    dataDict['actResp'].append(resp)
    dataDict['accuracy'].append(acc)
    dataDict['missed'].append(missed)
    ## Not available in photo practice
    for coli in stimulus_information:
        dataDict[coli].append(cp_stim)
    
    # Show feedback
    feedback.draw()
    fbText.draw()
    win.flip()
    time.sleep(FB_DUR)


# Photo task
# ----------
# Instructions
display_instructions(win, instruction, (INST_DIR/'phototask.png'), conBut)
display_instructions(win, instruction, (INST_DIR/'phototask2.png'), conBut)
# Trial loop
for triali, stim in enumerate(stimuList,
start=len(dataDict['trial'])):
    ## Add id, trial, task type, and correct response to data frame
    add_itt(dataDict, file_name, triali, 'main_photo')
    ## Stimulus information
    stinfo = stim.split('_')
    for coli, infoi in zip(stimulus_information, stinfo):
        dataDict[coli].append(infoi.split('.')[0])
    if stinfo[0].upper() == 'POLITIE':
        corresp = YES_response
    else:
        corresp = NO_response
    dataDict['expResp'].append(corresp)
    
    missed = False
    stimulus.image = TASK_DIR / stim
    stimulus.draw()

    event.clearEvents(eventType='keyboard')
    win.flip()
    my_clock.reset()

    # Response and feedback
    resp = event.waitKeys(keyList=respBut, maxWait=TRIAL_DUR)
    rt = my_clock.getTime()
    ## Determine feedback
    if not resp is None:
        resp = resp[0]
        ## Escape from button practice
        if resp == 'escape':
            break
        else:
            acc = int(resp == corresp)
            feedback.lineColor = fb_colours[acc]
            fbText.text = ''
    else:
        fbText.text = 'U heeft niet snel genoeg gedrukt'
        feedback.lineColor = fb_colours[0]
        rt, resp, acc = np.full((3, ), np.nan)
        missed = True
    # Save trial information
    dataDict['rawRT'].append(rt)
    dataDict['actResp'].append(resp)
    dataDict['accuracy'].append(acc)
    dataDict['missed'].append(missed)
    
    # Show feedback
    feedback.draw()
    fbText.draw()
    win.flip()
    time.sleep(FB_DUR)

# Save data
ppdata = pd.DataFrame(dataDict, columns=column_list)
ppdata['completed'] = (
    len(ppdata) == len(corresp_buttonPrac) + len(pracList) + len(stimuList)
    )
ppdata.to_csv(pp_file)

# End
onlyReal = ppdata.iloc[len(corresp_buttonPrac + pracList):]
totacc = onlyReal['accuracy'].sum()
peracc = round((totacc / len(onlyReal) * 100))
meanrt = round(np.nanmean(list(onlyReal['rawRT'])), 3) * 1000
end.text = f'U heeft {peracc}% juist,\nUw gemiddelde reactietijd was {meanrt} ms'
text_keys(win, end, YES_response)

win.close()
core.quit()



# ------------------------------------------------------------------------- End
