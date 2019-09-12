import pandas as pd
import numpy as np
import sqlalchemy as db
import sqlite3
import cvxpy as cp

team_names = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", #PFR abbreviations
              "DAL", "DEN", "DET", "GNB", "HOU", "IND", "JAX", "KAN",
              "LAC", "LAR", "MIA", "MIN", "NOR", "NWE", "NGY", "NYJ",
              "OAK", "PHI", "PIT", "SEA", "SFO", "TAM", "TEN", "WAS"] + \
             ["TB"] #DraftKings abbreviations

def solve_classic_contest(df, num_lineups, max_overlap = 6):
    """
    Compute the best possible lineups for entering a DraftKings Classic NFL contest.
    """
    lineups = []
    for i in range(num_lineups):
        selection = cp.Variable(shape = len(df), boolean = True)

        ### Salary constraints
        salary_constraint = cp.sum(df["salary"].values * selection) <= 50000

        ### Positional constraints
        lineup_size_constraint = cp.sum(selection) == 9

        num_qb = cp.sum((df["pos"] == "QB").values * selection)
        num_rb = cp.sum((df["pos"] == "RB").values * selection)
        num_wr = cp.sum((df["pos"] == "WR").values * selection)
        num_te = cp.sum((df["pos"] == "TE").values * selection)
        num_def = cp.sum((df["pos"] == "DEF").values * selection)

        num_qb_constraint = num_qb == 1
        min_rb_constraint = num_rb >= 2
        max_rb_constraint = num_rb <= 3
        min_wr_constraint = num_wr >= 3
        max_wr_constraint = num_wr <= 4
        min_te_constraint = num_te >= 1
        max_te_constraint = num_te <= 2
        num_def_constraint = num_def == 1

        ### Differentiate lineups
        lineup_constraints = []
        for lineup in lineups:
            lineup_constraints.append(cp.sum(lineup * selection) <= max_overlap) # max num. players that can match between lineups

        ### Define multi-integer problem
        objective = cp.Maximize(df["score"].values * selection)
        problem = cp.Problem(objective, [salary_constraint,
                                         lineup_size_constraint,
                                         num_qb_constraint,
                                         min_rb_constraint,
                                         max_rb_constraint,
                                         min_wr_constraint,
                                         max_wr_constraint,
                                         min_te_constraint,
                                         max_te_constraint,
                                         num_def_constraint] + lineup_constraints)
        problem.solve()

        ### Add result to list
        rounded_selection = np.rint(selection.value)
        lineups.append(rounded_selection)

    result = []
    for lineup in lineups:
        players = []
        pos = []
        teams = []
        scores = []
        salaries = []
        for row_idx in range(len(lineup)):
            if lineup[row_idx]:
                players.append(df.iloc[row_idx]["player"])
                pos.append(df.iloc[row_idx]["pos"])
                teams.append(df.iloc[row_idx]["team"])
                scores.append(df.iloc[row_idx]["score"])
                salaries.append(df.iloc[row_idx]["salary"])
        result.append(pd.DataFrame(list(zip(players, pos, teams, scores, salaries))))

    return result

def solve_showdown_contest(df, num_lineups, max_overlap = 4):
    """
    Compute the best possible lineups for entering a DraftKings Showdown NFL contest.
    """
    lineups = []
    for i in range(num_lineups):
        captain = cp.Variable(shape = len(df), boolean = True)
        selection = cp.Variable(shape = len(df), boolean = True)

        ### Uniqueness constraints
        uniqueness_constraint = captain + selection <= 1

        ### Salary constraints
        salary_constraint = cp.sum(df["salary"].values * (cp.multiply(1.5, captain) + selection)) <= 50000

        ### Positional constraints
        captain_size_constraint = cp.sum(captain) == 1
        lineup_size_constraint = cp.sum(selection) == 5

        ### Differentiate lineups
        lineup_constraints = []
        for lineup in lineups:
            lineup_constraints.append(cp.sum(lineup * (selection)) <= max_overlap) # max num. players that can match between lineups

        ### Define multi-integer problem
        objective = cp.Maximize(df["score"].values * (cp.multiply(1.5, captain) + selection)) #cp.multiply(1.5, captain) +
        problem = cp.Problem(objective, [uniqueness_constraint,
                                         salary_constraint,
                                         captain_size_constraint,
                                         lineup_size_constraint] + lineup_constraints)
        problem.solve()

        ### Add result to list
        rounded_selection = np.rint(captain.value) + np.rint(selection.value)
        lineups.append(rounded_selection)

    ### Return results
    result = []
    for lineup in lineups:
        players = []
        pos = []
        teams = []
        scores = []
        salaries = []
        first_flag = True
        for row_idx in range(len(lineup)):
            if lineup[row_idx]:
                if first_flag:
                    players.append(df.iloc[row_idx]["player"] + " [C]")
                    scores.append(df.iloc[row_idx]["score"] * 1.5)
                    salaries.append(df.iloc[row_idx]["salary"] * 1.5)
                    first_flag = False
                else:
                    players.append(df.iloc[row_idx]["player"])
                    scores.append(df.iloc[row_idx]["score"])
                    salaries.append(df.iloc[row_idx]["salary"])

                pos.append(df.iloc[row_idx]["pos"])
                teams.append(df.iloc[row_idx]["team"])
        result.append(pd.DataFrame(list(zip(players, pos, teams, scores, salaries))))

    return result

def solve_ip(df, contest_type, num_lineups, valid_teams = team_names):
    """
    Solve the integer programming problem of maximizing projected fantasy points
    subject to multiple lineup constraints.

    contest_type (str): "classic" or "showdown", depending on which DraftKings contest format is entered
    num_lineups (int): number of lineups to return
    valid_teams (str list): list of teams eligible for the entered contest
    """
    slimmed_df = df[["player", "pos", "team", "score", "salary"]].replace("", np.nan).dropna()
    slimmed_df["score"] = slimmed_df["score"].astype(str).str.strip().astype(float)
    slimmed_df["salary"] = slimmed_df["salary"].astype(str).str.strip().astype(float)
    slimmed_df = slimmed_df[slimmed_df["team"].isin(valid_teams)]

    lineups = []
    if contest_type == "classic":
        lineups = solve_classic_contest(slimmed_df, num_lineups)
    elif contest_type == "showdown":
        lineups = solve_showdown_contest(slimmed_df, num_lineups)

    for lineup in lineups:
        print(lineup)

def main():
    import_csv_flag = True
    if import_csv_flag:
        csv_path = "DKSalaries.csv"
        data = pd.read_csv(csv_path)
        data = data[data["Roster Position"] != "CPT"]
        data.columns = ["pos", "name_id", "player", "id", "rost_pos", "salary",
                        "game_time", "team", "score"]
    else:

        engine = db.create_engine("sqlite:///data/dfs.db")
        con = engine.connect()
        data = pd.read_sql_query("SELECT * \
                                  FROM NFL_SALARIES \
                                  WHERE year = 2019 AND week_num = 1", con)
        con.close()

    solve_ip(data, contest_type = "showdown", num_lineups = 1)

if __name__ == "__main__":
    main()
