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
                
                self.page_results_list.append((team_one.text, team_two.text))
                
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
        
    def clean_page_results_dataframe(self):

        visitor_df = self.result.iloc[:,0]
        home_df = self.result.iloc[:,1]
        
        visitor_df = visitor_df.apply(lambda x: self.split_n_instance(x))
        home_df = home_df.apply(lambda x: self.split_n_instance(x))
        
        visitor_df = pd.DataFrame(visitor_df.tolist(), index=visitor_df.index)
        home_df = pd.DataFrame(home_df.tolist(), index=home_df.index)
        
        visitor_df.rename(columns={0:'Visitor Name', 1:'Visitor Score'}, inplace=True)
        home_df.rename(columns={0:'Home Name', 1:'Home Score'},inplace=True)
        
        visitor_df['Visitor Name'] = visitor_df['Visitor Name'].apply(lambda x: self.strip_numbers(x))
        home_df['Home Name'] = home_df['Home Name'].apply(lambda x: self.strip_numbers(x))         
        full_df = visitor_df.join(home_df) 
        
                
        #pickle.dump(visitor_df, open("visitor.p", "wb"))
        #pickle.dump(home_df, open("home.p", "wb"))
        
        # self.cleaned_df = non_empty_df
        #pickle.dump(self.cleaned_df, open("save.p", "wb"))

    def page_scrape(self):
        self.get_score_set()
        self.return_score_set()
        self.return_page_results_dataframe()
        self.clean_page_results_dataframe()
    


