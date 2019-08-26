import pandas as pd
import numpy as np
import sqlalchemy as db
import sqlite3
import cvxpy as cp

def get_selection(df, selection):
    """
    Produce a Pandas DataFrame describing the selected lineup.
    """

    players = []
    pos = []
    scores = []
    salaries = []
    for row_idx in range(len(selection)):
        if selection[row_idx]:
            players.append(df.iloc[row_idx]["player"])
            pos.append(df.iloc[row_idx]["pos"])
            scores.append(df.iloc[row_idx]["score"])
            salaries.append(df.iloc[row_idx]["salary"])
    return pd.DataFrame(list(zip(players, pos, scores, salaries)))

def solve_ip(df):
    """
    Solves integer programming problem subjected to certain lineup constraints.
    """
    slimmed_df = df[["player", "team", "pos", "score", "salary"]][(df["salary"] != "") & (df["score"] != "")]
    slimmed_df["score"] = slimmed_df["score"].str.strip().astype(float)
    slimmed_df["salary"] = slimmed_df["salary"].str.strip().astype(float)

    selection = cp.Variable(shape = len(slimmed_df), boolean = True)

    ### Salary constraints
    salary_constraint = slimmed_df["salary"].values * selection <= 50000

    ### Positional constraints
    lineup_size_constraint = cp.sum(selection) == 9

    num_qb = cp.sum((slimmed_df["pos"] == "QB").values * selection)
    num_rb = cp.sum((slimmed_df["pos"] == "RB").values * selection)
    num_wr = cp.sum((slimmed_df["pos"] == "WR").values * selection)
    num_te = cp.sum((slimmed_df["pos"] == "TE").values * selection)
    num_def = cp.sum((slimmed_df["pos"] == "DEF").values * selection)

    num_qb_constraint = num_qb == 1
    min_rb_constraint = num_rb >= 2
    max_rb_constraint = num_rb <= 3
    min_wr_constraint = num_wr >= 3
    max_wr_constraint = num_wr <= 4
    min_te_constraint = num_te >= 1
    max_te_constraint = num_te <= 2
    num_def_constraint = num_def == 1

    ### Define multi-integer problem
    objective = cp.Maximize(slimmed_df["score"].values * selection)
    problem = cp.Problem(objective, [salary_constraint,
                                     lineup_size_constraint,
                                     num_qb_constraint,
                                     min_rb_constraint,
                                     max_rb_constraint,
                                     min_wr_constraint,
                                     max_wr_constraint,
                                     min_te_constraint,
                                     max_te_constraint,
                                     num_def_constraint])
    problem.solve()

    ### Output the optimal lineup
    rounded_selection = np.rint(selection.value)
    return get_selection(slimmed_df, rounded_selection)

def main():
    engine = db.create_engine("sqlite:///data/dfs.db")
    con = engine.connect()
    data = pd.read_sql_query("SELECT * FROM NFL_SALARIES \
                              WHERE week_num = 1", con)
    con.close()

    lineup_df = solve_ip(data)
    print(lineup_df)

if __name__ == "__main__":
    main()
