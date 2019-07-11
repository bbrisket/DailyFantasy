import pandas as pd

def buildLineup(player_info, position_dict, cap):
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
    net_cost = 0
    net_value = 0

    found_position_dict = {}
    cheap_player_info = playerInfo.sort_values("Salary") #sort by cheapest player

    for i in range(len(cheap_player_info)): #build basic lineup
        pos = cheap_player_info.iloc[i]["Position"]
        salary = cheap_player_info.iloc[i]["Salary"]
        value = cheap_player_info.iloc[i]["Value"]
        name = cheap_player_info.index[i]
        if pos in position_dict: #assuming values of positionDict are POSITIVE
            if pos not in found_position_dict:
                found_position_dict[pos] = 1
                net_cost += salary
                net_value += value
                lineup.append(name)
            elif found_position_dict[pos] < position_dict[pos]:
                found_position_dict[pos] += 1
                net_cost += salary
                net_value += value
                lineup.append(name)

    if net_cost > cap: #sanity check
        print("Error: total cost of cheapest possible lineup exceeds salary cap.")
        return None

    player_info["Efficiency"] = pd.to_numeric(player_info["Value"])/pd.to_numeric(player_info["Salary"])
    efficient_player_info = player_info.sort_values("Efficiency", ascending=False)
    lineup.sort(key = lambda x: player_info.loc[x]["Efficiency"]) #sort by increasing efficiency
    print(efficient_player_info)

    for i in range(len(lineup)): #replace least efficient players first
        pos = player_info.loc[lineup[i]]["Position"]
        salary = player_info.loc[lineup[i]]["Salary"]
        value = player_info.loc[lineup[i]]["Value"]
        pos_pool = player_info[player_info["Position"] == pos].sort_values("Efficiency", ascending=False)
        for j in range(len(pos_pool)):
            name = pos_pool.index[j]
            new_cost = net_cost - salary + playerInfo.loc[name]["Salary"]
            new_value = net_value - value + playerInfo.loc[name]["Value"]
            if name not in lineup and new_value > net_value and new_cost <= cap: #update player
                lineup[i] = name
                net_cost = new_cost
                net_value = new_value

    return lineup

def describeLineup(player_info, lineup):
    total_value = 0
    total_salary = 0
    for name in lineup:
        total_value += int(player_info.loc[name]["Value"])
        total_salary += int(player_info.loc[name]["Salary"])
    print("This lineup has value index {} and requires a salary of ${}.".format(total_value, total_salary))

def main():
    player_info = pd.read_csv("playerinfo.csv")
    player_info.set_index("Name", inplace=True)

    cap = 20000
    position_dict = {"QB":1, "TE":1, "WR":2} #positional requirements
    lineup = buildLineup(player_info, position_dict, cap)

    print(lineup, "\n")
    describeLineup(player_info, lineup)

if __name__ == '__main__':
    main()
