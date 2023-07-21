class Player_Career:
    def __init__(self, player_name, seasons=[]):
        """"""
        self.player_name = player_name
        self.seasons = seasons
        self.best_season = None
        self.career_stats = None
        self.season_average = None
        self.game_average = None

    def add_season(self, season):
        """"""
        self.seasons.append(season)

    def get_best_season(self, ppr=False):
        """"""
        best_season = None
        best_fantasy_points = 0
        for season in self.seasons:
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
        career_stats = self.seasons[0]
        career_stats.year = "Career"
        career_stats.rank = "N/A"
        if len(self.seasons) > 1:
            for season in self.seasons[1:]:
                career_stats.games += season.games or 0
                career_stats.games_started += season.games_started or 0
                career_stats.passing_completions += season.passing_completions or 0
                career_stats.passing_attempts += season.passing_attempts or 0
                career_stats.passing_yards += season.passing_yards or 0
                career_stats.passing_touchdowns += season.passing_touchdowns or 0
                career_stats.passing_interceptions += season.passing_interceptions or 0
                career_stats.rushing_attempts += season.rushing_attempts or 0
                career_stats.rushing_yards += season.rushing_yards or 0
                career_stats.rushing_touchdowns += season.rushing_touchdowns or 0
                career_stats.receiving_targets += season.receiving_targets or 0
                career_stats.receiving_receptions += season.receiving_receptions or 0
                career_stats.receiving_yards += season.receiving_yards or 0
                career_stats.receiving_td += season.receiving_td or 0
                career_stats.fumbles += season.fumbles or 0
                career_stats.fumbles_lost += season.fumbles_lost or 0
                career_stats.fantasy_points += season.fantasy_points or 0
                career_stats.fantasy_ppr += season.fantasy_ppr or 0
                career_stats.fantasy_vbd += season.fantasy_vbd or 0
        
        self.career_stats = career_stats
        return career_stats

    def get_average_season_stats(self):
        """"""
        self.season_average = self.career_stats
        num_seasons = len(self.seasons)

        self.season_average.games /= num_seasons
        self.season_average.games_started /= num_seasons
        self.season_average.passing_completions /= num_seasons
        self.season_average.passing_attempts /= num_seasons
        self.season_average.passing_yards /= num_seasons
        self.season_average.passing_touchdowns /= num_seasons
        self.season_average.passing_interceptions /= num_seasons
        self.season_average.rushing_attempts /= num_seasons
        self.season_average.rushing_yards /= num_seasons
        self.season_average.rushing_touchdowns /= num_seasons
        self.season_average.receiving_targets /= num_seasons
        self.season_average.receiving_receptions /= num_seasons
        self.season_average.receiving_yards /= num_seasons
        self.season_average.receiving_td /= num_seasons
        self.season_average.fumbles /= num_seasons
        self.season_average.fumbles_lost /= num_seasons
        self.season_average.fantasy_points /= num_seasons
        self.season_average.fantasy_ppr /= num_seasons
        self.season_average.fantasy_vbd /= num_seasons

        return self.season_average


    def get_average_per_game_stats(self):
        """"""
        self.game_average = self.career_stats
        num_games = self.career_stats.games

        self.game_average.games /= num_games
        self.game_average.games_started /= num_games
        self.game_average.passing_completions /= num_games
        self.game_average.passing_attempts /= num_games
        self.game_average.passing_yards /= num_games
        self.game_average.passing_touchdowns /= num_games
        self.game_average.passing_interceptions /= num_games
        self.game_average.rushing_attempts /= num_games
        self.game_average.rushing_yards /= num_games
        self.game_average.rushing_touchdowns /= num_games
        self.game_average.receiving_targets /= num_games
        self.game_average.receiving_receptions /= num_games
        self.game_average.receiving_yards /= num_games
        self.game_average.receiving_td /= num_games
        self.game_average.fumbles /= num_games
        self.game_average.fumbles_lost /= num_games
        self.game_average.fantasy_points /= num_games
        self.game_average.fantasy_ppr /= num_games
        self.game_average.fantasy_vbd /= num_games

        return self.game_average