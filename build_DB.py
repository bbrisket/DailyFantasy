import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import requests

#    c.execute('''CREATE TABLE CONTESTS
#            ([Name] text, [Link] text, [Prize Pool] float, [Buy In] float,
#                [Top Prize] integer, [Max Entries] integer, [Entries] integer,
#                [Cash Line] float, [Winner] text, [Winning Score] float,
#                [Week] text)''')

def fetch_NFL_stats():
    return 0


def main():
    ### Get contest info

    conn = sqlite3.connect("dfs.db")
    c = conn.cursor()

    contest_df = pd.DataFrame()

    for i in range(1, 18):
        week = "Week " + str(i)
        temp_df = pd.read_excel("DK_NFL_contest_data_2018.xlsx", sheet_name=week)
        temp_df["Week"] = week
        contest_df = pd.concat([contest_df, temp_df])

    contest_df = contest_df.dropna() #get rid of contests with missing data
    contest_df.to_sql(name='CONTESTS', con=conn, if_exists='replace', index = False)

    contest_names = c.execute("SELECT Name, [Winning Score] FROM CONTESTS WHERE Name LIKE '%Double%'")
    print(contest_names.fetchall())

    ### Get player info

    url = "https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2018&year_max=2018&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min=1&week_num_max=1&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_rating&from_link=1"
    page = requests.get(url);
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')

    rows = table.findAll('tr')
    first_flag = True

    for row in rows:
        cols = row.findAll('td')

        if not cols:
            continue

        if first_flag:
            colnames = [col['data-stat'] for col in cols]
            data = pd.DataFrame(columns = colnames)
            first_flag = False

        text = [col.get_text() for col in cols if col] #list of stats for each player
        data = data.append(pd.DataFrame([text], columns = colnames))

    print(data)

if __name__ == '__main__':
    main()
