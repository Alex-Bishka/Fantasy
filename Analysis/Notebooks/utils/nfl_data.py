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
        player_map: player_map_type,
        game_limit: int = 2
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
        # not all players have a seasonal df
        if "seasonal_df" in player and player["seasonal_df"]["games"] >= game_limit:
            if player["position"] == "QB":
                qbs.append(player)
            if player["position"] == "RB":
                rbs.append(player)
            if player["position"] == "WR":
                wrs.append(player)
            if player["position"] == "TE":
                tes.append(player)

    return qbs, rbs, wrs, tes


def create_positional_df(players) -> pd.DataFrame:
    """
    """
    list_of_seasonal_dicts = list()
    for player in players:
        list_of_seasonal_dicts.append(player["seasonal_df"])
    
    df = pd.DataFrame(list_of_seasonal_dicts)
    df = df.round(3)
    return df


def clean_df_for_csv(df, player_map):
    """"""
    df["name"] = df["player_id"].map(lambda x: player_map[x]['name'])
    df.drop(columns=["player_id", "Index", "season", "season_type"], inplace=True)
    
    df["total_epa"] = df["passing_epa"] + df["rushing_epa"]
    
    ignore_cols = ["name", "season", "season_type", "games", "target_share", "air_yards_share"
                  "tgt_sh", "ay_sh", "yac_sh", "ry_sh", "rtd_sh", "rfd_sh", "rtdfd_sh", "ppr_sh"]
    for col in df.columns.to_list():
        if col not in ignore_cols and "per game" not in col:
            df[f"{col} per game"] = df[col] / df["games"]
            
    df = df[['name'] + [col for col in df.columns if col != "name"]]
    return df