import pandas as pd

def buildLineup(playerInfo, positionDict, cap):
    '''
    playerInfo: Pandas DataFrame containing player name, position, value, salary
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
    netCost = 0
    netValue = 0

    foundPositionDict = {}
    cheapPlayerInfo = playerInfo.sort_values("Salary") #sort by cheapest player

    for i in range(len(cheapPlayerInfo)): #build basic lineup
        pos = cheapPlayerInfo.iloc[i]["Position"]
        salary = cheapPlayerInfo.iloc[i]["Salary"]
        value = cheapPlayerInfo.iloc[i]["Value"]
        name = cheapPlayerInfo.index[i]
        if pos in positionDict: #assuming values of positionDict are POSITIVE
            if pos not in foundPositionDict:
                foundPositionDict[pos] = 1
                netCost += salary
                netValue += value
                lineup.append(name)
            elif foundPositionDict[pos] < positionDict[pos]:
                foundPositionDict[pos] += 1
                netCost += salary
                netValue += value
                lineup.append(name)

    if netCost > cap: #sanity check
        print("Error: total cost of cheapest possible lineup exceeds salary cap.")
        return None

    playerInfo["Efficiency"] = pd.to_numeric(playerInfo["Value"])/pd.to_numeric(playerInfo["Salary"])
    efficientPlayerInfo = playerInfo.sort_values("Efficiency", ascending=False)
    lineup.sort(key = lambda x: playerInfo.loc[x]["Efficiency"]) #sort by increasing efficiency
    print(efficientPlayerInfo)

    for i in range(len(lineup)): #replace least efficient players first
        pos = playerInfo.loc[lineup[i]]["Position"]
        salary = playerInfo.loc[lineup[i]]["Salary"]
        value = playerInfo.loc[lineup[i]]["Value"]
        posPool = playerInfo[playerInfo["Position"] == pos].sort_values("Efficiency", ascending=False)
        for j in range(len(posPool)):
            name = posPool.index[j]
            newCost = netCost - salary + playerInfo.loc[name]["Salary"]
            newValue = netValue - value + playerInfo.loc[name]["Value"]
            if name not in lineup and newValue > netValue and newCost <= cap: #update player
                lineup[i] = name
                netCost = newCost
                netValue = newValue

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
    positionDict = {"QB":1, "TE":1, "WR":2} #positional requirements
    lineup = buildLineup(playerInfo, positionDict, cap)

    print(lineup, "\n")
    describeLineup(playerInfo, lineup)

if __name__ == '__main__':
    main()
