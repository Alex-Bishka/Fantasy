class Player_Season:
    def __init__(self, year, rank, player_name, position, age, games, games_started, passing_completions, passing_attempts, 
                 passing_yards, passing_touchdowns, passing_interceptions, rushing_attempts, rushing_yards, 
                 rushing_y_per_attempt, rushing_touchdowns, receiving_targets, receiving_receptions, receiving_yards, 
                 receiving_y_per_reception, receiving_td, fumbles, fumbles_lost, fantasy_points, fantasy_ppr, 
                 fantasy_vbd, fantasy_position_rank, fantasy_overall_rank, additional):
        """"""
        self.year = year
        self.rank = rank
        self.player_name = player_name
        self.position = position
        self.age = age
        self.games = games
        self.games_started = games_started
        self.passing_completions = passing_completions
        self.passing_attempts = passing_attempts
        self.passing_yards = passing_yards
        self.passing_touchdowns = passing_touchdowns
        self.passing_interceptions = passing_interceptions
        self.rushing_attempts = rushing_attempts
        self.rushing_yards = rushing_yards
        self.rushing_y_per_attempt = rushing_y_per_attempt
        self.rushing_touchdowns = rushing_touchdowns
        self.receiving_targets = receiving_targets
        self.receiving_receptions = receiving_receptions
        self.receiving_yards = receiving_yards
        self.receiving_y_per_reception = receiving_y_per_reception
        self.receiving_td = receiving_td
        self.fumbles = fumbles
        self.fumbles_lost = fumbles_lost
        self.fantasy_points = fantasy_points
        self.fantasy_ppr = fantasy_ppr
        self.fantasy_vbd = fantasy_vbd
        self.fantasy_position_rank = fantasy_position_rank
        self.fantasy_overall_rank = fantasy_overall_rank
        self.additional = additional


    def __repr__(self):
        """"""
        return f"\nPlayer Name: {self.player_name}\n" \
               f"Season: {self.year}\n" \
               f"Position: {self.position}\n" \
               f"Age: {self.age}\n" \
               f"Games: {self.games}\n" \
               f"Games Started: {self.games_started}\n" \
               f"Fantasy Points: {self.fantasy_points}\n" \
               f"Fantasy PPR: {self.fantasy_ppr}\n" \
               f"Fantasy VBD: {self.fantasy_vbd}\n" \
               f"Fantasy Position Rank: {self.fantasy_position_rank}\n" \
               f"Fantasy Overall Rank: {self.fantasy_overall_rank}\n"


    # TODO: double check this is valid
    def __lt__(self, other) -> bool:
        """"""
        # return self.fantasy_points < other.fantasy_points
        return self.fantasy_ppr < other.fantasy_ppr