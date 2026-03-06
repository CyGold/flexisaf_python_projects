## PROJECT OVERVIEW
This is a weather tracker that fecths live data from Open-Meteo

## PREREQUISITE
-Python 3.10+ installed
-sqlite3 CLI installed or use the free GUI tool(DB Browser) at sqlitebrowser.org to open weather.db visually.

##
Clone the repositoriry
'''
git clone https://github.com/CyGold/flexisaf_python_projects/tree/main/final%20project
'''
change directory
"""
cd final project
"""
Run the code
"""
python3 main.py
"""

Inspect the database with the sqlite3 CLI
"""
sqlite3 weather.db
"""
Then inside the shell:
'''.tables
SELECT * FROM weather_records;
.quit '''

