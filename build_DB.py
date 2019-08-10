import pandas as pd
import numpy as np
import sqlite3
import sqlalchemy as db
from bs4 import BeautifulSoup
import requests

team_names = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
         'DAL', 'DEN', 'DET', 'GNB', 'HOU', 'IND', 'JAX', 'KAN',
         'LAC', 'LAR', 'MIA', 'MIN', 'NOR', 'NWE', 'NGY', 'NYJ',
         'OAK', 'PHI', 'PIT', 'SEA', 'SFO', 'TAM', 'TEN', 'WAS']

table_names = ["NFL_CONTESTS", "NFL_STATS_PASS", "NFL_STATS_RUSH",
               "NFL_STATS_REC", "NFL_STATS_DEF", "NFL_SALARIES"]

def get_stats_URL(
    year = 2018, team_id = "", opp_id = "", week_num = 1,
    game_location = "", stat_type = "pass_att"
):
    '''
    Note: URL retrieves stats for only a single week at a time to account for PFR's
        limit of 100 results per page.
    '''
    if stat_type not in ["pass_att", "rush_att", "rec", "tackles_solo"]:
        print("stat_type must be in [\"pass_att\", \"rush_att\", \"rec\", \"tackles_solo\"]")

    url = ("https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&" +
            "year_min={}&" +
            "year_max={}&" +
            "season_start=1&" +
            "season_end=-1&" +
            "age_min=0&" +
            "age_max=99&" +
            "game_type=A&" +
            "league_id=&" +
            "team_id={}&" +
            "opp_id={}&" +
            "game_num_min=0&" +
            "game_num_max=99&" +
            "week_num_min={}&" +
            "week_num_max={}&" +
            "game_day_of_week=&" +
            "game_location={}&" +
            "game_result=&" +
            "handedness=&" +
            "is_active=&" +
            "is_hof=&" +
            "c1stat={}&" +
            "c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&" +
            "order_by=player&" +
            "from_link=1").format(year, year, team_id, opp_id, week_num, week_num,
                                  game_location, stat_type)
    print(year, week_num, team_id, stat_type, sep=" - ", end="\n")
    return url

def stats_to_df(url):
    page = requests.get(url);
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')

    if table is None:
        return None

    first_flag = True
    rows = table.findAll('tr')
    data = None
    for row in rows:
        cols = row.findAll('td')

        if not cols:
            continue

        if first_flag:  #extract column names from the table's first row; PFF table headers are unhelpful
            colnames = [col['data-stat'] for col in cols]
            data = pd.DataFrame(columns = colnames)
            first_flag = False

        text = [col.get_text() for col in cols if col] #list of stats for each player
        df = pd.DataFrame([text], columns = colnames)

        if data is None:
            data = df
        else:
            data = data.append(df)

    return data

def clear_db_tables(con, table_names):
    for table in table_names:
        con.execute("DROP TABLE IF EXISTS {}".format(table))

def add_NFL_stats(con, table_name, team_id, week_num, stat_type):
    data = stats_to_df(get_stats_URL(team_id = team_id, week_num = week_num, stat_type = stat_type))
    if data is not None:
        data.to_sql(name = table_name, con = con, if_exists = 'append', index = False)

def add_salaries(con, table_name, year = 2018, week_num = 1):
    page = requests.get("http://rotoguru1.com/cgi-bin/fyday.pl?week={}&year={}&game=dk&scsv=1".format(week_num, year))
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')

    salaries_raw = table.find('pre').string
    salaries_clean = salaries_raw.split("\n")

    salary_columns = ['player', 'pos', 'team', 'week_num', 'year', 'score', 'salary']
    salaries = pd.DataFrame(columns = salary_columns)
    for row in salaries_clean[1:]:
        record = row.split(";")
        if len(record) == 10: # Check that each row is properly formatted
            new_record = []
            fullname = record[3]
            if "," in fullname: # Swap naming format to `firstname lastname`
                name = fullname.split(", ")
                fullname = (name[1] + " " + name[0]).replace("'", "\\'")

            position = record[4]
            if position == 'Def':
                position = 'DEF'
                fullname = record[5].upper()
                if fullname == 'JAC':
                    fullname = 'JAX'

            team = record[5].upper()
            if team == 'JAC':
                team = 'JAX'

            new_record.append(fullname)  # Player name
            new_record.append(position) # Position
            new_record.append(team) # Team
            new_record.append(record[0]) # Week number
            new_record.append(record[1]) # Year
            new_record.append(record[8]) # Fantasy score
            new_record.append(record[9]) # DraftKings salary

            salaries.loc[len(salaries)] = new_record
            print(new_record)

    salaries.to_sql(name = table_name, con = con, if_exists = 'append', index = False)
    return salaries

def main():
    ### Set up database
    engine = db.create_engine('sqlite:///data/dfs.db')
    con = engine.connect()
    clear_db_tables(con, table_names)

    ### Get contest info
    contest_df = pd.DataFrame()
    for week in range(1, 18):
        w = "Week " + str(week)
        temp_df = pd.read_excel("data/DK_NFL_contest_data_2018.xlsx", sheet_name=w)
        temp_df["Week"] = week
        contest_df = pd.concat([contest_df, temp_df])

    contest_df = contest_df.dropna() #get rid of contests with missing data
    contest_df.to_sql(name = 'NFL_CONTESTS', con = con, if_exists = 'replace', index = False)

    ### Get salary info
    for week in range(1, 18):
            add_salaries(con, "NFL_SALARIES", year = 2018, week_num = week)

    ### Get player info
    for week in range(1, 18):
        for team in team_names:
            add_NFL_stats(con, "NFL_STATS_PASS", team, week, "pass_att")
            add_NFL_stats(con, "NFL_STATS_RUSH", team, week, "rush_att")
            add_NFL_stats(con, "NFL_STATS_REC", team, week, "rec")
            add_NFL_stats(con, "NFL_STATS_DEF", team, week, "tackles_solo")

    con.close()


if __name__ == '__main__':
    main()
