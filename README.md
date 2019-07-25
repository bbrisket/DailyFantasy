# DailyFantasy
A project to build optimal lineups for daily fantasy purposes.

[IN PROGRESS]

* DK_NFL_contest_data_2018.xlsx - Self-curated file containing stats regarding all DraftKings NFL contests during the 2018 regular season
* dfs.db - SQL database with the following tables:
	* CONTESTS - has columns:Name, Link, Prize Pool, Buy In, Top Prize, Max Entries,
	Entries, Cash Line, Winner, Winning Score, Week.
* build_DB.py - Sets up an SQL database (dfs.db) for storing contest data and player data
* assemble_lineup.py - Builds the optimal lineup based on predetermined 
* contest_analysis.ipynb - Contains visualizations and explorations of contest data
------
* dataCleaner.py - Becoming obsolete in favor of setupDB.py
* build_LOL.py - Currently lacks a comprehensive source of stats




