import matplotlib.pyplot as plt
from typing import List
from models.player_season import Player_Season

# constants for text positioning on vertical and horizontal lines
FACTOR_ABOVE_HORIZONTAL = 0.008173076923076924
FACTOR_LEFT_VERTICAL = 0.015625

# graph constants
FIGSIZE = (12, 8)
ROTATION = 45
MARKERSIZE = 12

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


def graph_stat(position_group: List[Player_Season], stat_to_show: str, break_one: int = None,
               break_two: int = None, break_three: int = None, top_n: int = 0,
               show_tier_1: bool = False, show_tier_2: bool = False,
               show_tier_3: bool = False) -> None:
    """
    """
    position = position_group[0].position
    year = position_group[0].year
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
    else:
        raise ValueError("Incorrect stat to show passed through!")
    y_axis_label = stat_to_show

    # graphing stat and name
    data.sort()
    data = data[top_n:]
    stat = [stat for stat, _ in data]
    names = [name for _, name in data]

    shift_left = FACTOR_LEFT_VERTICAL * len(position_group)
    vertical_name_pos = stat[0]

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
        plt.text(x=-0.5, y=stat_top + above_top, s=str_top, color='Black', fontsize=16)

        # top vertical threshold 
        plt.axvline(x=len(position_group) - break_one, color='b', linestyle='--') 
        plt.text(x=(len(position_group) - break_one) - shift_left, y=vertical_name_pos, s=names[-break_one], rotation=90, color='black')

    if break_two:
        # second horizontal threshold
        stat_second = stat[-break_two]
        plt.axhline(y=stat_second, color='r', linestyle='--')
        plt.text(x=-0.5, y=stat_second + above_top, s=f"Top {break_two} {position} - {round(stat_second, 2)}", color='Black', fontsize=16)

        # second vertical threshold 
        plt.axvline(x=len(position_group) - break_two, color='b', linestyle='--') 
        plt.text(x=(len(position_group) - break_two) - shift_left, y=vertical_name_pos, s=names[-break_two], rotation=90, color='black')

    if break_three:
        # third horizontal threshold
        stat_third = stat[-break_three]
        plt.axhline(y=stat_third, color='r', linestyle='--')
        plt.text(x=-0.5, y=stat_third + above_top, s=f"Top {break_three} {position} - {round(stat_third, 2)}", color='Black', fontsize=16)

        # top vertical threshold 
        plt.axvline(x=len(data) - break_three, color='b', linestyle='--') 
        plt.text(x=(len(data) - break_three) - shift_left, y=vertical_name_pos, s=names[-break_three], rotation=90, color='black')

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

    plt.xlabel(X_AXIS_LABEL, fontsize=20) 
    plt.ylabel(y_axis_label, fontsize=20)
    plt.title(f"{year} Top {len(data)} {position}s by {stat_to_show}", fontsize=24)

    plt.tight_layout()
    plt.show()