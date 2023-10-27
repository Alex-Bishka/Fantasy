import nfl_data_py as nfl
import pandas as pd
from typing import List, Dict, Union, Optional

# the typing for the player map object
player_map_type = Dict[str, 
            Union[
                str,
                Dict[str, Union[int, float, str]], 
                List[Dict[str, Union[int, float, str, Optional[float]]]]
            ]
        ]

# the typing for the id map object
id_map_type = Dict[str, str]

def get_weekly_df(years: List[int], columns: List[str]) -> pd.DataFrame:
    """"""
    df_weekly = nfl.import_weekly_data(years, columns, downcast=True)
    return df_weekly

def get_seasonal_df(years: List[int], s_type: str = "REG") -> pd.DataFrame:
    """"""
    df_seasonal = nfl.import_seasonal_data(years, s_type)
    return df_seasonal


def get_roster_df(
        years: List[int],
        columns: List[str] = ["player_name", "player_id", "position"]
    ) -> pd.DataFrame:
    """"""
    df_roster = nfl.import_seasonal_rosters(years, columns)
    return df_roster


def create_mappings(
        df_roster: pd.DataFrame,
        df_seasonal: pd.DataFrame,
        df_weekly: pd.DataFrame
    ) -> Union[
        player_map_type,
        id_map_type
    ]:
    """"""
    player_map = dict()
    id_map = dict()

    for row in df_roster.itertuples():
        player_map[row.player_id] = dict()
        player_map[row.player_id]["name"] = row.player_name
        player_map[row.player_id]["position"] = row.position
        
        id_map[row.player_name] = row.player_id

    for row in df_seasonal.itertuples():
        if row.player_id in player_map:
            player_map[row.player_id]["seasonal_df"] = row._asdict()

    # each row represents the performance of that player for the week
    for row in df_weekly.itertuples():
        if row.player_display_name in id_map:
            player_id = id_map[row.player_display_name]
            if "week_dfs" in player_map[player_id]:
                player_map[player_id]["week_dfs"].append(row._asdict())
            else:
                player_map[player_id]["week_dfs"] = [row._asdict()]

    return player_map, id_map


def create_position_groups(
        player_map: player_map_type
    ) -> Union[
        List[player_map_type],
        List[player_map_type],
        List[player_map_type],
        List[player_map_type]
    ]:
    """"""
    qbs = list()
    rbs = list()
    wrs = list()
    tes = list()

    for key in player_map:
        player = player_map[key]
        if "seasonal_df" in player:  # not all players have a seasonal df
            if player["position"] == "QB":
                qbs.append(player)
            if player["position"] == "RB":
                rbs.append(player)
            if player["position"] == "WR":
                wrs.append(player)
            if player["position"] == "TE":
                tes.append(player)

    return qbs, rbs, wrs, tes


def create_positional_df(columns: List[str], players):
    """
    TODO: complete custimization for this function
    """
    df_pos = pd.DataFrame(columns=columns)
    for player in players:
        pass