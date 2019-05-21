import numpy as np
import pandas as pd

def main():
    df = pd.DataFrame()

    for i in range(1, 18):
        week = "Week " + str(i)
        temp_df = pd.read_excel("DK_NFL_contest_data_2018.xlsx", sheet_name=week)
        temp_df["Week"] = week

        df = pd.concat([df, temp_df])

    df = df.dropna() #get rid of contests with missing data
    df.to_csv("DK_NFL_contest_data_2018_clean.csv", index=False)

if __name__ == '__main__':
    main()
