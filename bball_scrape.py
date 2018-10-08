import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import datetime
import multiprocessing as multi


def create_soup(url):
    '''
    turns a url into a beautifulsoup object
    :param url: webpage url as a string
    :return: beautifulsoup object
    '''
    response = requests.get(url)
    #print(response.status_code)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')
    return soup

def read_table(soup):
    '''
    turns a table from the site into a dictionary with players as keys and a list of statistics as values
    :param soup: beautifulsoup object created by create_soup function
    :return: dictionary of players with their statistics as values
    '''
    all_data = []
    remove_list = ['<tr><th class=','left ', ' csk=', ' data-append-csv=', ' data-stat=', 'player', ' scope=',
                    'row', '><a href=', 'right ', ' data-stat=', 'mp', ' scope=', '<tr data-row=', '><th class=']

    table_list = str(soup.find_all(class_='overthrow table_container'))
    #print(table_list)
    table = table_list.split('\n')
    #print('check0')
    #print(table)
    for item in table:
        if '<th class="left "' in item:
            #print('check1')
            data = []
            fragments = re.split('csk"|"|', item)
            for chunk in fragments:
                if chunk not in remove_list:
                    data.append(chunk)
            all_data.append(data[1:])

    # for stat_list in all_data:
    #     print(stat_list)

    player_dict = {}

    all_data.pop(len(all_data)-1)

    for stat_list in all_data:
        if len(stat_list) >= 42:
            player_dict[stat_list[0]] = [pt_clean(stat_list[4])/60, #minutes played
                                         int_clean(stat_list[7]),   #field goals hit
                                         int_clean(stat_list[9]),   #field goals attempted
                                         pct_clean(stat_list[11]),  #fg percentage
                                         int_clean(stat_list[13]),  #3's hit
                                         int_clean(stat_list[15]),  #3's attempted
                                         pct_clean(stat_list[17]),  #3's pct
                                         int_clean(stat_list[19]),  #free throws hit
                                         int_clean(stat_list[21]),  #free throws attempted
                                         pct_clean(stat_list[23]),  #free throw pct
                                         int_clean(stat_list[25]),  #offensive rebounds
                                         int_clean(stat_list[27]),  #defensive rebounds
                                         int_clean(stat_list[29]),  #total rebounds
                                         int_clean(stat_list[31]),  #assists
                                         int_clean(stat_list[33]),  #steals
                                         int_clean(stat_list[35]),  #blocks
                                         int_clean(stat_list[37]),  #turnovers
                                         int_clean(stat_list[39]),  #fouls
                                         int_clean(stat_list[41])]  #points

    return player_dict
    ###Ultimately will return a dictionary of player names with statistics

def pt_clean(string):
    '''
    turns a string that is an integer into its integer
    :param string: string with an integer value
    :return: int object or -1 if error is triggered
    '''
    try:
        return int(string)
    except:
        return -1

def int_clean(string):
    '''
    cleans a integer from html artifacts
    :param string: string in <##>.... format
    :return: integer object where ## was represented or -1 if formatting is incorrect
    '''
    ws = string[1:]
    try:
        if ws[0] == 'g' or len(ws) < 4:
            return -1
        elif ws[1] == '<':
            return int(ws[0])
        elif ws[2] == '<':
            return int(ws[0:2])
        else:
            return -1
    except:
        print(ws)
        return -1

def pct_clean(string):
    '''
    cleans a 3 digit percentage number from a string
    :param string: '<.###>....'
    :return: 0.### as a float object or 0 if formatting is incorrect
    '''
    ws = '0' + string[1:5]
    if ws[1] == '.':
        return float(ws)
    else:
        return 0

    ## building a crawler to take a years worth of data
    ## this cell sets up the spider


def scrape(year_list):
    #Initializes a dataframe
    url = 'https://www.basketball-reference.com/boxscores/200905240ORL.html'
    page = create_soup(url)
    # class with table is called overthrow table_container
    df = pd.DataFrame.from_dict(read_table(page), orient='index')

    df.columns = ['minutes_played', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', '3_pct',
                  'ft', 'fta', 'ft_pct', 'or', 'dr', 'tot_r', 'asst', 'steals',
                  'blocks', 'turnovers', 'fouls', 'points']

    #this block loops over day/month/year to append new box scores to my initial df
    chromedriver = '/Users/aaronfrederick/Downloads/chromedriver'
    os.environ['webdriver.chrome.driver'] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    for year in year_list:
        for a in range(5, 7):
            for b in range(1, 29):
                url = 'https://www.basketball-reference.com/boxscores/?month=%d&day=%d&year=%d' % (a, b, year)
                driver.get(url)
                try:
                    link = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/p/a[1]')
                    time.sleep(0.8)
                    link.click()
                except:
                    continue
                time.sleep(0.8)
                try:
                    soup = BeautifulSoup(driver.page_source,'lxml')
                except:
                    continue
                # class with table is called overthrow table_container
                time.sleep(0.8)
                add_df = pd.DataFrame.from_dict(read_table(soup), orient='index')
                if not add_df.empty:
                    add_df.columns = ['minutes_played', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', '3_pct',
                                      'ft', 'fta', 'ft_pct', 'or', 'dr', 'tot_r', 'asst', 'steals',
                                      'blocks', 'turnovers', 'fouls', 'points']
                df = df.append(add_df)
            # at the very end, we go back
                df.to_pickle(f'{a}-{year}df.pkl')

def workload(n,year_list):
    return np.array_split(year_list,n)

def main():
    start = time.time()
    cpus = multi.cpu_count()
    year_list = list(range(2000,2018,1))
    chunks = workload(cpus,year_list)
    workers = []
    for cpu in range(cpus):
        worker = multi.Process(name=str(cpu),
                               target=scrape, #Scrape function
                               args=(chunks[cpu],)) #Workload per processer
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()


    end = time.time()
    print(end - start, end='')
    print(' seconds taken to run')


main()
