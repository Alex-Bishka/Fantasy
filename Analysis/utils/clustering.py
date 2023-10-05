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
        kmeans = KMeans(n_clusters=i, algorithm='elkan').fit(X_scaled)
        inertia.append(kmeans.inertia_)

    plt.plot(range(2, 11), inertia)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show()

    return kmeans


def create_clusters(cluster_num, X_scaled, players):
    """"""
    kmeans = KMeans(n_clusters=cluster_num, random_state=0).fit(X_scaled)
    kmeans.labels_

    cluster_ranking = dict()
    for player, cluster_num in zip(players, kmeans.labels_):
        cluster_ranking[player.player_name] = cluster_num

    return kmeans.labels_, cluster_ranking


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