import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def getPlayerStatsURL(player_name):
    return "https://lol.gamepedia.com/Special:RunQuery/TournamentStatistics?TS%5Bpreload%5D=PlayerByChampion&TS%5Btournament%5D=LCS%202019%20Summer&TS%5Blink%5D=" + player_name + "&pfRunQueryFormName=TournamentStatistics"

def describePlayer(player_stats):
```
playerStats (df): contains fantasy points per week

```
    return

def main():
    doublelift_URL = getPlayerStatsURL("doublelift")
    #table = pd.read_html(doublelift_URL)

    player_page = requests.get(doublelift_URL)
    player_soup = BeautifulSoup(player_page.content)
    player_stats = playerSoup.find()

    print(soup)

if __name__ == '__main__':
    main()
