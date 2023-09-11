import matplotlib.pyplot as plt
from typing import List
from models.player_season import Player_Season

#
FACTOR_ABOVE_HORIZONTAL = 0.008173076923076924
FACTOR_LEFT_VERTICAL = 0.015625

# 
FIGSIZE = (12, 8)
ROTATION = 45
MARKERSIZE = 12

#
X_AXIS_LABEL = "Players"

def graph_stat(position_group: List[Player_Season], stat_to_show: str, break_one: int = None, break_two: int = None, 
               break_three: int = None, top_n: int = 0) -> None:
    """
    """
    position = position_group[0].position
    year = position_group[0].year
    if stat_to_show == "Total Fantasy Points":
        data = [(p.fantasy_points, p.player_name) for p in position_group]
        y_axis_label = stat_to_show
    elif stat_to_show == "Fantasy Points Per Game":
        data = [(p.fantasy_points / p.games, p.player_name) for p in position_group]
        y_axis_label = stat_to_show
    elif stat_to_show == "Total Passing Yards":
        data = [(p.passing_yards, p.player_name) for p in position_group]
        y_axis_label = stat_to_show
    else:
        raise ValueError("Incorrect stat to show passed through!")

    # graphing stat and name
    data.sort()
    data = data[top_n:]
    stat = [stat for stat, _ in data]
    names = [name for _, name in data]

    above_top = FACTOR_ABOVE_HORIZONTAL * stat[-break_one]
    shift_left = FACTOR_LEFT_VERTICAL * len(position_group)
    vertical_name_pos = stat[0]

    # creating graph
    plt.figure(figsize=FIGSIZE) # Increase figure size

    plt.xticks(range(len(names)), names, rotation=ROTATION, ha='right') # Rotate x-tick labels
    plt.plot(names, stat, 'o-', markersize=MARKERSIZE) # Use circles and increase size 

    if break_one:
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

    plt.xlabel(X_AXIS_LABEL, fontsize=20) 
    plt.ylabel(y_axis_label, fontsize=20)
    plt.title(f"{year} Top {len(data)} {position}s by {stat_to_show}", fontsize=24)

    plt.tight_layout()
    plt.show()