from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import SilhouetteVisualizer
from .utils import check_save_path
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


def create_subset_df(df, subset_cols, drop_fantasy=True, len_subset_df=30, div_col=None, div_col_name=None):
    """"""
    if div_col and div_col_name:
        df, subset_cols = create_per_df(df.copy(), subset_cols, div_col, div_col_name)

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


def get_candidate_cluster_size_elbow_method(X_scaled):
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


def get_candidate_cluster_size_silhouette_method(X_scaled):
    """"""
    _, ax = plt.subplots(3, 2, figsize=(15,8))
    for i in range(2, 8):
        '''
        Create KMeans instances for different number of clusters
        '''
        km = KMeans(n_clusters=i, init='k-means++', n_init=10, random_state=0)
        q, mod = divmod(i, 2)
        '''
        Create SilhouetteVisualizer instance with KMeans instance
        Fit the visualizer
        '''

        visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
        visualizer.fit(X_scaled) 

    return km


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


def create_cluster_plot(df_cluster, cluster_ranking, subset_cols,
                        save_path=None, font_size=12, marker_size=4, diagonal_is_visible=False,
                        width=1000, height=1000, showupperhalf=False, legend_size=14):
    # Convert dictionary keys to a list
    name_list = list(cluster_ranking.keys())

    # Add the list as a new column to the dataframe
    df_cluster['Names'] = name_list

    df_cluster.set_index('Names', inplace=True)

    df_cluster.sort_values(by="Cluster", inplace=True)

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


num_2_word = {
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven"
}
legend_color_dict = {
    0: "Dark Blue",
    1: "Red",
    2: "Green",
    3: "Purple",
    4: "Orange",
    5: "Teal",
    6: "Pink"
}
STARTING_INDENT = 3


def indent(num_indents):
    return "\t" * num_indents


def html_breaking_down_clusters(keys):
    """"""
    print(f"{indent(STARTING_INDENT)}<div>")
    
    print(f"{indent(STARTING_INDENT + 1)}<p class='blog-p-tag'>")
    print(f"{indent(STARTING_INDENT + 2)}TODO")
    print(f"{indent(STARTING_INDENT + 1)}</p>")
    print(f"{indent(STARTING_INDENT + 1)}<div class='iframe-container'>")
    print(f"{indent(STARTING_INDENT + 2)}<iframe class='large-iframe' data-src='TODO'></iframe>")
    print(f"{indent(STARTING_INDENT + 1)}</div>")
    
    print(f"{indent(STARTING_INDENT + 1)}<p class='blog-p-tag'>")
    print(f"{indent(STARTING_INDENT + 2)}TODO:")
    print(f"{indent(STARTING_INDENT + 1)}</p>")
    print(f"{indent(STARTING_INDENT + 1)}<ul class='bullet-list'>")
    for key in keys:
        print(f"{indent(STARTING_INDENT + 2)}<li><b>Cluster {key} ({legend_color_dict[int(key)]}):</b> TODO</li>")
        
    print(f"{indent(STARTING_INDENT + 1)}</ul>")


def create_cluster_html_tiers(df: pd.DataFrame) -> None:
    cluster_dict = dict()
    for index, row in df.iterrows():
        if row.Cluster not in cluster_dict:
            cluster_dict[row.Cluster] = [index]
        else:
            cluster_dict[row.Cluster].append(index)
            
    sorted_cluster_dict = dict(sorted(cluster_dict.items()))
    keys = list(sorted_cluster_dict.keys())
    
    
    html_breaking_down_clusters(keys)
    print(f"{indent(STARTING_INDENT + 1)}<div style='display: flex; justify-content: space-evenly;''>")
    for key in keys:
        names = cluster_dict[key]
        
        print(f"{indent(STARTING_INDENT + 2)}<div>")
        print(f"{indent(STARTING_INDENT + 3)}<b>Cluster {key} ({legend_color_dict[int(key)]})</b>")
        print(f"{indent(STARTING_INDENT + 3)}<ul class='bullet-list'>")
        for name in names:
            print(f"{indent(STARTING_INDENT + 4)}<li>{name}</li>")
        print(f"{indent(STARTING_INDENT + 3)}</ul>")
        print(f"{indent(STARTING_INDENT + 2)}</div>")
        if key != keys[-1]:
            print()
    print(f"{indent(STARTING_INDENT + 1)}</div>")
    print(f"""{indent(STARTING_INDENT + 1)}<p class="blog-p-tag">
    {indent(STARTING_INDENT + 2)}TODO
    {indent(STARTING_INDENT + 1)}</p>""")
    print(f"{indent(STARTING_INDENT + 1)}<ul class='bullet-list'>")
    for key in keys:
        print(f"{indent(STARTING_INDENT + 2)}<li><b>Cluster {key} ({legend_color_dict[int(key)]}):</b> TODO</li>")
    print(f"{indent(STARTING_INDENT + 1)}</ul>")
    print(f"{indent(STARTING_INDENT)}</div>")
