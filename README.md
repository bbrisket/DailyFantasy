# DailyFantasy
A project to build optimal lineups for daily fantasy purposes.

Data was pulled from rotogrinder (DraftKings contest stats), rotoguru (DraftKings salaries), and Pro Football Reference (NFL stats).

## Current usage
Select a DraftKings upcoming contest (on the website, not the mobile app) and download the accompanying .csv file. Open assemble_lineup.py, navigate to the `main()` function and set `import_csv_flag` to `True`. Then set `csv_path` to the path where your downloded .csv file was saved. In the last line of the main() function, specify the contest type ("classic" or "showdown") and pick the number of lineups to output. The variance across generated lineups can be changed by altering the max_overlap argument.

Note: The DraftKings .csv file contains a column named `AvgPtsPerGame` that is currently the basis for our code's projections. In the event that you have different projected scores for specific players, edit the values directly within the DraftKings .csv file. 




## Files
------
[COMPLETE]
* build_DB.py - Sets up a SQL database (dfs.db) for storing contest data and player data
* build_csv.py - Creates .csv files for each table found within dfs.db

[FUNCTIONAL/IN PROGRESS]
* assemble_lineup.py - Builds the optimal lineup using a CVXPY multi-variable programmer
* contest_analysis.ipynb - Contains visualizations and explorations of contest data
------
[NONFUNCTIONAL/IN PROGRESS]
* build_LOL.py - Analogue for esports; currently lacks a comprehensive source for player performance statistics

------
[DATA]
* dfs.db - SQL database with the following tables:
	* NFL_CONTESTS - has columns: 'Name', 'Link', 'Prize Pool', 'Buy In', 'Top Prize', 'Max Entries', 'Entries', 'Cash Line', 'Winner', 'Winning Score', 'Week'
	* NFL_STATS_PASS - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'pass_cmp', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_int', 'pass_rating', 'pass_sacked', 'pass_sacked_yds', 'pass_yds_per_att', 'pass_adj_yds_per_att'
	* NFL_STATS_RUSH - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'rush_att', 'rush_yds', 'rush_yds_per_att', 'rush_td'
	* NFL_STATS_REC - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'targets', 'rec', 'rec_yds', 'rec_yds_per_rec', 'rec_td', 'catch_pct', 'rec_yds_per_tgt'
	* NFL_STATS_DEF - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'sacks', 'tackles_solo', 'tackles_assists', 'tackles_combined', 'tackles_loss', 'qb_hits'
	* NFL_SALARIES - has columns: 'Week', 'Year', 'GID', 'Name', 'Pos', 'Team', 'h/a', 'Oppt', 'DK points', 'DK salary'
* DK_NFL_contest_data_2018.xlsx - Self-curated file containing stats regarding all DraftKings NFL contests during the 2018 regular season
