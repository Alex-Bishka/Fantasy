from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from models.player_season import Player_Season


def get_stats_array(player: Player_Season, stats):
    """"""
    player_data = list()
    for stat in stats:
        # total stats (non-qb)
        if stat == "Total Yards":
            player_data.append(float(player.receiving_yards + player.rushing_yards))
        if stat == "Yards Per Game":
            player_data.append(float((player.receiving_yards + player.rushing_yards) / player.games))
        if stat == "Total TDs":
            player_data.append(float(player.receiving_td + player.rushing_touchdowns))
        if stat == "TDs Per Game":
            player_data.append(float((player.receiving_td + player.rushing_touchdowns) / player.games))

        # receiving stats
        if stat == "Receiving Yards":
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
        elif stat == "Passing Interceptions":
            player_data.append(float(player.passing_interceptions))
        elif stat == "Passing Inteceptions Per Game":
            player_data.append(float(player.passing_interceptions / player.games))
        elif stat == "Passing Touchdowns":
            player_data.append(float(player.passing_touchdowns))
        elif stat == "Passing Touchdowns Per Game":
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


import plotly.express as px
def graph_pair_plot_plotly(df, cluster_rankings, stats,
        position, save_fig=True, save_suffix="",
        font_size=12, marker_size=4, diagonal_is_visible=False,
        width=700, height=700
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
        df,
        dimensions=stats,
        color="Cluster",
        hover_name=df.index,  # Assuming the player's name is the index
        labels={col: col for col in stats}  # Optional if you want to customize axis labels
    )
    
    # Customize the appearance (optional)
    fig.update_traces(diagonal_visible=diagonal_is_visible)

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

    # Save the plot as HTML
    if save_fig:
        save_path = f"./interactive/{position}/clustering-{len(df['Cluster'].unique())}"

        if save_suffix:
            save_path += f"-{save_suffix}"

        save_path += ".html"
        fig.write_html(save_path)

    fig.show()

