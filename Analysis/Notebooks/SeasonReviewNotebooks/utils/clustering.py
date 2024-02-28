from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from models.player_season import Player_Season
from typing import List


def get_stats_array(player: Player_Season, stats: List[str]) -> List[float]:
    """"""
    player_data = list()
    for stat in stats:
        # total stats (non-qb)
        if stat == "Total Yards":
            player_data.append(float(player.receiving_yards + player.rushing_yards))
        elif stat == "Yards Per Game":
            player_data.append(float((player.receiving_yards + player.rushing_yards) / player.games))
        elif stat == "Total TDs":
            player_data.append(float(player.receiving_td + player.rushing_touchdowns))
        elif stat == "TDs Per Game":
            player_data.append(float((player.receiving_td + player.rushing_touchdowns) / player.games))

        # receiving stats
        elif stat == "Receiving Yards":
            player_data.append(float(player.receiving_yards))
        elif stat == "Receiving Yards Per Game":
            player_data.append(float(player.receiving_yards / player.games))
        elif stat == "Receptions":
            player_data.append(float(player.receiving_receptions))
        elif stat == "Receptions Per Game":
            player_data.append(float(player.receiving_receptions / player.games))
        elif stat == "Receiving TDs":
            player_data.append(float(player.receiving_td))
        elif stat == "Receiving TDs Per Game":
            player_data.append(float(player.receiving_td / player.games))
        elif stat == "Targets":
            player_data.append(float(player.receiving_targets))
        elif stat == "Targets Per Game":
            player_data.append(float(player.receiving_targets / player.games))
        
        # rushing stats
        elif stat == "Rushing Yards":
            player_data.append(float(player.rushing_yards))
        elif stat == "Rushing Yards Per Game":
            player_data.append(float(player.rushing_yards / player.games))
        elif stat == "Carries":
            player_data.append(float(player.rushing_attempts))
        elif stat == "Carries Per Game":
            player_data.append(float(player.rushing_attempts / player.games))
        elif stat == "Yards Per Carry":
            player_data.append(float(player.rushing_y_per_attempt))
        elif stat == "Rushing Touchdowns":
            player_data.append(float(player.rushing_touchdowns))
        elif stat == "Rushing Touchdowns Per Game":
            player_data.append(float(player.rushing_touchdowns / player.games))
        elif stat == "Fumbles":
            player_data.append(float(player.fumbles))
        elif stat == "Fumbles Per Game":
            player_data.append(float(player.fumbles / player.games))

        # passing stats
        elif stat == "Interceptions":
            player_data.append(float(player.passing_interceptions))
        elif stat == "Interceptions Per Game":
            player_data.append(float(player.passing_interceptions / player.games))
        elif stat == "Passing TDs":
            player_data.append(float(player.passing_touchdowns))
        elif stat == "Passing TDs Per Game":
            player_data.append(float(player.passing_touchdowns / player.games))
        elif stat == "Passing Yards":
            player_data.append(float(player.passing_yards))
        elif stat == "Passing Yards Per Game":
            player_data.append(float(player.passing_yards / player.games))
        elif stat == "Attempts":
            player_data.append(float(player.passing_attempts))
        elif stat == "Attempts Per Game":
            player_data.append(float(player.passing_attempts / player.games))
        elif stat == "Completions":
            player_data.append(float(player.passing_completions))
        elif stat == "Completions Per Game":
            player_data.append(float(player.passing_completions / player.games))

        # error
        else:
            raise ValueError(f"Passed in stat - '{stat}' - is not available for stat array creation!")
    return player_data



def create_cluster_data(players, stats):
    """"""
    data = list()
    for player in players:
        player_data = get_stats_array(player=player, stats=stats)
        data.append(player_data)

    X = np.array(data)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled


def create_vectors_advanced(subset_df):
    """"""
    X = subset_df.to_numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled


def get_candidate_cluster_n_values(X_scaled):
    """"""
    # Elbow method
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


def create_clusters(cluster_num, X_scaled, players):
    """"""
    kmeans = KMeans(n_clusters=cluster_num, random_state=0, n_init=10).fit(X_scaled)
    kmeans.labels_

    cluster_ranking = dict()
    for player, cluster_num in zip(players, kmeans.labels_):
        cluster_ranking[player.player_name] = cluster_num

    return [str(label) for label in kmeans.labels_], cluster_ranking


def create_clusters_advanced(cluster_num, X_scaled, df):
    """"""
    kmeans = KMeans(n_clusters=cluster_num, random_state=0, n_init=10).fit(X_scaled)
    kmeans.labels_

    cluster_ranking = dict()
    for i, cluster_num in enumerate(kmeans.labels_):
        cluster_ranking[df.loc[df.index[i], 'name']] = cluster_num

    return [str(label) for label in kmeans.labels_], cluster_ranking


def create_cluster_df(labels, X, stats):
    """"""
    df = pd.DataFrame(X, columns=stats)
    df["Cluster"] = labels

    return df


def graph_pair_plot(df, stats, position, palette="bright", save_fig=True, save_suffix=""):
    """"""
    cluster_size = df["Cluster"].nunique()
    sns.pairplot(df, hue='Cluster', palette=palette, vars=stats)
    
    # save the image
    if save_fig:
        save_path = f"./images/{position}/clustering-{cluster_size}"

        if save_suffix:
            save_path += f"-{save_suffix}"

        save_path += ".png"
        plt.savefig(save_path, format="png")

    plt.show()


import plotly.graph_objs as go

def add_subplot_border(fig, positions, color='red', width=3):
    # Calculate the domain of the subplot to add a border
    # The positions are the fractions (0-1) of the subplot's location on the canvas
    x0, x1, y0, y1 = positions
    
    # Add shapes to create the border effect
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line=dict(
            color=color,
            width=width
        ),
        layer="above"
    )


import plotly.express as px
def graph_pair_plot_plotly(df: pd.DataFrame, cluster_rankings, stats,
        position, save_fig: bool = True, save_suffix: str = "",
        font_size: int = 12, marker_size: int = 4, diagonal_is_visible: bool = False,
        width: int = 700, height: int = 700, showupperhalf: bool = False, legend_size: int = 14
    ):
    """
    Create a pair plot using Plotly
    """
    # Convert dictionary keys to a list
    name_list = list(cluster_rankings.keys())

    # Add the list as a new column to the dataframe
    df['Names'] = name_list

    df.set_index('Names', inplace=True)

    fig = px.scatter_matrix(
        data_frame=df,
        dimensions=stats,
        color="Cluster",
        hover_name=df.index,  # Assuming the player's name is the index
        labels={col: col for col in stats}  # Optional if you want to customize axis labels
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
    # highligh a subplot by giving it a border
    # col = 2
    # row = 1
    # num_plots_per_side = 5
    # step = 1.0 / num_plots_per_side
    # x0 = (col - 1) * step
    # x1 = col * step
    # y0 = 1 - row * step
    # y1 = 1 - (row - 1) * step
    # positions = (x0, x1, y0, y1)
    # add_subplot_border(fig, positions)
    # highlight_subplot_background(fig, rows=[1], cols=[1, 2, 3], color='rgba(255, 235, 238, 1)')  # A light red background color

    # Save the plot as HTML
    if save_fig:
        save_path = f"./interactive/{position}/clustering-{len(df['Cluster'].unique())}"

        if save_suffix:
            save_path += f"-{save_suffix}"

        save_path += ".html"
        fig.write_html(save_path)

    fig.show()

