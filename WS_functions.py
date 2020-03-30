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
from unidecode import unidecode
import os

root_dir = '/home/swapnil/Study/Football/TM_Web_Scraping_Project/'

def generate_players_database():   
    all_player_base_url='https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/0/galerie/0?ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&land_id=0&kontinent_id=0&yt0=Show'
    response2 = requests.get(all_player_base_url, headers={'User-Agent': 'Custom5'})
    soup_obj2 = BeautifulSoup(response2.text,'html5lib')
#    keys = soup_obj2.find('ul',attrs = {'id':'yw2'}).find_all('li')[-1].find('a')['href'].replace('/spieler-statistik/wertvollstespieler/marktwertetop?page=','')    
    all_players_details = list()
    for i in range(int(20)):
        response2 = requests.get(all_player_base_url+'&page='+str(i+1), headers={'User-Agent': 'Custom5'})
        soup_obj2 = BeautifulSoup(response2.text,'html5lib')
        table = soup_obj2.find('div',attrs = {'id':'yw1'}).find('tbody').find_all('table')
        for each_row in table:
            each_player = each_row.find('tbody').find_all('tr')[0].find_all('a')[1]
            each_player_name = each_player.text
            each_player_id = each_player['id']
            each_player_pos = each_row.find('tbody').find_all('tr')[1].find('td').text
            each_player_tag = each_player['href'].split('/')[1]
            all_players_details.append([each_player_name,each_player_tag,each_player_id,each_player_pos])
    all_players_df = pd.DataFrame(all_players_details,columns=['Name','Name_tag','ID','Position'])
    all_players_df.to_csv(root_dir+'Data/Databases/all_players_db.csv')

def search_player(player_name):
    player_name = player_name.lower().replace(' ','-').replace("'","")
    all_player_df = pd.read_csv(root_dir+'Data/Database/all_players_db.csv')
    curr_player_search = all_player_df[all_player_df['Name_tag'].str.contains(player_name)]
    if len(curr_player_search)>0:
        print(curr_player_search)
        player_index = input("INPUT PLAYER INDEX : ")
        if len(curr_player_search.ix[int(player_index)])>0:
            return(curr_player_search.ix[int(player_index)])
        else:
            print('Enter Vaild Index')
            return False
    else:
        print('No match found! Try Again!')
        return False
    
    
def Get_Player_Club_Goal(name_tag,ID):
    
    url = "https://www.transfermarkt.com/"+str(name_tag)+"/alletore/spieler/"+str(ID)+"/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/minute/0/torart/0/plus/1"
    response = requests.get(url, headers={'User-Agent': 'Custom5'})
    soup_obj = BeautifulSoup(response.text,'html5lib')
    table = soup_obj.find('div',attrs = {'class':'responsive-table'})

    for each in table.find_all('tbody'):
        i=1
        table_list = list()
        for each_tr in each.find_all('tr'):
            if len(each_tr.find_all('td'))>1:
                if len(each_tr.find_all('td'))==15:
                    c_g_league=each_tr.find_all('td')[1].find('a')['href'].split('/')[1]
                    c_g_date=datetime.strptime(each_tr.find_all('td')[3].text,'%m/%d/%y').date()
                    c_g_venue=each_tr.find_all('td')[4].text
                    c_g_for=each_tr.find_all('td')[5].find('img')['alt']
                    c_g_against=each_tr.find_all('td')[7].find('img')['alt']
                    c_g_mat_res=each_tr.find_all('td')[9].find('span').text
                    c_g_mat_pos=each_tr.find_all('td')[10].find('a')['title']
                    c_g_min=each_tr.find_all('td')[11].text
                    c_g_score=each_tr.find_all('td')[12].text
                    c_g_type=each_tr.find_all('td')[13].text
                    c_g_assist=each_tr.find_all('td')[14].text
                    
                elif len(each_tr.find_all('td'))==14:
                    c_g_league=each_tr.find_all('td')[1].find('a')['href'].split('/')[1]
                    c_g_date=datetime.strptime(each_tr.find_all('td')[3].text,'%m/%d/%y').date()
                    c_g_venue=each_tr.find_all('td')[4].text
                    c_g_for=each_tr.find_all('td')[5].find('img')['alt']
                    c_g_against=each_tr.find_all('td')[6].find('img')['alt']
                    c_g_mat_res=each_tr.find_all('td')[8].find('span').text
                    c_g_mat_pos=each_tr.find_all('td')[9].find('a')['title']
                    c_g_min=each_tr.find_all('td')[10].text
                    c_g_score=each_tr.find_all('td')[11].text
                    c_g_type=each_tr.find_all('td')[12].text
                    c_g_assist=each_tr.find_all('td')[13].text
                        
                elif len(each_tr.find_all('td'))==5:
                    c_g_min=each_tr.find_all('td')[1].text
                    c_g_score=each_tr.find_all('td')[2].text
                    c_g_type=each_tr.find_all('td')[3].text
                    c_g_assist=each_tr.find_all('td')[4].text
                
                table_list.append([i,c_g_date,c_g_league,c_g_for,c_g_against,c_g_venue,c_g_mat_res,c_g_mat_pos,c_g_min,c_g_score,c_g_type,c_g_assist])
                i=i+1
    
    table_df = pd.DataFrame(table_list,columns=['Goal_No','Date','Competition','For','Against','Home_Away','Match_Result','Position','Time','Score_After_Goal','Goal_Type','Assist_Provider'])
    if os.path.isdir(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/')==False:
        os.mkdir(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/')
    table_df.to_csv(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/'+str(name_tag)+'-'+str(ID)+'_club_goals.csv')
    return table_df
    

def Get_Player_Club_Stats(name_tag,ID):
    season = 2019
    url = "https://www.transfermarkt.co.in/"+str(name_tag)+"/leistungsdatendetails/spieler/"+str(ID)+"/plus/1?saison="+str(season)+"&verein=&liga=&wettbewerb=&pos=&trainer_id="
    response = requests.get(url, headers={'User-Agent': 'Custom5'})
    soup_obj = BeautifulSoup(response.text,'html5lib')
    
    all_years = [each['value'] for each in soup_obj.find_all('table',attrs={'class':'auflistung'})[0].find_all('tr')[0].find_all('option')[1:]]
    all_season_matches = list()   
    for each_year in all_years:
        print(each_year)
        url = "https://www.transfermarkt.co.in/"+str(name_tag)+"/leistungsdatendetails/spieler/"+str(ID)+"/plus/1?saison="+str(each_year)+"&verein=&liga=&wettbewerb=&pos=&trainer_id="
        response = requests.get(url, headers={'User-Agent': 'Custom5'})
        soup_obj = BeautifulSoup(response.text,'html5lib')
        all_tables = soup_obj.find_all('div',attrs={'class':'responsive-table'})
        for i in range(1,len(all_tables)):
            all_matches = all_tables[i].find('tbody').find_all('tr')
            for each_match in all_matches:
#                print(each_match.find_all('td')[0].find('a')['href'].split('/')[1])
#                print(len(each_match.find_all('td')))
                if len(each_match.find_all('td'))==17 or len(each_match.find_all('td'))==18:
                    competition = each_match.find_all('td')[0].find('a')['href'].split('/')[1]
                    date = datetime.strptime(each_match.find_all('td')[1].text,'%b %d, %Y').date()
                    home_team = each_match.find_all('td')[3].find('a').text
                    away_team = each_match.find_all('td')[5].find('a').text
                    match_score = each_match.find_all('td')[6].find('a').text
                    if len(each_match.find_all('td')[6].find('span')['class'])==0:
                        match_result = 'draw'
                    elif each_match.find_all('td')[6].find('span')['class'][0]=='greentext':
                        match_result = 'won'
                    elif each_match.find_all('td')[6].find('span')['class'][0]=='redtext':
                        match_result = 'lost'
                    match_position = each_match.find_all('td')[7].find('a')['title']
                    match_goals = 0 if each_match.find_all('td')[8].text=='' else each_match.find_all('td')[8].text
                    match_assists = 0 if each_match.find_all('td')[9].text=='' else each_match.find_all('td')[9].text
                    match_own_goals = 0 if each_match.find_all('td')[10].text=='' else each_match.find_all('td')[9].text
                    if len(each_match.find_all('td'))==17:
                        minutes_played = each_match.find_all('td')[16].text
                    elif len(each_match.find_all('td'))==18:
                        minutes_played = each_match.find_all('td')[17].text
                    all_season_matches.append([date,competition,each_year,home_team,away_team,match_score,match_result,match_position,match_goals,match_assists,match_own_goals,minutes_played])
    
    all_season_matches_df = pd.DataFrame(all_season_matches,columns=['Date','Competition','Season','Home_Team','Away_Team','Match_Score','Match_Result','Position','Goals','Assists','Own_Goals','Minutes_Played'])
    if os.path.isdir(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/')==False:
        os.mkdir(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/')
    all_season_matches_df.to_csv(root_dir+'Data/Player_Data/'+str(name_tag)+'-'+str(ID)+'/'+str(name_tag)+'-'+str(ID)+'_club_match_statistics.csv')
    



























