#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 01:20:54 2019

@author: swapnil
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from WS_functions import *
from unidecode import unidecode

#-------generate_player_database()-------
#creates a csv file of 500 top valued players
#----------------------------------------
#generate_players_database()

player_name=input('Enter Player Name :')
res_returned = search_player(player_name)
if type(res_returned)==type(pd.Series()):
    print(res_returned['Name'])
    name_tag = res_returned['Name_tag']
    ID = res_returned['ID']
    table_df = Get_Player_Club_Goal(name_tag,ID)
    all_season_matches=Get_Player_Club_Stats(name_tag,ID)
else:
    print('Run again!')       



#%%
