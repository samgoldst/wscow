#WEBSCRAPING STATFOX
import re
import json
import requests
import csv
import numpy as np
import math
import time
from random import randint
from collections import defaultdict
from bs4 import BeautifulSoup

### FIX TIES

teams_by_sport = {"NFL": ["ARIZONA", "ATLANTA", "BALTIMORE", "BUFFALO", "CAROLINA", "CHICAGO", "CINCINNATI", "CLEVELAND", "DALLAS", "DENVER", "DETROIT", "GREEN BAY", "HOUSTON", "INDIANAPOLIS", "JACKSONVILLE", "KANSAS CITY", "LA CHARGERS", "LA RAMS", "LAS VEGAS", "MIAMI", "MINNESOTA", "NEW ENGLAND", "NEW ORLEANS", "NY GIANTS", "NY JETS", "OAKLAND", "PHILADELPHIA", "PITTSBURGH", "SAN DIEGO", "SAN FRANCISCO", "SEATTLE", "ST LOUIS", "TAMPA BAY", "TENNESSEE", "WASHINGTON"],
                  "CFB": ["AIR FORCE", "AKRON", "ALABAMA", "APPALACHIAN ST", "ARIZONA", "ARIZONA ST", "ARKANSAS", "ARKANSAS ST", "ARMY", "AUBURN", "BALL ST", "BAYLOR", "BOISE ST", "BOSTON COLLEGE", "BOWLING GREEN", "BUFFALO", "BYU", "C MICHIGAN", "CALIFORNIA", "CHARLOTTE", "CINCINNATI", "CLEMSON", "COASTAL CAROLINA", "COLORADO", "COLORADO ST", "CONNECTICUT", "DUKE", "E CAROLINA", "E MICHIGAN", "FLA ATLANTIC", "FLA INTERNATIONAL", "FLORIDA", "FLORIDA ST", "FRESNO ST", "GA SOUTHERN", "GEORGIA", "GEORGIA ST", "GEORGIA TECH", "HAWAII", "HOUSTON", "ILLINOIS", "INDIANA", "IOWA", "IOWA ST", "JACKSONVILLE ST", "JAMES MADISON", "KANSAS", "KANSAS ST", "KENT ST", "KENTUCKY", "LA LAFAYETTE", "LA MONROE", "LIBERTY", "LOUISIANA TECH", "LOUISVILLE", "LSU", "MARSHALL", "MARYLAND", "MASSACHUSETTS", "MEMPHIS", "MIAMI", "MIAMI OHIO", "MICHIGAN", "MICHIGAN ST", "MIDDLE TENN ST", "MINNESOTA", "MISSISSIPPI ST", "MISSOURI", "N CAROLINA", "N ILLINOIS", "NAVY", "NC STATE", "NEBRASKA", "NEVADA", "NEW MEXICO", "NEW MEXICO ST", "NORTH TEXAS", "NORTHWESTERN", "NOTRE DAME", "OHIO ST", "OHIO U", "OKLAHOMA", "OKLAHOMA ST", "OLD DOMINION", "OLE MISS", "OREGON", "OREGON ST", "PENN ST", "PITTSBURGH", "PURDUE", "RICE", "RUTGERS", "S ALABAMA", "S CAROLINA", "S FLORIDA", "SAM HOUSTON ST", "SAN DIEGO ST", "SAN JOSE ST", "SMU", "SOUTHERN MISS", "STANFORD", "SYRACUSE", "TCU", "TEMPLE", "TENNESSEE", "TEXAS", "TEXAS A&M", "TEXAS ST", "TEXAS TECH", "TOLEDO", "TROY", "TULANE", "TULSA", "UAB", "UCF", "UCLA", "UNLV", "USC", "UTAH", "UTAH ST", "UTEP", "UTSA", "VANDERBILT", "VIRGINIA", "VIRGINIA TECH", "W KENTUCKY", "W MICHIGAN", "W VIRGINIA", "WAKE FOREST", "WASHINGTON", "WASHINGTON ST", "WISCONSIN", "WYOMING"],
                  "CBB": ["ABILENE CHRISTIAN", "AIR FORCE", "AKRON", "ALABAMA", "ALABAMA A&M", "ALABAMA ST", "ALBANY", "ALCORN ST", "AMERICAN", "APPALACHIAN ST", "ARIZONA", "ARIZONA ST", "ARK-LITTLE ROCK", "ARK-PINE BLUFF", "ARKANSAS", "ARKANSAS ST", "ARMY", "AUBURN", "AUSTIN PEAY", "BALL ST", "BAYLOR", "BELLARMINE", "BELMONT", "BETHUNE-COOKMAN", "BINGHAMTON", "BOISE ST", "BOSTON COLLEGE", "BOSTON U", "BOWLING GREEN", "BRADLEY", "BROWN", "BRYANT", "BUCKNELL", "BUFFALO", "BUTLER", "BYU", "C ARKANSAS", "C CONN ST", "C MICHIGAN", "CAL BAPTIST", "CAL DAVIS", "CAL POLY-SLO", "CAL SAN DIEGO", "CALIFORNIA", "CAMPBELL", "CANISIUS", "CHARLESTON SO", "CHARLOTTE", "CHICAGO ST", "CINCINNATI", "CLEMSON", "CLEVELAND ST", "COASTAL CAROLINA", "COLGATE", "COLL OF CHARLESTON", "COLORADO", "COLORADO ST", "COLUMBIA", "CONNECTICUT", "COPPIN ST", "CORNELL", "CREIGHTON", "CS-BAKERSFIELD", "CS-FULLERTON", "CS-NORTHRIDGE", "DARTMOUTH", "DAVIDSON", "DAYTON", "DELAWARE", "DELAWARE ST", "DENVER", "DEPAUL", "DETROIT", "DRAKE", "DREXEL", "DUKE", "DUQUESNE", "E CAROLINA", "E ILLINOIS", "E KENTUCKY", "E MICHIGAN", "E TENN ST", "E WASHINGTON", "ELON", "EVANSVILLE", "FAIRFIELD", "FARLEIGH DICKINSON", "FLA ATLANTIC", "FLA GULF COAST", "FLA INTERNATIONAL", "FLORIDA", "FLORIDA A&M", "FLORIDA ST", "FORDHAM", "FRESNO ST", "FURMAN", "GA SOUTHERN", "GARDNER WEBB", "GEORGE MASON", "GEORGE WASHINGTON", "GEORGETOWN", "GEORGIA", "GEORGIA ST", "GEORGIA TECH", "GONZAGA", "GRAMBLING", "GRAND CANYON", "HAMPTON", "HARVARD", "HAWAII", "HIGH POINT", "HOFSTRA", "HOLY CROSS", "HOUSTON", "HOUSTON CHRISTIAN", "HOWARD", "IDAHO", "IDAHO ST", "IL-CHICAGO", "ILLINOIS", "ILLINOIS ST", "INCARNATE WORD", "INDIANA", "INDIANA ST", "IONA", "IOWA", "IOWA ST", "IUPU-FT WAYNE", "IUPUI", "JACKSON ST", "JACKSONVILLE", "JACKSONVILLE ST", "JAMES MADISON", "KANSAS", "KANSAS ST", "KENNESAW ST", "KENT ST", "KENTUCKY", "LA-LAFAYETTE", "LA-MONROE", "LAFAYETTE", "LAMAR", "LASALLE", "LEHIGH", "LEMOYNE", "LIBERTY", "LINDENWOOD", "LIPSCOMB", "LONG BEACH ST", "LONG ISLAND", "LONGWOOD", "LOUISIANA TECH", "LOUISVILLE", "LOYOLA-IL", "LOYOLA-MARYMOUNT", "LOYOLA-MD", "LSU", "MAINE", "MANHATTAN", "MARIST", "MARQUETTE", "MARSHALL", "MARYLAND", "MASSACHUSETTS", "MCNEESE ST", "MD-BALT COUNTY", "MD-EAST SHORE", "MEMPHIS", "MERCER", "MERRIMACK", "MIAMI", "MIAMI OHIO", "MICHIGAN", "MICHIGAN ST", "MIDDLE TENN ST", "MINNESOTA", "MISS VALLEY ST", "MISSISSIPPI ST", "MISSOURI", "MISSOURI ST", "MISSOURI-KC", "MONMOUTH", "MONTANA", "MONTANA ST", "MOREHEAD ST", "MORGAN ST", "MOUNT ST MARYS", "MURRAY ST", "N ALABAMA", "N ARIZONA", "N CAROLINA", "N CAROLINA A&T", "N COLORADO", "N DAKOTA", "N DAKOTA ST", "N FLORIDA", "N ILLINOIS", "N IOWA", "N KENTUCKY", "N TEXAS", "NAVY", "NC CENTRAL", "NC STATE", "NEBRASKA", "NEBRASKA-OMAHA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY TECH", "NEW MEXICO", "NEW MEXICO ST", "NEW ORLEANS", "NIAGARA", "NICHOLLS ST", "NORFOLK ST", "NORTHEASTERN", "NORTHWESTERN", "NORTHWESTERN ST", "NOTRE DAME", "OAKLAND", "OHIO ST", "OHIO U", "OKLAHOMA", "OKLAHOMA ST", "OLD DOMINION", "OLE MISS", "ORAL ROBERTS", "OREGON", "OREGON ST", "PACIFIC", "PENN ST", "PENNSYLVANIA", "PEPPERDINE", "PITTSBURGH", "PORTLAND", "PORTLAND ST", "PRAIRIE VIEW A&M", "PRESBYTERIAN", "PRINCETON", "PROVIDENCE", "PURDUE", "QUEENS U - CHAR", "QUINNIPIAC", "RADFORD", "RHODE ISLAND", "RICE", "RICHMOND", "RIDER", "ROBERT MORRIS", "RUTGERS", "S ALABAMA", "S CAROLINA", "S CAROLINA ST", "S DAKOTA", "S DAKOTA ST", "S FLORIDA", "S ILLINOIS", "S INDIANA", "SACRAMENTO ST", "SACRED HEART", "SAINT LOUIS", "SAM HOUSTON ST", "SAMFORD", "SAN DIEGO", "SAN DIEGO ST", "SAN FRANCISCO", "SAN JOSE ST", "SANTA CLARA", "SAVANNAH ST", "SE LOUISIANA", "SE MISSOURI ST", "SEATTLE", "SETON HALL", "SF AUSTIN ST", "SIENA", "SIU EDWARDSVL", "SMU", "SOUTHERN MISS", "SOUTHERN U", "SOUTHERN UTAH", "ST BONAVENTURE", "ST FRANCIS-NY", "ST FRANCIS-PA", "ST JOHNS", "ST JOSEPHS", "ST MARYS-CA", "ST PETERS", "ST THOMAS (MN)", "STANFORD", "STETSON", "STONEHILL", "STONY BROOK", "SYRACUSE", "TARLETON ST", "TCU", "TEMPLE", "TENN-MARTIN", "TENNESSEE", "TENNESSEE ST", "TENNESSEE TECH", "TEXAS", "TEXAS A&M", "TEXAS A&M CC", "TEXAS A&M-COMM", "TEXAS SOUTHERN", "TEXAS ST", "TEXAS TECH", "THE CITADEL", "TOLEDO", "TOWSON ST", "TROY", "TULANE", "TULSA", "TX-ARLINGTON", "TX-SAN ANTONIO", "UAB", "UC-IRVINE", "UC-RIVERSIDE", "UC-SANTA BARBARA", "UCF", "UCLA", "UMASS-LOWELL", "UNC-ASHEVILLE", "UNC-GREENSBORO", "UNC-WILMINGTON", "UNLV", "USC", "USC UPSTATE", "UT-CHATTANOOGA", "UTAH", "UTAH ST", "UTAH TECH", "UTAH VALLEY ST", "UTEP", "UTRGV", "VA COMMONWEALTH", "VALPARAISO", "VANDERBILT", "VERMONT", "VILLANOVA", "VIRGINIA", "VIRGINIA TECH", "VMI", "W CAROLINA", "W ILLINOIS", "W KENTUCKY", "W MICHIGAN", "W VIRGINIA", "WAGNER", "WAKE FOREST", "WASHINGTON", "WASHINGTON ST", "WEBER ST", "WI-GREEN BAY", "WI-MILWAUKEE", "WICHITA ST", "WINTHROP", "WISCONSIN", "WM & MARY", "WOFFORD", "WRIGHT ST", "WYOMING", "XAVIER", "YALE", "YOUNGSTOWN ST"],
                  "NBA": ["ATLANTA", "BOSTON", "BROOKLYN", "CHARLOTTE", "CHICAGO", "CLEVELAND", "DALLAS", "DENVER", "DETROIT", "GOLDEN STATE", "HOUSTON", "INDIANA", "LA CLIPPERS", "LA LAKERS", "MEMPHIS", "MIAMI", "MILWAUKEE", "MINNESOTA", "NEW ORLEANS", "NEW YORK", "OKLAHOMA CITY", "ORLANDO", "PHILADELPHIA", "PHOENIX", "PORTLAND", "SACRAMENTO", "SAN ANTONIO", "TORONTO", "UTAH", "WASHINGTON"]
                 }

saved_probs = {}

def get_games(sport, season, all):
    teams = teams_by_sport[sport]
    all_games = []

    for team in teams:
        if sport == "NFL": html = requests.get(f"https://statfox.com/nfl/gamelog.asp?teamid={team}&season={season}").text
        if sport == "CFB": html = requests.get(f"https://statfox.com/cfb/gamelog.asp?teamid={team}&season={season}").text
        if sport == "CBB": html = requests.get(f"https://statfox.com/cbb/cbbteam.asp?teamid={team}&season={season}&log={all}").text
#         if sport == "NBA": html = requests.get(f"https://statfox.com/nba/nbateam.asp?teamid={team}&season={season}").text
        soup = BeautifulSoup(html, 'html.parser')
#         if sport == "NBA":
#             if season > 2003:     **NBA DOES NOT WORK**
#                ind = 34
#             else:
#                ind = 27
#         else:
        ind = 13
        table  = soup.find_all("tr")[ind]
        rows = []
        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                header = [el.text.strip() for el in row.find_all('th')]
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])
        for game in rows:
            if game[1][3:] in teams_by_sport[sport]:
                if game[5] == 'W':
                    all_games.append((team, game[4].split('-')[0], game[1][3:], game[4].split('-')[1]))
        print(f"\r{team}", end ="")
    return all_games

def save_to_csv(rows, output_name):
    with open(f"{output_name}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def get_c(sport):
    if sport == "NFL": return 3.0
    if sport == "CFB": return 3.0
    if sport == "MLB": return 3.7
    if sport == "CBB": return 14.0
    if sport == "NBA": return 18.0

def elo(old, exp, score, k):
    return old + k * (score - exp)

def expected(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))

def game_score(a, b, sport, g = .5):
    c = get_c(sport)
    if (a,b) in saved_probs:
        return saved_probs[(a,b)]
    d = a - b
    if a == 0:  a = 1
    if b == 0:  b = 1
    m_1 = (max(a , 1) * (a + c))/(max(b, 1) * (b + c))
    m_2 = -(2*c*d/(a + b))**(1+d/(a+b))
    prob = (1-g)/(1+(m_1**m_2)) + g
    saved_probs[(a,b)] = prob
    return prob

def load_games(filename):
    games = []
    file = open(filename)
    csvreader = csv.reader(file)
    for game in csvreader:
        games.append([game[0], int(game[1]), game[2], int(game[3])])
    file.close()
    return games

def get_elos(games, trials, d, sport,  starting_elos = {}):
    s = 1 - (10/d)
    d = d // 100
    trial_elos = {}
    for team in teams_by_sport[sport]:
        trial_elos[team] = []
    for trial in range(trials):
        if len(starting_elos) == 0:
            elos = defaultdict(lambda: 1600)
        else:
            elos = starting_elos.copy()
        sensitivity = 600.0
        l = len(games)
        for t in range(100):
            for i in range(d):
                sensitivity *= s
                game = games[randint(1, l-1)]
                winner = game[0]
                winner_score = int(game[1])
                loser = game[2]
                loser_score = int(game[3])
                winner_exp = expected(elos[winner], elos[loser])
                loser_exp = 1 - winner_exp
                winner_prob = game_score(winner_score, loser_score, sport)
                loser_prob = 1 - winner_prob
                elos[winner] = elo(elos[winner], winner_exp, winner_prob, k=sensitivity)
                elos[loser] = elo(elos[loser], loser_exp, loser_prob, k=sensitivity)
            print("\r" + "{:.2f}".format(((100 * trial / trials) + (t/trials))) + "% done with elos", end="")
        for team in teams_by_sport[sport]:
            trial_elos[team].append(elos[team])
    print("\rFINISHED CALCULATING ELOS!!        ")
    return [(k, *v) for k, v in trial_elos.items()]

def recalculate_team(team, all_games, elos, sims, sport):
    team_elos = []
    applicable_games = []
    for g in games:
        if g[0] == team:
            applicable_games.append(['W', g[2], float(elos[g[2]]), int(g[1]), int(g[3])])
        if g[2] == team:
            applicable_games.append(['L', g[0], float(elos[g[0]]), int(g[1]), int(g[3])])
        l = len(applicable_games)
    if l == 0:
        return -1
    for i in range(100):
        team_elo = float(elos[team])
        sensitivity = 5
        s = 1 - (10/sims)
        for t in range(sims):
            sensitivity *= s
            game = applicable_games[randint(1, l-1)]
            if game[0] == 'W':
                team_exp = expected(team_elo, game[2])
                team_score = game_score(game[3], game[4], sport)
                team_elo = elo(team_elo, team_exp, team_score, k=sensitivity)
            if game[0] == 'L':
                team_exp = expected(team_elo, game[2])
                team_score = 1 - game_score(game[3], game[4], sport)
                team_elo = elo(team_elo, team_exp, team_score, k=sensitivity)
        team_elos.append(team_elo)
    return [np.mean(team_elos), np.var(team_elos)**(1/2)]

def recalculate_all_teams(elos, games, sims_per_team, sport):
    new_elos = {}
    for team in elos:
        print(f"\r{team}", end="")
        new_elo = recalculate_team(team, games, elos, sims_per_team, sport)
        if new_elo == -1:
            continue
        new_elos[team] = new_elo
    return [[k, *v] for k, v in new_elos.items()]

def load_processed_elos(filename):
    elos = {}
    file = open(filename)
    csvreader = csv.reader(file)
    for team in csvreader:
        elos[team[0]] = team[5]
    file.close()
    return elos

def average_elos(elos):
    output = []
    for item in elos:
#         output[item[0]] = [np.percentile(item[1:], n * 10) for n in range(0, 11)]
        output.append([item[0], *[np.percentile(item[1:], n * 10) for n in range(0, 11)]])
    return output

# games = get_games("CBB", 2024, 1)
# save_to_csv(games, "CBB_GAMES_L20_2024")
games = load_games("CBB_GAMES_L20_2024.csv")
elos = load_processed_elos("CBB_ELOS_ALL_2024.csv")
# elos = get_elos(games, 250, 1000000, "CBB")
# processed_elos = average_elos(elos)
# print(processed_elos)
new_elos = recalculate_all_teams(elos, games, 1000, "CBB")
save_to_csv(new_elos, "CBB_ELOS_L20_2024")
# save_to_csv([[k, *v] for k, v in processed_elos.items()], f"CBB_ELOS_ALL_2024")

# elos_by_season = {}
# for team in teams_by_sport["NFL"]:
#     elos_by_season[team] = []
#
# for season in range(1999, 2024):
#     print(season)
#     games = get_games("NFL", season)
# #     games = load_games(f"NFL({season})GAMES.csv")
#     save_to_csv(games, f"NFL({season})GAMES")
#     elos = get_elos(games, 16, 1000000, "NFL")
#     processed_elos = average_elos(elos)
#     for team in teams_by_sport["NFL"]:
#         elos_by_season[team].append(processed_elos[team][0])
#     save_to_csv([[k, *v] for k, v in processed_elos.items()], f"NFL({season})ELOS")
#
# for team in teams_by_sport["NFL"]:
#     print(team, ":", elos_by_season[team])
