import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def getPlayerStatsURL(playerName):
    return "https://lol.gamepedia.com/Special:RunQuery/TournamentStatistics?TS%5Bpreload%5D=PlayerByChampion&TS%5Btournament%5D=LCS%202019%20Summer&TS%5Blink%5D=" + playerName + "&pfRunQueryFormName=TournamentStatistics"

def main():
    doubleliftURL = getPlayerStatsURL("doublelift")
    #table = pd.read_html(doubleliftURL)

    playerPage = requests.get(doubleliftURL)
    playerSoup = BeautifulSoup(playerPage.content)
    playerStats = playerSoup.find()

    print(soup)

if __name__ == '__main__':
    main()
