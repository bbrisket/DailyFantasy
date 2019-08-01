# DailyFantasy
A project to build optimal lineups for daily fantasy purposes.

Stats were pulled from rotogrinder and Pro Football Reference.

[COMPLETE]
* DK_NFL_contest_data_2018.xlsx - Self-curated file containing stats regarding all DraftKings NFL contests during the 2018 regular season
* build_DB.py - Sets up an SQL database (dfs.db) for storing contest data and player data
* dfs.db - SQL database with the following tables:
	* NFL_CONTESTS - has columns: 'Name', 'Link', 'Prize Pool', 'Buy In', 'Top Prize', 'Max Entries', 'Entries', 'Cash Line', 'Winner', 'Winning Score', 'Week'
	* NFL_STATS_PASS - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'pass_cmp', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_int', 'pass_rating', 'pass_sacked', 'pass_sacked_yds', 'pass_yds_per_att', 'pass_adj_yds_per_att'
	* NFL_STATS_RUSH - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'rush_att', 'rush_yds', 'rush_yds_per_att', 'rush_td'
	* NFL_STATS_REC - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'targets', 'rec', 'rec_yds', 'rec_yds_per_rec', 'rec_td', 'catch_pct', 'rec_yds_per_tgt'
	* NFL_STATS_DEF - has columns: 'player', 'pos', 'age', 'game_date', 'league_id', 'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num', 'game_day_of_week', 'sacks', 'tackles_solo', 'tackles_assists', 'tackles_combined', 'tackles_loss', 'qb_hits'

[FUNCTIONAL/IN PROGRESS]
* contest_analysis.ipynb - Contains visualizations and explorations of contest data
------
[NONFUNCTIONAL/IN PROGRESS]
* assemble_lineup.py - Builds the optimal lineup based on stats scraped from Pro Football Reference
* build_LOL.py - Analogue for esports; currently lacks a comprehensive source of stats




