# DailyFantasy
A project to build optimal lineups for daily fantasy purposes.

[IN PROGRESS]

* DK_NFL_contest_data_2018.xlsx - Self-curated file containing stats regarding all DraftKings NFL contests during the 2018 regular season
* dfs.db - SQL database with the following tables:
	* CONTESTS - has columns:Name, Link, Prize Pool, Buy In, Top Prize, Max Entries,
	Entries, Cash Line, Winner, Winning Score, Week.
* setupDB.py - Sets up an SQL database (dfs.db) for storing contest data and player data
* lineupBuilder.py - Builds the optimal lineup based on predetermined 
* contestAnalysis.ipynb - Contains visualizations and explorations of contest data
------
* dataCleaner.py - Becoming obsolete in favor of setupDB.py
* LOL_builder.py - Currently lacks a comprehensive source of stats




