import pandas as pd

#input: DataFrame containing player name, position, value, salary
#assume that players.keys() == salaries.keys()
def knapsack(playerinfo, positionDict, cap):
    '''
    playerinfo: Pandas DataFrame containing player name, position, value, Salary
    positionDict: Dictionary with keys representing each position needed and
        values representing the number of players from those positions required
    cap: Integer representing salary cap

    knapsack() returns a list of player names, representing the lineup of
    maximum value that fulfills the position requirement and stays below the
    salary cap.
    '''
    for position in positionDict:
        continue
    return 0

def describeLineup(playerinfo, lineup):
    totalValue = 0
    totalSalary = 0
    for player in lineup:
        totalValue += int(playerinfo.loc[player]["Value"])
        totalSalary += int(playerinfo.loc[player]["Salary"])
    print("This lineup has value index {} and requires a salary of ${}.".format(totalValue, totalSalary))

def main():
    playerinfo = pd.read_csv("playerinfo.csv")
    playerinfo.set_index("Name", inplace=True)
    print(playerinfo)

    cap = 20000
    #lineup = knapsack(playerinfo, cap)
    lineup = ["Bob", "Carol", "Eunice"]
    describeLineup(playerinfo, lineup)

if __name__ == '__main__':
    main()
