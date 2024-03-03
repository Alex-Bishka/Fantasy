from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def create_per_df(df, subset_cols, div_col, div_col_name):
    """"""
    for i, col in enumerate(subset_cols):
        # update df to have columns per X
        df[f"{col}_per_{div_col_name}"] = df[col] / df[div_col]

        # update subset columns
        subset_cols[i] = f"{col}_per_{div_col_name}"

    return df, subset_cols


def create_subset_df(df, subset_cols, drop_fantasy=True, len_subset_df=30):
    """"""
    assert("fantasy_points" in subset_cols[0])
    col_to_sort_by = subset_cols[0]
    
    # sort our cluster df by fantasy points (per something)
    subset_df = df[subset_cols].copy().dropna()
    subset_df = subset_df.sort_values(by=col_to_sort_by)[-len_subset_df:]

    # optionally drop the fantasy production part
    if drop_fantasy:
        subset_df.drop(columns=col_to_sort_by, inplace=True)
        subset_cols = subset_cols[1:]

    return subset_df, subset_cols


def create_cluster_vectors(df):
    """"""
    X = df.to_numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled


def get_candidate_cluster_size(X_scaled):
    """
    TODO: explore alternative for optimal candidate size
    """
    inertia = []
    for i in range(2, 11):  # consider clusters from 1 to 10
        kmeans = KMeans(n_clusters=i, algorithm='elkan', n_init=10).fit(X_scaled)
        inertia.append(kmeans.inertia_)

    plt.plot(range(2, 11), inertia)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

    return kmeans


def create_clusters(n, kmeans, X, X_scaled, df_review, subset_df, subset_cols):
    """"""
    kmeans = KMeans(n_clusters=n, random_state=0, n_init=10).fit(X_scaled)

    cluster_ranking = dict()
    for i, cluster_num in enumerate(kmeans.labels_):
        cluster_ranking[df_review.loc[subset_df.index[i], 'player_name']] = cluster_num

    labels = [str(label) for label in kmeans.labels_]

    df_cluster = pd.DataFrame(X, columns=subset_cols)
    df_cluster["Cluster"] = labels

    return df_cluster, cluster_ranking


import os
def check_save_path(save_path):
    """
    Checks to see if a file already exists, so we avoid over-writing it
    """
    exists = os.path.exists(save_path)
    if exists:
        raise(FileExistsError(f"File '{save_path}' already exists! Please choose a different name for the file."))
    

def create_cluster_plot(df_cluster, cluster_ranking, subset_cols,
                        save_path=None, font_size=12, marker_size=4, diagonal_is_visible=False,
                        width=1000, height=1000, showupperhalf=False, legend_size=14):
    # Convert dictionary keys to a list
    name_list = list(cluster_ranking.keys())

    # Add the list as a new column to the dataframe
    df_cluster['Names'] = name_list

    df_cluster.set_index('Names', inplace=True)

    fig = px.scatter_matrix(
        data_frame=df_cluster,
        dimensions=subset_cols,
        color="Cluster",
        hover_name=df_cluster.index,  # Assuming the player's name is the index
        labels={col: col for col in subset_cols}  # Optional if you want to customize axis labels
    )

    # Customize the appearance (optional)
    fig.update_traces(diagonal_visible=diagonal_is_visible, showupperhalf=showupperhalf)

    # improving UI
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',   # Transparent background outside the plot
        plot_bgcolor='rgba(245, 245, 245, 1)',  # Light gray plot background
        showlegend=True,
        font=dict(
            family="Courier New, monospace",  # Choose a font family
            size=font_size,  # Adjust the font size
            color="black"  # Font color
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(200, 200, 200, 0.5)')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(200, 200, 200, 0.5)')

    fig.update_layout(width=width, height=height)  # Adjust as necessary
    fig.update_traces(marker=dict(size=marker_size))  # Adjust marker size as needed

    fig.update_layout(legend=dict(font=dict(size=legend_size)))

    # Save the plot as HTML
    if save_path:
        check_save_path(save_path)
        fig.write_html(save_path)

    fig.show()