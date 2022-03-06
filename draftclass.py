from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import logging
import time

class ParseScoreSet:
    def __init__(self, soup):
        self.soup = soup
        self.page_results_list = []
        self.result = None
        self.cleaned_df = None
        
    @staticmethod            
    def strip_numbers(team_input):
        "removes ranking number from team name" 
        unclean_team = re.sub(r'\d+', '', team_input)
        clean_team = unclean_team.strip()
        return clean_team

    def get_score_set(self):
        self.score_set_list = [tag for tag in self.soup.find_all(class_="score-set")]
        
    def return_score_set(self):
        "Returns team "
        for i in self.score_set_list: 
            box_score_by_division = i.find_all(class_='box-score scoresclear')
            
            for j in box_score_by_division:
                team_one = j.find(class_="team-1")
                team_two = j.find(class_="team-2")
                #away_team = self.strip_numbers(team_one.find(class_="team-title").text)
                #home_team = self.strip_numbers(team_two.find(class_="team-title").text)
                #print(team_one.text, team_two.text)
                
                self.page_results_list.append((team_one.text, team_two.text))
                # try: 
                #     away_team_winner = team_one.find(class_="team-score winner").text
                #     home_team_loser = team_two.find(class_="team-score defeated").text
                # except AttributeError: 
                #     pass
                # try: 
                #     home_team_winner = team_two.find(class_="team-score winner").text
                #     away_team_loser = team_one.find(class_="team-score defeated").text
                # except AttributeError: 
                #     pass
                # if away_team_winner and home_team_loser:
                #     self.page_results_list.append((away_team, away_team_winner, home_team, home_team_loser))
                # elif home_team_winner and away_team_loser:   
                #     self.page_results_list.append((away_team, away_team_loser, home_team, home_team_winner)) 
                # else: 
                #     logging.error(f'something wrong with {away_team} and {home_team}')  
    @staticmethod                
    def split_n_instance(text):
        """splits dataframe on third instance of \n"""
        n = 3
        groups = text.split('\n')
        a, b = ''.join(groups[:n]), ''.join(groups[n:])
        return a.strip(), b
                            
    def return_page_results_dataframe(self):
        """Turn page results into dataframe"""
        self.result = pd.DataFrame(self.page_results_list)
        pickle.dump(self.result, open("save.p", "wb"))
        
    def clean_page_results_dataframe(self):
        #This is where the issue is, using the split_n_instance does not work 
        #visitor_df = self.result.iloc[:,0].apply(self.split_n_instance())
        #home_df = self.result.iloc[:,1].apply(self.split_n_instance())
        visitor_df = self.result.iloc[:,0]
        home_df = self.result.iloc[:,1]
        
        visitor_df = visitor_df.apply(lambda x: self.split_n_instance(x))
        home_df = home_df.apply(lambda x: self.split_n_instance(x))
        
        
        
        visitor_df = pd.DataFrame(visitor_df.tolist(), index=visitor_df.index)
        home_df = pd.DataFrame(home_df.tolist(), index=home_df.index)
        
        # full_df = visitor_df.join(home_df) 
        pickle.dump(visitor_df, open("save.p", "wb"))
        # non_empty_df = full_df[full_df['Visitor Score'] != '']
        
        # non_empty_df['Visitor Name'] = non_empty_df['Visitor Name'].apply(strip_numbers)
        # non_empty_df['Home Name'] = non_empty_df['Visitor Name'].apply(strip_numbers)
        
        # self.cleaned_df = non_empty_df
        #pickle.dump(self.cleaned_df, open("save.p", "wb"))

    


