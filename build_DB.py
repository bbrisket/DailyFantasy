import pandas as pd
import numpy as np
import sqlite3
import sqlalchemy as db
from bs4 import BeautifulSoup
import requests

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
    print(year, week_num, stat_type, sep=" - ", end="\n")
    return url

def stats_to_df(url):
    page = requests.get(url);
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')

    first_flag = True
    rows = table.findAll('tr')
    for row in rows:
        cols = row.findAll('td')

        if not cols:
            continue

        if first_flag:  #extract column names from the table's first row; PFF table headers are unhelpful
            colnames = [col['data-stat'] for col in cols]
            data = pd.DataFrame(columns = colnames)
            first_flag = False

        text = [col.get_text() for col in cols if col] #list of stats for each player
        data = data.append(pd.DataFrame([text], columns = colnames))

    data = data.dropna()
    return data

def clear_db_tables(con, table_names):
    for table in table_names:
        con.execute("DROP TABLE IF EXISTS {}".format(table))

def main():
    ### Set up database
    engine = db.create_engine('sqlite:///dfs.db')
    conn = engine.connect()
    clear_db_tables(conn, ["NFL_CONTESTS", "NFL_STATS_PASS", "NFL_STATS_RUSH",
                           "NFL_STATS_REC", "NFL_STATS_DEF"])

    ### Get contest info
    contest_df = pd.DataFrame()
    for i in range(1, 17):
        week = "Week " + str(i)
        temp_df = pd.read_excel("DK_NFL_contest_data_2018.xlsx", sheet_name=week)
        temp_df["Week"] = week
        contest_df = pd.concat([contest_df, temp_df])

    contest_df = contest_df.dropna() #get rid of contests with missing data
    contest_df.to_sql(name='NFL_CONTESTS', con=conn, if_exists='replace', index = False)

    ### Get player info
    for i in range(1, 17):
        pass_data = stats_to_df(get_stats_URL(week_num = i, stat_type = "pass_att"));
        pass_data.to_sql(name='NFL_STATS_PASS', con=conn,if_exists='append', index = False)

        rush_data = stats_to_df(get_stats_URL(week_num = i, stat_type = "rush_att"));
        rush_data.to_sql(name='NFL_STATS_RUSH', con=conn, if_exists='append', index = False)

        rec_data = stats_to_df(get_stats_URL(week_num = i, stat_type = "rec"));
        rec_data.to_sql(name='NFL_STATS_REC', con=conn, if_exists='append', index = False)

        def_data = stats_to_df(get_stats_URL(week_num = i, stat_type = "tackles_solo"));
        def_data.to_sql(name='NFL_STATS_DEF', con=conn, if_exists='append', index = False)

    ### Examine data
    playernames = conn.execute("SELECT player, team FROM NFL_STATS_DEF")
    print(playernames.fetchall()[0:100])


if __name__ == '__main__':
    main()
