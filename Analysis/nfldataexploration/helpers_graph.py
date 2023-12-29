import pandas as pd
import plotly.express as px


def filter_df(df, query, x, y, base_path="", title="temp"):
    # create filtered df
    df_filter = df.copy()    
    if query:
        df_filter = df_filter.query(query)
    
    # create and show corr_mat
    corr_mat, x, y = create_correlation_matrix(df_filter, x, y)  
    
    if title == "temp" or len(title) == 0 or len(base_path) == 0:
        plot_correlation_matrix(corr_mat, x, y)
    else:
        plot_correlation_matrix(corr_mat, x, y, path=f"{base_path}/{title}")
    
    # visualize highest correlation pairing
    series = corr_mat.max().iloc[0:]
    temp_arr = list(series)
    
    max_series_value = series.max()
    i = temp_arr.index(max_series_value)
    col = list(corr_mat.columns)[i]
    print(col)
    col_prev = f"{col}_last"
    
    fig = px.scatter(df_filter, x=col_prev, y=col,
                 hover_data=["rusher", "season", "age"]
                )
    if title and title != "temp" and base_path:
        fig_name = f"{title}-scatter-{col}"
        path = f"{base_path}/{fig_name}.html"
        print(f"\nSave path: {fig_name}\n")
        fig.write_html(path)
    fig.show()
    
    return df_filter

def create_correlation_matrix(df, x, y):
    """
    Helper function to create the correlation matrix between the stats
    from the current and previous season.

    The df passed in comes from the parsed and cleaned play by play, seasonal,
    and roster dfs from the nfl data package.
    """
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


def plot_correlation_matrix(corr_mat, x, y, path="", title=""):
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

    # Update layout
    if title:
        fig.update_layout(
            title=title,
        )

    if path:
        fig.write_html(f"{path}.html")

    fig.show()