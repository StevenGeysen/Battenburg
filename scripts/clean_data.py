#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""     Clean data -- Version 2
Last edit:  2023/03/16
Author(s):  Geysen, Steven (SG)
Notes:      - Clean the data from the online experiment
            - Release notes:
                * Fit to iVOX data
Comments:   SG: Only works with .csv files of json dumps, stored
                in `../data/raw`.
"""



#%% ~~ Imports and directories ~~ %%#


import json

import pandas as pd

from pathlib import Path


# Directories
SPINE = Path.cwd().parent
DAT_DIR = SPINE / 'data'
RAW_DIR = DAT_DIR / 'raw'
OUT_DIR = DAT_DIR / 'cleaned'
if not Path.exists(OUT_DIR):
    Path.mkdir(OUT_DIR)



#%% ~~ Variables ~~ %%#


dataList = [
    filei.name for filei in Path.iterdir(RAW_DIR)
    if filei.name.endswith('csv')
    ]

# Excessive columns
excess_cols = ['trial_type', 'internal_node_id']
# Stimulus columns
stim_cols = [
    'scenarioID', 'persepctief', 'kleur', 'kledij', 'retroreflectie',
    'zijde_zichtbaar', 'zwaailicht', 'omgeving', 'scenario', 'lichtconditie'
    ]



#%% ~~ Clean data ~~ %%#
########################


for datai in dataList:
    dataset = pd.read_csv((RAW_DIR / datai), sep=';')
    for _, subdata in dataset.iterrows():
        # Subject data in DataFrame
        # -------------------------
        sublist = []
        subid = subdata['ID']
        for indexi, triali in subdata.iteritems():
            if 'Q' in indexi:
                trialdata = json.loads(triali)
                if 'task' in trialdata.keys():
                    trialdf = pd.DataFrame(trialdata, index=[0])
                    sublist.append(trialdf)
        subdata_df = pd.concat(sublist).set_index('trial_index')

        # Clean data
        # ----------
        # Remove excessive columns
        subdata_df = subdata_df.drop(excess_cols, axis=1)
        # Stimulus information
        stimDict = {coli: [] for coli in stim_cols}
        for _, trial in subdata_df.iterrows():
            ## Remove photo location
            stimInfo = trial['stimulus'].split('/')[-1]
            stimInfo = stimInfo.split('_')
            for coli, infoi in zip(stimDict.keys(), stimInfo):
                stimDict[coli].append(infoi)
        stimData = pd.DataFrame.from_dict(stimDict)

        # Save data
        # ---------
        ## Correct indexes
        subdata_df.reset_index(drop=True, inplace=True)
        stimData.reset_index(drop=True, inplace=True)
        subdata_df = pd.concat([subdata_df, stimData], axis=1)
        
        subdata_df.to_csv((OUT_DIR / f'cleaned_{subid}.csv'))



# ------------------------------------------------------------------------- End
