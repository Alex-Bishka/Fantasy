class Player_Career:
    def __init__(self, player_name, seasons=[]):
        """"""
        self.player_name = player_name
        self.seasons = seasons
        self.best_season = None
        self.career_stats = None
        self.career_average = None

    def add_season(self, season):
        """"""
        self.seasons.append(season)

    def get_best_season(self, seasons, ppr=False):
        """"""
        best_season = None
        best_fantasy_points = 0
        for season in seasons:
            if ppr:
                season_fantasy_points = season.fantasy_points
            else:
                season_fantasy_points = season.fantasy_ppr
            
            if season_fantasy_points > best_fantasy_points:
                best_season = season
                best_fantasy_points = season_fantasy_points

        self.best_season = best_season
        return best_season

    def get_career_stats(self):
        """"""

    def get_average_stats(self):
        """"""