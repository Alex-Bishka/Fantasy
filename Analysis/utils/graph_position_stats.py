import matplotlib.pyplot as plt
from typing import List, Tuple, Union
from models.player_season import Player_Season

# constants for text positioning on vertical and horizontal lines
FACTOR_ABOVE_HORIZONTAL = 0.008173076923076924
FACTOR_LEFT_VERTICAL = 0.015625

# graph constants
FIGSIZE = (12, 8)
ROTATION = 45
MARKERSIZE = 12
SCATTER_MARKERSIZE = 24

# title constants
X_AXIS_LABEL = "Players"


def grab_top_n_players(position_group: List[Player_Season], show_tier_2: bool = False,
                       show_tier_3: bool = False) -> List[str] and List[str] and List[str]:
    """"""
    # init potential tiers
    highlight_names_tier_1 = list()
    highlight_names_tier_2 = list()
    highlight_names_tier_3 = list()

    # grabbing names of all players in position group
    names = [p.player_name for p in position_group]

    # setting each name per tier
    highlight_names_tier_1 = names[-12:]
    if show_tier_2:
        highlight_names_tier_2 = names[-24:-12]
    if show_tier_3:
        highlight_names_tier_3 = names[-36:-12]

    return highlight_names_tier_1, highlight_names_tier_2, highlight_names_tier_3


def get_possible_stat_options() -> None:
    stat_options = [
        "Total Fantasy Points",
        "Games Played",
        "Games Started",
        "Fantasy Points Per Game",
        "Total Passing Yards",
        "Passing Yards Per Game",
        "Total Passing Completions",
        "Passing Completions Per Game",
        "Total Passing Attempts",
        "Passing Attempts Per Game",
        "Total Passing Touchdowns",
        "Passing Touchdowns Per Game",
        "Total Passing Interceptions",
        "Total Rushing Attempts",
        "Carries Per Game",
        "Total Rushing Yards",
        "Rushing Yards Per Game",
        "Yards Per Carry",
        "Total Rushing Touchdowns",
        "Total Receiving Targets",
        "Targets Per Game",
        "Total Receiving Receptions",
        "Receptions Per Game",
        "Total Receiving Yards",
        "Receiving Yards Per Game",
        "Yards Per Catch",
        "Total Receiving Touchdowns",
        "Fumbles",
        "Fumbles Lost",
        "Fantasy PPR",
        "Fantasy VBD",
        "Fantasy Position Rank",
        "Fantasy Overall Rank",
        "Age"
    ]

    print("Options for stat to graph:")
    for option in stat_options:
        print(f"\t{option}")


def set_data(position_group: List[Player_Season], stat_to_show: str) -> List[Tuple[Union[float, str], str]]:
    """"""
    if stat_to_show == "Total Fantasy Points":
        data = [(p.fantasy_points, p.player_name) for p in position_group]
    elif stat_to_show == "Games Played":
        data = [(p.games) for p in position_group]
    elif stat_to_show == "Games Started":
        data = [(p.games_started) for p in position_group]
    elif stat_to_show == "Fantasy Points Per Game":
        data = [(p.fantasy_points / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Passing Yards":
        data = [(p.passing_yards, p.player_name) for p in position_group]
    elif stat_to_show == "Passing Yards Per Game":
        data = [(p.passing_yards / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Passing Completions":
        data = [(p.passing_completions, p.player_name) for p in position_group]
    elif stat_to_show == "Passing Completions Per Game":
        data = [(p.passing_completions / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Passing Attempts":
        data = [(p.passing_attempts, p.player_name) for p in position_group]
    elif stat_to_show == "Passing Attempts Per Game":
        data = [(p.passing_attempts / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Passing Touchdowns":
        data = [(p.passing_touchdowns, p.player_name) for p in position_group]
    elif stat_to_show == "Passing Touchdowns Per Game":
        data = [(p.passing_touchdowns / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Passing Interceptions":
        data = [(p.passing_interceptions, p.player_name) for p in position_group]
    elif stat_to_show == "Total Rushing Attempts":
        data = [(p.rushing_attempts, p.player_name) for p in position_group]
    elif stat_to_show == "Carries Per Game":
        data = [(p.rushing_attempts / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Rushing Yards":
        data = [(p.rushing_yards, p.player_name) for p in position_group]
    elif stat_to_show == "Rushing Yards Per Game":
        data = [(p.rushing_yards / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Yards Per Carry":
        data = [(p.rushing_y_per_attempt, p.player_name) for p in position_group]
    elif stat_to_show == "Total Rushing Touchdowns":
        data = [(p.rushing_touchdowns, p.player_name) for p in position_group]
    elif stat_to_show == "Total Receiving Targets":
        data = [(p.receiving_targets, p.player_name) for p in position_group]
    elif stat_to_show == "Targets Per Game":
        data = [(p.receiving_targets / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Receiving Receptions":
        data = [(p.receiving_receptions, p.player_name) for p in position_group]
    elif stat_to_show == "Receptions Per Game":
        data = [(p.receiving_receptions / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Total Receiving Yards":
        data = [(p.receiving_yards, p.player_name) for p in position_group]
    elif stat_to_show == "Receiving Yards Per Game":
        data = [(p.receiving_yards / p.games, p.player_name) for p in position_group]
    elif stat_to_show == "Yards Per Catch":
        data = [(p.receiving_y_per_reception, p.player_name) for p in position_group]
    elif stat_to_show == "Total Receiving Touchdowns":
        data = [(p.receiving_td, p.player_name) for p in position_group]
    elif stat_to_show == "Fumbles":
        data = [(p.fumbles, p.player_name) for p in position_group]
    elif stat_to_show == "Fumbles Lost":
        data = [(p.fumbles_lost, p.player_name) for p in position_group]
    elif stat_to_show == "Fantasy PPR":
        data = [(p.fantasy_ppr, p.player_name) for p in position_group]
    elif stat_to_show == "Fantasy VBD":
        data = [(p.fantasy_vbd, p.player_name) for p in position_group]
    elif stat_to_show == "Fantasy Position Rank":
        data = [(p.fantasy_position_rank, p.player_name) for p in position_group]
    elif stat_to_show == "Fantasy Overall Rank":
        data = [(p.fantasy_overall_rank, p.player_name) for p in position_group]
    elif stat_to_show == "Age":
        data = [(p.age, p.player_name) for p in position_group]
    else:
        raise ValueError("Incorrect stat to show passed through!")

    return data


def graph_stat_by_stat(position_group: List[Player_Season], primary_stat: str, secondary_stat: str, 
        names: List[str] = [], vertical_name_pos: int = 0, horizontal_name_pos: int = -0.5,
        break_one: int = None, break_two: int = None, break_three: int = None, top_n: int = 0,
        show_tier_1: bool = False, show_tier_2: bool = False, show_tier_3: bool = False,
        save_fig: bool = True, save_suffix: str = ""
    ) -> None:
    """
    TODO: incorporate top n value
    TODO: lines need differnt philosophy on this
    """
    position = position_group[0].position
    year = position_group[0].year
    
    # grabing y-axis data
    primary_data = set_data(position_group=position_group, stat_to_show=primary_stat) 
    y_axis_label = primary_stat

    # grabbing x-axis data
    secondary_data = set_data(position_group=position_group, stat_to_show=secondary_stat)
    x_axis_label = secondary_stat

    # construct alignment
    graph_data = []
    for (y_axis_stat, name), (x_axis_stat, _) in zip(primary_data, secondary_data):
        graph_data.append((x_axis_stat, y_axis_stat, name))

    graph_data.sort()
    
    # graphing stat and second stat
    y_axis_data = [y_axis_stat for _, y_axis_stat, _ in graph_data]
    x_axis_data = [x_axis_stat for x_axis_stat, _, _ in graph_data]
    labels = [name for _, _, name in graph_data]

    # creating graph
    plt.figure(figsize=FIGSIZE) # Increase figure size

    # grab tier lists for highlighitng
    if show_tier_1:
        tier_1_list, tier_2_list, tier_3_list = grab_top_n_players(position_group=position_group,
                                                    show_tier_2=show_tier_2, show_tier_3=show_tier_3)
    print(tier_1_list)

    for (name, x, y) in zip(labels, x_axis_data, y_axis_data):
        if show_tier_1:
            if name in tier_1_list:
                color = 'green'
                label = f'{position} 1' if f'{position} 1' not in plt.gca().get_legend_handles_labels()[1] else ""
            elif name in tier_2_list:
                color = 'yellow'
                label = f'{position} 2' if f'{position} 2' not in plt.gca().get_legend_handles_labels()[1] else ""
            elif name in tier_3_list:
                color = 'red'
                label = f'{position} 3' if f'{position} 3' not in plt.gca().get_legend_handles_labels()[1] else ""
            else:
                color = 'gray'
                label = 'Others' if 'Others' not in plt.gca().get_legend_handles_labels()[1] else ""
                
            # Plot the point with the determined color
            plt.scatter(x, y, color=color, s=SCATTER_MARKERSIZE, label=label)
        else:
            # Plot the point without any special coloring
            plt.scatter(x, y, color='blue', s=SCATTER_MARKERSIZE)
        
        # add annotation
        plt.annotate(name, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
        

    # label axes and title
    plt.xlabel(x_axis_label, fontsize=20) 
    plt.ylabel(y_axis_label, fontsize=20)
    plt.title(f"{year} {position}s {primary_stat} by {secondary_stat}", fontsize=24)

    # adjust the layout to fit everything
    plt.tight_layout()

    # save the image
    if save_fig:
        save_path = f"./images/{position}/{primary_stat}-by-{secondary_stat}"

        if save_suffix:
            save_path += f"-{save_suffix}"

        save_path += ".png"
        plt.savefig(save_path, format="png", bbox_inches="tight")

    # display the image
    plt.show()


def graph_stat_by_name(position_group: List[Player_Season], stat_to_show: str, break_one: int = None,
        break_two: int = None, break_three: int = None, top_n: int = 0, vertical_name_pos: float = 0,
        horizontal_name_pos: float = -0.5, show_tier_1: bool = False, show_tier_2: bool = False,
        show_tier_3: bool = False, save_fig: bool = True, save_suffix: str = ""
    ) -> None:
    """
    Graphs a stat from a position group by the names of the players in the position group / selected data.

    The names go on the x-axis and the stat on the y-axis. This function is very flexible and allows you
    to add highlights and lines to make more detailed graph to see thresholds and tiers of players.
    """
    position = position_group[0].position
    year = position_group[0].year
    data = set_data(position_group=position_group, stat_to_show=stat_to_show) 
    y_axis_label = stat_to_show

    # graphing stat and name
    data.sort()
    data = data[top_n:]
    stat = [stat for stat, _ in data]
    names = [name for _, name in data]

    shift_left = FACTOR_LEFT_VERTICAL * len(names)
    vertical_name_pos = stat[vertical_name_pos]

    # creating graph
    plt.figure(figsize=FIGSIZE) # Increase figure size

    plt.xticks(range(len(names)), names, rotation=ROTATION, ha='right') # Rotate x-tick labels
    plt.plot(names, stat, 'o-', markersize=MARKERSIZE) # Use circles and increase size 

    if break_one:
        above_top = FACTOR_ABOVE_HORIZONTAL * stat[-break_one]
        # top horizontal threshold
        stat_top = stat[-break_one]
        str_top = f"Top {break_one} {position} - {round(stat_top, 2)}"
        plt.axhline(y=stat_top, color='r', linestyle='--')
        plt.text(x=horizontal_name_pos, y=stat_top + above_top, s=str_top, color='Black', fontsize=16)

        # top vertical threshold 
        plt.axvline(x=len(names) - break_one, color='b', linestyle='--') 
        plt.text(x=(len(names) - break_one) - shift_left, y=vertical_name_pos, s=names[-break_one], rotation=90, color='black')

    if break_two:
        # second horizontal threshold
        stat_second = stat[-break_two]
        plt.axhline(y=stat_second, color='r', linestyle='--')
        plt.text(x=horizontal_name_pos, y=stat_second + above_top, s=f"Top {break_two} {position} - {round(stat_second, 2)}", color='Black', fontsize=16)

        # second vertical threshold 
        plt.axvline(x=len(names) - break_two, color='b', linestyle='--') 
        plt.text(x=(len(names) - break_two) - shift_left, y=vertical_name_pos, s=names[-break_two], rotation=90, color='black')

    if break_three:
        # third horizontal threshold
        stat_third = stat[-break_three]
        plt.axhline(y=stat_third, color='r', linestyle='--')
        plt.text(x=horizontal_name_pos, y=stat_third + above_top, s=f"Top {break_three} {position} - {round(stat_third, 2)}", color='Black', fontsize=16)

        # top vertical threshold 
        plt.axvline(x=len(names) - break_three, color='b', linestyle='--') 
        plt.text(x=(len(names) - break_three) - shift_left, y=vertical_name_pos, s=names[-break_three], rotation=90, color='black')

    if show_tier_1:
        tier_1_list, tier_2_list, tier_3_list = grab_top_n_players(position_group=position_group,
                                            show_tier_2=show_tier_2, show_tier_3=show_tier_3)
        # Plotting each point individually for highlighting tier 1 and tier 2
        for i, (name, s) in enumerate(zip(names, stat)):
            if name in tier_1_list:
                color = 'green'
                label = f'{position} 1' if f'{position} 1' not in plt.gca().get_legend_handles_labels()[1] else ""
            elif name in tier_2_list:
                color = 'yellow'
                label = f'{position} 2' if f'{position} 2' not in plt.gca().get_legend_handles_labels()[1] else ""
            elif name in tier_3_list:
                color = 'red'
                label = f'{position} 3' if f'{position} 3' not in plt.gca().get_legend_handles_labels()[1] else ""
            else:
                color = 'gray'
                label = 'Others' if 'Others' not in plt.gca().get_legend_handles_labels()[1] else ""
                
            plt.plot(i, s, 'o-', color=color, markersize=12, label=label)

    # label axes and title
    plt.xlabel(X_AXIS_LABEL, fontsize=20) 
    plt.ylabel(y_axis_label, fontsize=20)
    plt.title(f"{year} Top {len(data)} {position}s by {stat_to_show}", fontsize=24)

    # adjust the layout to fit everything
    plt.tight_layout()

    # save the image
    if save_fig:
        save_path = f"./images/{position}/{stat_to_show}"

        if save_suffix:
            save_path += f"-{save_suffix}"

        save_path += ".png"
        plt.savefig(save_path, format="png", bbox_inches="tight")

    # display the image
    plt.show()