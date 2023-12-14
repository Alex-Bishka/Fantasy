import pandas as pd
import plotly.express as px


def create_correlation_matrix(df, x=[], y=[], all_vars=False):
    """
    Helper function to create the correlation matrix between the stats
    from the current and previous season.

    Can use the interesting stats or all of the stats to create the correlation
    matrix, by flipping the boolean 'all_vars'.

    The df passed in comes from the parsed and cleaned play by play, seasonal,
    and roster dfs from the nfl data package.
    """
    if (len(x) == 0) or (len(y) == 0):
        if all_vars:
            x = ['passing_yards', 'passing_attempts', 'yards_per_pass', 'total_epa',
                'passing_touchdowns', 'completions', 'games', 'age', 'fantasy_points']
            y = ['passing_yards_last', 'passing_attempts_last', 'yards_per_pass_last',
                'total_epa_last', 'passing_touchdowns_last', 'completions_last', 
                'games_last', 'age_last', 'fantasy_points_last'] 
        else:
            x = ['passing_yards', 'passing_attempts', 'total_epa', 'passing_touchdowns',
                'completions']
            y = ['passing_yards_last', 'passing_attempts_last', 'total_epa_last',
                'passing_touchdowns_last', 'completions_last']

    # Define current year and last year stats
    current_year_stats = df[x]
    last_year_stats = df[y]

    # Calculate pairwise correlations
    correlation_matrix = pd.DataFrame(index=last_year_stats.columns, columns=current_year_stats.columns)

    for current_col in current_year_stats.columns:
        for last_col in last_year_stats.columns:
            correlation = current_year_stats[current_col].corr(last_year_stats[last_col])
            correlation_matrix.at[last_col, current_col] = correlation

    correlation_matrix = correlation_matrix.astype(float)
    correlation_matrix = correlation_matrix.round(2)
    return correlation_matrix, x, y


def plot_correlation_matrix(corr_mat, x, y, title=""):
    """
    Helper function to create the heat map for the correlation matrix
    so that we can visualize it in a pretty way.
    """
    fig = px.imshow(corr_mat,
                    text_auto=True,
                    labels=dict(x="Current Season Stats", y="Previous Season Stats"),
                    x = x,
                    y = y,
                )

    if title:
        save_path = f"../../interactive/QB/stability-passing/{title}"
        save_path += ".html"
        fig.write_html(save_path)

    fig.show()