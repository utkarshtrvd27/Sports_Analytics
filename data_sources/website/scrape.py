from operator import le
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def league_table():
    # Defining Data source URL
    url = 'https://www.bbc.com/sport/football/premier-league/table'

    # Extracting HTML content from the webpage
    page = requests.get(url) # makes a request to the webpage and returns the html content
    soup = BeautifulSoup(page.text, "html.parser")

    # Extracting the table headers and data from the HTML content
    headers = []
    table = soup.find("table", {"data-testid": "football-table"}) # find the <table> element with the specified data-testid attribute
    for th in table.find_all('th'): #finds all the html tags th which holds the header details
        title = th.text # Header content
        headers.append(title)

    league_table = pd.DataFrame(columns = headers) #creates a dataframe with the headers
        
    for tr in table.find_all('tr')[1:]:
        row_data = tr.find_all('td')
        row = [i.text for i in row_data]
        
        curr_idx = len(league_table)
        # print("league_table length=", curr_idx, "row=",row)
        league_table.loc[curr_idx] = row
        
    league_table.drop(["Form, Last 6 games, Oldest first"], axis=1, inplace=True)
    
    # Remove position numbers from team names (e.g., "1Arsenal" -> "Arsenal")
    league_table['Team'] = league_table['Team'].str.replace(r'^\d+', '', regex=True)
    
    return league_table


def top_scorers():
    url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", {"data-testid": "sport-table"})

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)

    top_scorers = pd.DataFrame(columns = headers)

    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(top_scorers)
        top_scorers.loc[length] = row

    top_scorers.Name = top_scorers.Name.replace(r'([A-Z])', r' \1', regex=True).str.split()
    top_scorers.Name = top_scorers.Name.apply(lambda x: ' '.join(dict.fromkeys(x).keys()))

    top_scorers['Club'] = top_scorers.Name.str.split().str[2:].str.join(' ')
    top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(' ')
    col = top_scorers.pop("Club")
    top_scorers.insert(2, 'Club', col)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Manchester City' if 'Manchester City' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Manchester United' if 'Manchester United' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Brighton & Hove Albion' if 'Brighton & Hove Albion' in x else x)

    #Removing unnecessary columns
    top_scorers.drop(["GoalsGL", "AssistsA", "PlayedP", "Minutes per GoalMins per Goal"], axis=1, inplace=True)

    # Rename column
    top_scorers.rename(columns={"Goals per 90 minutesGoals per 90": "Goals per 90 minutes", "Minutes per GoalMPG": "Minutes per Goal"}, inplace=True)
    return top_scorers


# def detail_top_scorers():
#     url = 'https://www.worldfootball.net/competition/co91/england-premier-league/se94757/2025-2026/statistics-goals/'
#     headers = []
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text,  "html.parser")
#     table= soup.find("table", class_="module-statistics statistics")

#     for i in table.find_all('th'):
#         title = i.text
#         headers.append(title)
#     detail_top_scorer = pd.DataFrame(columns = headers)
#     for j in table.find_all('tr')[1:]:
#         row_data = j.find_all('td')
#         row = [i.text for i in row_data]
#         length = len(detail_top_scorer)
#         detail_top_scorer.loc[length] = row

#     detail_top_scorer = detail_top_scorer.drop([''],axis=1)
#     detail_top_scorer.Team = detail_top_scorer.Team.str.replace('\n\n','')
#     detail_top_scorer['Penalty'] = detail_top_scorer['Goals (Penalty)'].str.split().str[-1:].str.join(' ')
#     detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace('(','')
#     detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace(')','')
#     detail_top_scorer['Goals (Penalty)'] = detail_top_scorer['Goals (Penalty)'].str.split().str[0].str.join('')
#     detail_top_scorer.rename(columns = {'Goals (Penalty)':'Goals'}, inplace = True)
#     detail_top_scorer = detail_top_scorer.drop(['#'], axis = 1)
#     return detail_top_scorer


# def all_time_winner_club():
#     url = 'https://www.worldfootball.net/winner/eng-premier-league/'
#     headers = []
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text,  "html.parser")
#     table= soup.find("table", class_="standard_tabelle")

#     for i in table.find_all('th'):
#         title = i.text
#         headers.append(title)
#     winners = pd.DataFrame(columns = headers)
#     for j in table.find_all('tr')[1:]:
#         row_data = j.find_all('td')
#         row = [i.text for i in row_data]
#         length = len(winners)
#         winners.loc[length] = row

#     winners = winners.drop([''], axis=1)
#     winners['Year'] = winners['Year'].str.replace('\n', '')
#     return winners


