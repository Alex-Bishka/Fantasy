import plotly.express as px


def prep_df_for_scatter_plot(df):
    """
    Take sorted season or per game dataframe and assign colors to tier the players
    from best to worst.
    """
    df.reset_index(inplace=True)
    
    # Calculate the reverse index for each row (starting from the bottom)
    reverse_index = (len(df) - 1) - df.index

    # Calculate the group for each row based on the reverse index
    group = reverse_index // 12
    
    # Map each group to a color
    colors = {0: 'Tier 1', 1: 'Tier 2', 2: 'Tier 3', 3: 'Tier 4', 4: 'Tier 5', 5: 'Tier 6'}
    df['Color'] = group.map(colors)
    
    return df


def create_scatter_plot(df, stat, start_index=-30, save_path=None,
                        three_tiers=False, four_tiers=False, custom_appendix=None):
    """
    Helper function to graph scatter plots for a stat against a player name. Works for season total and 
    per game numbers.
    """
    position = df["position"].iloc[0]

    # Adjusting titles for figure layout
    title = f"2023 {position} {' '.join([s.capitalize() for s in stat.split('_')])}"
    title = title.replace("Epa", "EPA")
    y_axis_title = f"{' '.join([s.capitalize() for s in stat.split('_')])}"
    y_axis_title = y_axis_title.replace("Epa", "EPA")
    
    if custom_appendix in df.columns[-2]:
        stat += "_" + custom_appendix
        title += f" {' '.join([s.capitalize() for s in custom_appendix.split('_')])}"
        y_axis_title += f" ({' '.join([s.capitalize() for s in custom_appendix.split('_')])})"
    
    # scatter plot
    fig = px.scatter(df[start_index:], x="player_name", y=stat, color='Color')

    # Add a horizontal line at pos1 line
    pos1_line_h = df[stat].iloc[-12]
    fig.add_shape(type="line",
                  x0=0, x1=1, y0=pos1_line_h, y1=pos1_line_h,
                  line=dict(color="black", width=2),
                  xref="paper", yref="y")

    # add a vertical line at pos1
    pos1_line_v = df["player_name"].iloc[-12]
    fig.add_shape(type="line",
                  x0=pos1_line_v, x1=pos1_line_v, y0=df[stat].iloc[start_index - 10], 
                  y1=df[stat].max()* 1.1,
                  line=dict(color="black", width=2),
                  xref="x", yref="y")

    # Add a horizontal line at pos2 line
    pos2_line_h = df[stat].iloc[-24]
    fig.add_shape(type="line",
                  x0=0, x1=1, y0=pos2_line_h, y1=pos2_line_h,
                  line=dict(color="black", width=2),
                  xref="paper", yref="y")

    # add a vertical line at pos2
    pos2_line_v = df["player_name"].iloc[-24]
    fig.add_shape(type="line",
                  x0=pos2_line_v, x1=pos2_line_v, y0=df[stat].iloc[start_index - 10], 
                  y1=df[stat].max()* 1.1,
                  line=dict(color="black", width=2),
                  xref="x", yref="y")
    
    if three_tiers:
        assert(start_index < -40)
        
        # Add a horizontal line at pos3 line
        pos3_line_h = df[stat].iloc[-36]
        fig.add_shape(type="line",
                      x0=0, x1=1, y0=pos3_line_h, y1=pos3_line_h,
                      line=dict(color="black", width=2),
                      xref="paper", yref="y")

        # add a vertical line at pos3
        pos3_line_v = df["player_name"].iloc[-36]
        fig.add_shape(type="line",
                      x0=pos3_line_v, x1=pos3_line_v, y0=df[stat].iloc[start_index - 10], 
                      y1=df[stat].max()* 1.1,
                      line=dict(color="black", width=2),
                      xref="x", yref="y")
    
    if four_tiers:
        assert(start_index < -52)
        
        # Add a horizontal line at pos4 line
        pos4_line_h = df[stat].iloc[-48]
        fig.add_shape(type="line",
                      x0=0, x1=1, y0=pos4_line_h, y1=pos4_line_h,
                      line=dict(color="black", width=2),
                      xref="paper", yref="y")

        # add a vertical line at pos4
        pos4_line_v = df["player_name"].iloc[-48]
        fig.add_shape(type="line",
                      x0=pos4_line_v, x1=pos4_line_v, y0=df[stat].iloc[start_index - 10], 
                      y1=df[stat].max()* 1.1,
                      line=dict(color="black", width=2),
                      xref="x", yref="y")

    fig.update_traces(marker=dict(size=12))
    
    fig.update_layout(
        title=title,
        xaxis_title="Player Names",
        yaxis_title=y_axis_title,
        legend_title=f'{position} Tiers',
    )

    if save_path:
        fig.write_html(save_path)
    fig.show()