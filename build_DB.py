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
               "NFL_STATS_REC", "NFL_STATS_DEF"]

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

    salaries = pd.DataFrame(columns = salaries_clean[0].split(";"), )
    for row in salaries_clean[1:]:
        record = row.split(";")
        if record != [""]:
            salaries.loc[len(salaries)] = record

    salaries.to_sql(name = table_name, con = con, if_exists = 'append', index = False)
    return salaries

def main():
    ### Set up database
    engine = db.create_engine('sqlite:///data/dfs.db')
    conn = engine.connect()
    clear_db_tables(conn, table_names)

    ### Get contest info
    contest_df = pd.DataFrame()
    for week in range(1, 18):
        w = "Week " + str(week)
        temp_df = pd.read_excel("data/DK_NFL_contest_data_2018.xlsx", sheet_name=week)
        temp_df["Week"] = w
        contest_df = pd.concat([contest_df, temp_df])

    contest_df = contest_df.dropna() #get rid of contests with missing data
    contest_df.to_sql(name = 'NFL_CONTESTS', con = conn, if_exists = 'replace', index = False)

    ### Get player info
    for week in range(1, 18):
        for team in team_names:
            add_NFL_stats(conn, "NFL_STATS_PASS", team, week, "pass_att")
            add_NFL_stats(conn, "NFL_STATS_RUSH", team, week, "rush_att")
            add_NFL_stats(conn, "NFL_STATS_REC", team, week, "rec")
            add_NFL_stats(conn, "NFL_STATS_DEF", team, week, "tackles_solo")

    ### Get salary info
    for week in range(1, 18):
            add_salaries(conn, "NFL_SALARIES", year = 2018, week_num = week)

    conn.close()


if __name__ == '__main__':
    main()
