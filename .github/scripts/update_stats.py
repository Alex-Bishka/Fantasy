import sys
import os

# Add the directory containing nfl_data.py to the Python path
script_directory = os.path.dirname(__file__)
project_root = os.path.join(script_directory, '..', '..', 'Analysis', 'utils')
sys.path.append(project_root)

# Now we can import nfl_data
from nfl_data import (get_weekly_df, get_seasonal_df, get_roster_df, clean_df_for_csv,
                    create_mappings, create_position_groups, create_positional_df)
from datetime import datetime


def update_csvs() -> None:
    """"""
    def get_nfl_season() -> int:
        """"""
        # Get the current date and time
        now = datetime.now()

        # Extract the year and month
        current_year = now.year
        current_month = now.month

        if current_month == 1:
            current_year -= 1

        return current_year

    # getting nfl season
    current_year = get_nfl_season()
    years = [current_year]

    # grabbing seasonal and weekly data
    df_weekly = get_weekly_df(years=years, columns=[])
    df_seasonal = get_seasonal_df(years=years)

    # grabbing roster ids
    columns = ["player_name", "player_id", "position"]
    df_roster = get_roster_df(years=years, columns=columns)

    # creating player mappings from the roster, seasonal, and weekly dfs
    player_map, _ = create_mappings(df_roster=df_roster, df_seasonal=df_seasonal, df_weekly=df_weekly)

    # creating position groups and dfs for each
    qbs, rbs, wrs, tes = create_position_groups(player_map=player_map)
    df_qb = create_positional_df(qbs)
    df_rb = create_positional_df(rbs)
    df_wr = create_positional_df(wrs)
    df_te = create_positional_df(tes)

    # cleaning dfs for csv
    df_to_save_qb = clean_df_for_csv(df=df_qb, player_map=player_map)
    df_to_save_rb = clean_df_for_csv(df=df_rb, player_map=player_map)
    df_to_save_wr = clean_df_for_csv(df=df_wr, player_map=player_map)
    df_to_save_te = clean_df_for_csv(df=df_te, player_map=player_map)

    # saving dfs to csv
    df_to_save_qb.to_csv(f"FantasyData/advanced-stats/QB/{current_year}.csv")
    df_to_save_rb.to_csv(f"FantasyData/advanced-stats/RB/{current_year}.csv")
    df_to_save_wr.to_csv(f"FantasyData/advanced-stats/WR/{current_year}.csv")
    df_to_save_te.to_csv(f"FantasyData/advanced-stats/TE/{current_year}.csv")
