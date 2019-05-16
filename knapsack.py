import pandas as pd

def buildLineup(playerInfo, positionDict, cap):
    '''
    playerInfo: Pandas DataFrame containing player name, position, value, Salary
    positionDict: Dictionary with keys representing each position needed and
        values representing the number of players from those positions required
    cap: Integer representing salary cap

    buildLineup() returns a list of player names, representing the lineup of
    maximum value that fulfills the position requirement and stays below the
    salary cap.

    Current algorithm: Create basic roster consisting of players requiring
    minimum salary. Then gradually replace least efficient player within the
    lineup with the most efficient available player within the same position.
    '''
    lineup = []
    cost = 0

    foundPositionDict = {}
    cheapPlayerInfo = playerInfo.sort_values("Salary") #sort by cheapest player

    for row in range(len(cheapPlayerInfo)): #build basic lineup
        pos = cheapPlayerInfo.iloc[row]["Position"]
        salary = cheapPlayerInfo.iloc[row]["Salary"]
        name = cheapPlayerInfo.index[row]
        if pos in positionDict: #assuming values of positionDict are POSITIVE
            if pos not in foundPositionDict:
                foundPositionDict[pos] = 1
                cost += salary
                lineup.append(name)
            elif foundPositionDict[pos] < positionDict[pos]:
                foundPositionDict[pos] += 1
                cost += salary
                lineup.append(name)

    playerInfo["Efficiency"] = pd.to_numeric(playerInfo["Value"])/pd.to_numeric(playerInfo["Salary"])
    efficientPlayerInfo = playerInfo.sort_values("Efficiency", ascending=False)
    lineup.sort(key = lambda x: playerInfo.loc[x]["Efficiency"]) #sort by increasing efficiency

    for index in range(len(lineup)): #replace least efficient players first
        continue #playerInfo[playerInfo["Position"] == playerInfo.loc[lineup[index]]["position"]]

    print(efficientPlayerInfo)
    return lineup

def describeLineup(playerInfo, lineup):
    totalValue = 0
    totalSalary = 0
    for name in lineup:
        totalValue += int(playerInfo.loc[name]["Value"])
        totalSalary += int(playerInfo.loc[name]["Salary"])
    print("This lineup has value index {} and requires a salary of ${}.".format(totalValue, totalSalary))

def main():
    playerInfo = pd.read_csv("playerinfo.csv")
    playerInfo.set_index("Name", inplace=True)

    cap = 20000
    positionDict = {"QB":1, "TE":1, "WR":2}
    lineup = buildLineup(playerInfo, positionDict, cap)

    print(lineup, "\n")
    describeLineup(playerInfo, lineup)

if __name__ == '__main__':
    main()
