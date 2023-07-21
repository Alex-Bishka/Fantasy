import csv, re
from player_season import Player_Season
from player_career import Player_Career

def generate_season_from_csv(csv_file_path, by_position=False, by_player=False):
    """"""
    pattern = r'./FantasyData/(\d{4}).csv'
    match = re.search(pattern, csv_file_path)
    if match:
        year = match.group(1)
    else:
        raise ValueError("\nYear in filename is invalid!\n")

    players_by_position = {}
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = re.sub('[+*]', '', row['Player Name'])
            player = Player_Season(
                year=year,
                rank=int(row['Rank']),
                player_name=name,
                position=row['Position'],
                age=int(row['Age']),
                games=int(row['Games']),
                games_started=int(row['Games Started']),
                passing_completions=int(row['Passing Completions']) if row['Passing Completions'] else 0,
                passing_attempts=int(row['Passing Attempts']) if row['Passing Attempts'] else 0,
                passing_yards=int(row['Passing Yards']) if row['Passing Yards'] else 0,
                passing_touchdowns=int(row['Passing Touchdowns']) if row['Passing Touchdowns'] else 0,
                passing_interceptions=int(row['Passing Interceptions']) if row['Passing Interceptions'] else 0,
                rushing_attempts=int(row['Rushing Attempts']) if row['Rushing Attempts'] else 0,
                rushing_yards=int(row['Rushing Yards']) if row['Rushing Yards'] else 0,
                rushing_y_per_attempt=float(row['Rushing Y/A']) if row['Rushing Y/A'] else 0,
                rushing_touchdowns=int(row['Rushing Touchdowns']) if row['Rushing Touchdowns'] else 0,
                receiving_targets=int(row['Receiving Targets']) if row['Receiving Targets'] else 0,
                receiving_receptions=int(row['Receiving Receptions']) if row['Receiving Receptions'] else 0,
                receiving_yards=int(row['Receiving Yards']) if row['Receiving Yards'] else 0,
                receiving_y_per_reception=float(row['Receiving Y/R']) if row['Receiving Y/R'] else 0,
                receiving_td=int(row['Receiving TD']) if row['Receiving TD'] else 0,
                fumbles=int(row['Fumbles']) if row['Fumbles'] else 0,
                fumbles_lost=int(row['Fumbles Lost']) if row['Fumbles Lost'] else 0,
                fantasy_points=float(row['Fantasy Points']) if row['Fantasy Points'] else 0,
                fantasy_ppr=float(row['Fantasy PPR']) if row['Fantasy PPR'] else 0,
                fantasy_vbd=int(row['Fantasy VBD']) if row['Fantasy VBD'] else 0,
                fantasy_position_rank=int(row['Fantasy Position Rank']) if row['Fantasy Position Rank'] else 0,
                fantasy_overall_rank=int(row['Fantasy Overall Rank']) if row['Fantasy Overall Rank'] else 0,
                additional=row['additional']
            )
            
            # Add the player to the appropriate list based on their position
            if by_position:
                if player.position in players_by_position:
                    players_by_position[player.position].append(player)
                elif len(player.position.strip()) > 0:
                    players_by_position[player.position] = [player]
            elif by_player:
                if player.position in players_by_position:
                    players_by_position[player.player_name].append(player)
                elif len(player.position.strip()) > 0:
                    players_by_position[player.player_name] = [player]
                  
    return players_by_position


data_path = "./FantasyData"
years = ['2010',
 '2011',
 '2012',
 '2013',
 '2014',
 '2015',
 '2016',
 '2017',
 '2018',
 '2019',
 '2020',
 '2021',
 '2022']

# grabbing all data - by player
def grab_data(by_position, by_player):
    """"""
    seasons_data = []
    for year in years:
        season = generate_season_from_csv(f"{data_path}/{year}.csv", by_position=by_position, by_player=by_player)
        season_data = (year, season)
        seasons_data.append(season_data)

    return seasons_data


def construct_career(player_name, seasons):
    """"""
    player_career = Player_Career(player_name, [])
    for _, season in seasons:
        if player_name in season:
            player_career.add_season(season[player_name][0])

    return player_career
