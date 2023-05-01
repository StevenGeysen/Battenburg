#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""     Battenburg: Film -- Version 6.2.1
Last edit:  2023/01/28
Author(s):  Geysen, Steven (SG)
Notes:      - Video experiment (Opvallendheid)
            - Reaction time task for VIAS
            - Release notes:
                * Fixed end feedback
                * Drop '.mp4'
To do:      - Fullscreen = True
Comments:   SG: Now saved are
                * 'id' - Pc number and time stamp
                * 'trial' - Trials 0-6 are practice trials
                * 'task' - Film practice, task
                * 'scenarioID' - Scenario identification
                * 'persepctief' - Car or pedestrian
                * 'versie_politie' - Half, Full, Klassiek
                * 'zwaailicht' - Zwaailicht of niet
                * 'omgeving' - Ruraal, stedelijk, snelweg
                * 'zicht' - Voorruit, spiegel, voet
                * 'zijde_zichtbaar' - zij, voor, achter
                * 'beweging' - Beweegt de wagen?
                * 'scenario' - Scenario
                * 'lichtconditie' - Dag of nacht
                * 'rawRT' - Response time, NaN if missed
                * 'actResp' - Actual response
                * 'missed' - True if participant was slower than 3 seconds
                * 'completed' - True if all trials are done
Sources:    https://www.psychopy.org/online/
            https://discourse.psychopy.org/t/movie-doesnt-play/8103
"""



#%% ~~ Imports ~~ %%#


import os
import time

import numpy as np
import pandas as pd

from pathlib import Path
from psychopy import visual, monitors, core, event


# Directories
SPINE = Path.cwd().parent
STIM_DIR = SPINE / 'stimuli'
INST_DIR = STIM_DIR / 'instructions_feedback'
PRAC_DIR = STIM_DIR / 'film_prac'
TASK_DIR = STIM_DIR / 'film_task'
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

def text_time(win, text, duration):
    """
    Display text, time to continue
    Waits as long as given in duration.
    """
    text.draw()
    win.flip()
    core.wait(duration)

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
    Add id, trial number, and task type to data frame
    """
    data['id'].append(ppid)
    data['trial'].append(trial_nr)
    data['task'].append(task_type)



#%% ~~ Set-up ~~ %%#
####################


##SG: Set to True when using real participants
Fullscreen = False
## How far is subject from screen (cm)?
PP_DIST = 40
## Response mapping
##SG: For now: left-f-yes
YES_response = '1'
## Feedback duration (s)
FB_DUR = 1
## PC name
pc_name = os.getlogin()


# Print settings for final check
print(' Laatste check '.center(20, '='))
print('Fullscreen: ', Fullscreen)
print('BLAUW: ', YES_response)
print('PC naam: ', pc_name)



#%% ~~ Data frame ~~ %%#
#----------------------#


trial_information = ['id', 'trial', 'task', 'rawRT', 'actResp', 'missed']
##SG: Columns in same order as in stimulus name, for easy loop to store data.
stimulus_information = [
    'scenarioID', 'perspectief', 'versie_politie', 'zwaailichten', 'omgeving',
    'zicht', 'zijde_zichtbaar', 'beweging', 'scenario', 'lichtconditie'
    ]

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
pp_file = DATA_DIR / (file_name + '_film.csv')


# Interaction
conBut = ['space', 'escape', YES_response]

# Clock for RT
my_clock = core.Clock()

# On screen text
## Instructions
instruction = visual.ImageStim(
    win, size=(2, 2), image=(INST_DIR / 'welkom.png')
    )
## Buffer
bufferText = visual.TextStim(win, text='+')
loadText = visual.TextStim(
    win, text='Even geduld, het experiment wordt voorbereid!'
    )
## Feedback
feedback = visual.Rect(
    win, width=2, height=2, lineWidth=20, units='norm',
    lineColor='blue', fillColor=None
    )
fbText = visual.TextStim(win, text='Er ging even iets mis')
end = visual.TextStim(win, text='Bedankt voor uw deelname')

# Stimuli
pracList = [filei.name for filei in Path.iterdir(PRAC_DIR)]
stimuList = [filei.name for filei in Path.iterdir(TASK_DIR)]
np.random.shuffle(stimuList)

stimulus = visual.VlcMovieStim(
    win, (PRAC_DIR / pracList[0]), noAudio=True, autoStart=True,
    units='norm', size=(2, 2)
    )



#%% ~~ Experiment ~~ %%#
########################


# Greeting and instruction
display_instructions(win, instruction, (INST_DIR / 'welkom.png'), conBut)
display_instructions(win, instruction, (INST_DIR / 'goal.png'), conBut)

# Film practice
# -------------
# Instructions
display_instructions(win, instruction, (INST_DIR / 'filmprac.png'), conBut)
## Transition
text_time(win, bufferText, 2)
# Trial loop
for fp_triali, fp_stim in enumerate(pracList):
    # Add trial information to data frame
    ## Id, trial, and task type
    add_itt(dataDict, file_name, fp_triali, 'filmPrac')
    ## Stimulus information not available in photo practice
    for coli in stimulus_information:
        dataDict[coli].append(fp_stim)
    
    ## Default values
    missed = False
    resp = None
    rt = np.nan
    
    ## Prepare stimulus
    stimname_full = PRAC_DIR / fp_stim
    stimulus.filename = stimname_full
    stimulus.loadMovie(stimname_full)
    
    ## Prepare data collection
    event.clearEvents(eventType='keyboard')
    my_clock.reset()
    # Play stimulus
    while not stimulus.isFinished:
        stimulus.draw()
        win.flip()
        ## Quit
        if event.getKeys('escape'):
            stimulus.stop()
            core.quit()
        ## Response time
        elif event.getKeys(YES_response):
            rt = my_clock.getTime()
            resp = YES_response
            
            stimulus.stop()
            fbText.text = ''
            feedback.lineColor = 'green'
    ## No response
    if resp is None:
        missed = True
        resp = np.nan

        stimulus.stop()
        fbText.text = 'U heeft niet snel genoeg gedrukt'
        feedback.lineColor = 'red'
    # Save trial information
    dataDict['rawRT'].append(rt)
    dataDict['actResp'].append(resp)
    dataDict['missed'].append(missed)

    # Show feedback
    feedback.draw()
    fbText.draw()
    win.flip()
    time.sleep(FB_DUR)


# Film task
# ---------
# Instructions
display_instructions(win, instruction, (INST_DIR/'filmtask.png'), conBut)
## Transition
text_time(win, bufferText, 2)
# Trial loop
for triali, stim in enumerate(
    stimuList, start=len(dataDict['trial'])
    ):
    ## Add id, trial, task type, and correct response to data frame
    add_itt(dataDict, file_name, triali, 'main_film')
    ## Stimulus information
    stinfo = stim.split('_')
    for coli, infoi in zip(stimulus_information, stinfo):
        dataDict[coli].append(infoi.split('.')[0])

    ## Default values
    missed = False
    resp = None
    rt = np.nan
    
    ## Prepare stimulus
    stimname_full = TASK_DIR / stim
    stimulus.filename = stimname_full
    stimulus.loadMovie(stimname_full)

    ## Prepare data collection
    event.clearEvents(eventType='keyboard')
    my_clock.reset()
    # Play stimulus
    while not stimulus.isFinished:
        stimulus.draw()
        win.flip()
        ## Quit
        if event.getKeys('escape'):
            stimulus.stop()
            core.quit()
        ## Response time
        elif event.getKeys(YES_response):
            rt = my_clock.getTime()
            resp = YES_response
            
            stimulus.stop()
            fbText.text = ''
            feedback.lineColor = 'green'
    ## No response
    if resp is None:
        missed = True
        resp = np.nan
        
        stimulus.stop()
        fbText.text = 'U heeft niet snel genoeg gedrukt'
        feedback.lineColor = 'red'
    # Save trial information
    dataDict['rawRT'].append(rt)
    dataDict['actResp'].append(resp)
    dataDict['missed'].append(missed)

    # Show feedback
    feedback.draw()
    fbText.draw()
    win.flip()
    time.sleep(FB_DUR)

# Save data
ppdata = pd.DataFrame(dataDict, columns=column_list)
ppdata['completed'] = (len(ppdata) == len(pracList) + len(stimuList))
ppdata.to_csv(pp_file)

# End
onlyReal_missed = list(ppdata.iloc[len(pracList):]['missed'])
totacc = onlyReal_missed.count(False)
scoretext = f'U zag {totacc} van de {len(onlyReal_missed)} politiewagens!\n'
peracc = round(totacc / len(onlyReal_missed) * 100, 2)
percentext = f'Dat is {peracc} %!\n\nBedankt voor uw deelname!'

end.text = scoretext + percentext
text_keys(win, end, YES_response)

win.close()
core.quit()



# ------------------------------------------------------------------------- End
