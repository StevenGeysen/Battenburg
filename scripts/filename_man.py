#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""     File name manipulation -- Version 2.1
Last edit:  2022/12/30
Author(s):  Geysen, Steven (SG)
Notes:      - Change file names to preferred format
            - Release notes:
                * Removed dead code
Comments:   SG: Removes ' ' from stimuli name, and adds uniform
                extention (.jpg)
            
Sources:    https://stackoverflow.com/a/45353565
            https://stackoverflow.com/a/952952
"""



#%% ~~ Imports and directories ~~ %%#


import pandas as pd

from pathlib import Path


# Directories
SPINE = Path.cwd().parent
STIM_DIR = SPINE / 'stimuli'
CAR_DIR = STIM_DIR / 'car_task'
PRAC_DIR = STIM_DIR / 'clothes_prac'
CLO_DIR = STIM_DIR / 'clothes_task'



#%% ~~ Format file names ~~ %%#
###############################


stimuList= [stimi.name for stimi in Path.iterdir(CAR_DIR)]

for stimi in stimuList:
    if ' ' in stimi:
        spacegone = stimi.split(' ')[0]
        splitname = spacegone.split('_')
        newname = '_'.join(splitname) + '.jpg'
        fullname = Path(CAR_DIR / stimi)
        fullname.rename(Path(CAR_DIR / newname))



#%% ~~ Prepare clothes stimuli ~~ %%#
#####################################


pracList = [
    f'PRAC_DIR + \'{stimi.name}\',\n' for stimi in Path.iterdir(PRAC_DIR)
    ]
with open('pracList.txt', 'w') as jsPrac:
    for stimi in pracList:
        jsPrac.write(stimi)

taskList = [
    f'STIM_DIR + \'{stimi.name}\',\n' for stimi in Path.iterdir(CLO_DIR)
    ]
with open('taskList.txt', 'w') as jsTask:
    for stimi in taskList:
        jsTask.write(stimi)



# ------------------------------------------------------------------------ End
