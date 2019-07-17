import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def getPlayerStatsURL(player_name):
    return "https://lol.gamepedia.com/Special:RunQuery/TournamentStatistics?TS%5Bpreload%5D=PlayerByChampion&TS%5Btournament%5D=LCS%202019%20Summer&TS%5Blink%5D=" + player_name + "&pfRunQueryFormName=TournamentStatistics"

def analyze_player(player_stats, recency_bias):
```
player_stats (df): contains fantasy points per week
recency_bias (double): value describing the weight to assign to more recent performances,
    between 0 (least) to 1 (most) 

```
    numWeeks = 1
    points = [player_stats.iloc(i)[pts] for i in range(numWeeks)]

    avg = sum(points)/len(points)

    skewed_avg = 0 #bias toward more recent performances
    for i in range(numWeeks):
        skewed_avg += points[i]/(i+1)

    std = np.std(points)

    return avg, skewed_avg, std

def main():
    doublelift_URL = getPlayerStatsURL("doublelift")
    #table = pd.read_html(doublelift_URL)

    player_page = requests.get(doublelift_URL)
    player_soup = BeautifulSoup(player_page.content)
    player_stats = playerSoup.find()

    print(soup)

if __name__ == '__main__':
    main()