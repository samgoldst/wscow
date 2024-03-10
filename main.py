#WEBSCRAPING STATFOX
import re
import json
import requests
import csv
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

def get_games(sport, season):
    teams = teams_by_sport[sport]
    all_games = []

    for team in teams:
        if sport == "NFL": html = requests.get(f"https://statfox.com/nfl/gamelog.asp?teamid={team}&season={season}").text
        if sport == "CFB": html = requests.get(f"https://statfox.com/cfb/gamelog.asp?teamid={team}&season={season}").text
        if sport == "CBB": html = requests.get(f"https://statfox.com/cbb/cbbteam.asp?teamid={team}&season={season}").text
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

def probability(a, b, sport, g = .5):
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


#load games exported from save_to_csv(game_list)
def load_games(filename):
    pass

#add functionality for trials

def get_elos(games, trials, sport):
    elos = defaultdict(lambda: 1600.0)
    sensitivity = 600.0
    l = len(games)
    for t in range(1000):
        for i in range(10000):
            sensitivity *= 0.999999
            game = games[randint(1, l-1)]
            winner = game[0]
            winner_score = int(game[1])
            loser = game[2]
            loser_score = int(game[3])
            winner_exp = expected(elos[winner], elos[loser])
            loser_exp = 1 - winner_exp
            winner_prob = probability(winner_score, loser_score, sport)
            loser_prob = 1 - winner_prob
            elos[winner] = elo(elos[winner], winner_exp, winner_prob, k=sensitivity)
            elos[loser] = elo(elos[loser], loser_exp, loser_prob, k=sensitivity)
        print(f"\r{(t + 1)/10}% done with elos         ", end="")
    return [(k, v) for k, v in dict(sorted(elos.items(), key=lambda item: item[1])).items()]

games = get_games("CBB", 2024)
save_to_csv(games, "CBB(3-9-24)GAMES")
elos = get_elos(games, 100, "CBB")
save_to_csv(elos, "CBB(3-9-24)ELOS")

# sport = "NFL"
#
# for season in range(2000, 2025):
#     print(season)
#     games = get_games(sport, season)
#     save_to_csv(games, f"{season}_{sport}_games")
#     print(f"\rgames saved to {season}_{sport}_games")
#     elos = get_elos(games, sport)
#     save_to_csv(elos, f"{season}_{sport}_elos")
#     print(f"\relos saved to {season}_{sport}_elos")