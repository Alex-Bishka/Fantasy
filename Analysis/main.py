from utils import grab_data, construct_career

def top_players_by_position(position: str = "QB", top_n: int = 12) -> None:
    """
    Grabbing the top_n players from a position
    """
    seasons = grab_data(by_position=True, by_player=False)
    season_2022 = seasons[-1]

    year = season_2022[0]
    season_data = season_2022[1]
    players = season_data[position]
    
    return players[:top_n]

if True:
    top_qbs_22 = top_players_by_position(position="QB", top_n=12)
    print(top_qbs_22)


def get_by_position_example():
    """
    An example of how to grab data from each season by player position.

    The last season in seasons is 2022, and the first is 2010. Each item in the seasons list
    is composed of a tuple in the form of (year, season_data). 
    
    season_data is a dictionary of string keys to string lists. The keys are the positions in
    Fantasy: 'QB', 'RB', 'WR', 'TE'.

    Grabbing a value would return a list of players, for example season_data["QB"] would return
    the list of QBs with fantasy points during that season.

    Each element in the list of players is represented by the player_season class.

    This type of data gathering would be useful to see trends by position over years gone by.
    """
    seasons = grab_data(by_position=True, by_player=False)
    season_2022 = seasons[-1]

    year = season_2022[0]
    season_data = season_2022[1]
    qbs = season_data["QB"]
    qb = qbs[0]

    print()
    print(f"\nyear: {year}  |  keys: {season_data.keys()}")
    print(f"\nExample player:\n{qb}")
    print()

# example of getting data by position
if False:
    get_by_position_example()

def get_by_player_example():
    """"""
    seasons = grab_data(by_position=False, by_player=True)

    season_2022 = seasons[-1]
    year = season_2022[0]
    season_data = season_2022[1]

    print(f"\nyear: {year}\n")
    print(season_data["Patrick Mahomes"])
    print([key for key in season_data.keys() if "Mahomes" in key])

    # creates player career by storing all seasons in class
    player_career = construct_career("Patrick Mahomes", seasons)
    
    # finds the best season (by fantasy pts) of a player's career
    best_season = player_career.get_best_season()
    print()
    print(best_season)
    print()

    career_stats = player_career.get_career_stats()
    print()
    print(career_stats)
    print()

    # TODO: test the following - and adjust weird stats
    season_averages = player_career.get_average_season_stats()
    print()
    print(season_averages)
    print()
    
    game_averages = player_career.get_average_per_game_stats()
    print()
    print(game_averages)
    print()


if False:
    get_by_player_example()