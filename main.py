from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from draftclass import ParseScoreSet
import pickle
import logging
#environment is bs_sel
#https://www.youtube.com/channel/UC8tgRQ7DOzAbn9L7zDL8mLg

def main():
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=Service('./chromedriver'))
    driver.get("https://d1baseball.com/scores/?date=20210527&c=all")

    html_doc = driver.page_source

    soup = BeautifulSoup(html_doc, "html.parser")

    pss = ParseScoreSet(soup)
    # pss.get_score_set()
    # pss.return_score_set()
    # pss.return_page_results_dataframe()
    # pss.clean_page_results_dataframe()
    pss.page_scrape()

if __name__ == '__main__': 
    main()