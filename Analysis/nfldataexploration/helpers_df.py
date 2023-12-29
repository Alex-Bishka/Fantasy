import pandas as pd
from sklearn.model_selection import train_test_split

def create_lag_df(df, cols_to_filter=3, col_to_increment="season", 
                  cols_to_merge=["player_id", "season", "season_type"]
    ):
    """"""
    df_now = df.copy()
    df_last = df.copy()

    rename_dict = {}
    for col in list(df_last.columns[cols_to_filter:]):
        rename_dict[col] = f"{col}_last"

    df_last.rename(columns=rename_dict, inplace=True)
    df_last[col_to_increment] += 1

    df_lag = df_now.merge(df_last, how='inner', on=cols_to_merge)

    return df_lag


def create_train_and_test_sets(df, x_cols, test_size=0.2, inference_col="fantasy_points", verbose=True):
    """"""
    X = df[x_cols]
    y = df[inference_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

    len_dataset = len(df)
    len_train = len(X_train)
    len_test = len(X_test)
    
    if verbose:
        print("```")
        print(f"Length of train set: {len_train}")
        print(f"Length of test set: {len_test}")
        print(f"Length of data set: {len_dataset}")
        print("```")
    
    return X_train, X_test, y_train, y_test


def normalize_stats(df, stats_to_normalize):
    """"""
    for stat in stats_to_normalize:
        new_col = f"{stat}_normalized"
        df[new_col] = df[stat] / df[stat].max()

    return df