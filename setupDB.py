import pandas as pd
import sqlite3

def main():
    #engine = create_engine("sqlite:///dfs.db")
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

#    c.execute('''CREATE TABLE CONTESTS
#            ([Name] text, [Link] text, [Prize Pool] float, [Buy In] float,
#                [Top Prize] integer, [Max Entries] integer, [Entries] integer,
#                [Cash Line] float, [Winner] text, [Winning Score] float,
#                [Week] text)''')

    contest_names = c.execute("SELECT Name FROM CONTESTS WHERE Name LIKE '%Double%'")
    print(contest_names.fetchall())

    return 0

if __name__ == '__main__':
    main()
