import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import numpy as np
import csv,math
from scipy.interpolate import make_interp_spline


# ##########################    player.html   ############################################################################


teams_dict = {
    "Mumbai Indians": "MI","Royal Challengers Bangalore": "RCB","Kolkata Knight Riders": "KKR","Chennai Super Kings": "CSK",
    "Rajasthan Royals": "RR","Kings XI Punjab": "KXIP","Delhi Daredevils": "DC","Sunrisers Hyderabad": "SRH","Deccan Chargers": "DC",
    "Delhi Capitals": "DC","Pune Warriors": "PW","Gujarat Lions": "GL","Punjab Kings": "KXIP","Gujarat Titans": "GT","Rising Pune Supergiant": "RPS",
    "Lucknow Super Giants": "LSG","Kochi Tuskers Kerala": "KTK","Rising Pune Supergiants": "RPS"}

def batsmen_statistics_to_html(player_name="V Kohli"):
    def player_statistics(player_name, innings_value):
        data = pd.read_csv("all_matches.csv",dtype={"season": str})

        # Filter rows where the player appears as a striker or non-striker
        player_appearances = data[(data['striker'] == player_name) | (data['non_striker'] == player_name)]

        # Filter rows based on innings value
        if innings_value == 1:
            player_appearances = player_appearances[player_appearances['innings'] == 1]
        elif innings_value == 2:
            player_appearances = player_appearances[player_appearances['innings'] == 2]


        # Filter rows where the player appears as a striker or non-striker
        player_appearances = data[(data['striker'] == player_name)]

        # Filter rows based on innings value
        if innings_value == 1:
            player_appearances = player_appearances[player_appearances['innings'] == 1]
        elif innings_value == 2:
            player_appearances = player_appearances[player_appearances['innings'] == 2]

            

        # Count the unique match IDs to get the number of matches the player has played
        num_innings_player = len(player_appearances['match_id'].unique())

        total_runs_off_bat = player_appearances['runs_off_bat'].sum()

        num_times_dismissed = len(player_appearances[player_appearances['player_dismissed'] == player_name])

        num_times_notout = num_innings_player - num_times_dismissed

        avg = (total_runs_off_bat / num_times_dismissed).round(1) if num_times_dismissed > 0 else 0

        balls_faced = len(player_appearances[(player_appearances['striker'] == player_name) & (player_appearances['wides'].isnull())])

        strike_rate = ((total_runs_off_bat * 100) / balls_faced).round(1) if balls_faced > 0 else 0

        num_fours = len(player_appearances[(player_appearances['striker'] == player_name) & (player_appearances['runs_off_bat'] == 4)])
        num_sixes = len(player_appearances[(player_appearances['striker'] == player_name) & (player_appearances['runs_off_bat'] == 6)])

        # Calculate runs distribution
        match_runs = player_appearances.groupby('match_id')['runs_off_bat'].sum()

        count_200 = 0
        count_100 = 0
        count_50 = 0
        count_30 = 0

        for runs in match_runs:
            if runs >= 200:
                count_200 += 1
            elif runs >= 100:
                count_100 += 1
            elif runs >= 50:
                count_50 += 1
            elif runs >= 30:
                count_30 += 1

        runs_distribution = {
            "100+": count_100,
            "50+": count_50,
            "30-50": count_30
        }

        player_stats = {
            "Inns": num_innings_player,
            "Runs": total_runs_off_bat,
            "NO": num_times_notout,
            "Avg": avg,
            "Balls": balls_faced,
            "SR": strike_rate,
            "4s": num_fours,
            "6s": num_sixes
        }

        # Combine player_stats and runs_distribution into a single dictionary
        combined_stats = {**player_stats, **runs_distribution}

        return combined_stats



    # Create an empty DataFrame to store results
    combined_df = pd.DataFrame()

    # Example usage for different innings values # Replace with the player's name you want to count statistics for

    innings_values = [1, 2, 'both']
    ind = ["1st", "2nd","Total"] 
    combined_df = pd.DataFrame()  # Initialize an empty DataFrame

    for innings in innings_values:
        player_stats = player_statistics(player_name, innings)
        df = pd.DataFrame(player_stats, index=[ind[innings_values.index(innings)]])
        combined_df = pd.concat([combined_df, df])

    html_table = combined_df.to_html()

    return html_table

def bowler_statistics_to_html(bowler_name="JJ Bumrah"):
    # Load CSV data into a DataFrame
    df = pd.read_csv("all_matches.csv")
    
    # Filter rows where the bowler's name matches
    bowler_df = df[(df['bowler'] == bowler_name)]
    
    # Filter rows for 1st innings
    first_innings_df = bowler_df[bowler_df['innings'] == 1]
    
    # Filter rows for 2nd innings
    second_innings_df = bowler_df[bowler_df['innings'] == 2]
    
    # Calculate required statistics for 1st innings
    innings_1st = int(first_innings_df['match_id'].nunique())
    balls_delivered_1st = first_innings_df[(first_innings_df['wides'].isnull())].shape[0]

    

    runs_given_1st = int(first_innings_df['runs_off_bat'].sum() + first_innings_df['wides'].sum() + first_innings_df['noballs'].sum())

    notvalid_dismissals = ['run out', 'retired out', 'retire hurt']
    wickets_1st = first_innings_df[~first_innings_df['wicket_type'].isin(notvalid_dismissals)]['wicket_type'].count()


    if balls_delivered_1st==0:
        economy_1st = 0
        wicket_runs_1st = 0
        avg_1st = 0
        strike_rate_1st = 0
        five_wickets_hauls_1st = 0
        runs_given_1st = 0
    else:

        economy_1st = round(runs_given_1st / (balls_delivered_1st / 6), 2)
        
        wicket_runs_1st = first_innings_df['runs_off_bat'] + first_innings_df['extras']
        avg_1st = (wicket_runs_1st.sum() / wickets_1st).round(2) if wickets_1st > 0 else 0
        strike_rate_1st = (balls_delivered_1st / wickets_1st).round(2) if wickets_1st > 0 else 0

        match_wicket_counts_1st = first_innings_df.groupby('match_id')['wicket_type'].count()
        five_wickets_hauls_1st = match_wicket_counts_1st[match_wicket_counts_1st >= 5].count()
    
    # Calculate required statistics for 2nd innings
    innings_2nd = second_innings_df['match_id'].nunique()
    balls_delivered_2nd = second_innings_df[(second_innings_df['wides'].isnull())].shape[0]
    runs_given_2nd = int(second_innings_df['runs_off_bat'].sum() + second_innings_df['wides'].sum() + second_innings_df['noballs'].sum())
    wickets_2nd = second_innings_df[~second_innings_df['wicket_type'].isin(notvalid_dismissals)]['wicket_type'].count()

    if balls_delivered_2nd==0:
        economy_2nd = 0
        wicket_runs_2nd = 0
        avg_2nd = 0
        strike_rate_2nd = 0
        five_wickets_hauls_2nd = 0
        runs_given_2nd= 0

    else:

        

        
        economy_2nd = round(runs_given_2nd / (balls_delivered_2nd / 6), 2)
        
        wicket_runs_2nd = second_innings_df['runs_off_bat'] + second_innings_df['extras']
        avg_2nd = (wicket_runs_2nd.sum() / wickets_2nd).round(2) if wickets_2nd > 0 else 0
        strike_rate_2nd = (balls_delivered_2nd / wickets_2nd).round(2) if wickets_2nd > 0 else 0

        match_wicket_counts_2nd = second_innings_df.groupby('match_id')['wicket_type'].count()
        five_wickets_hauls_2nd = match_wicket_counts_2nd[match_wicket_counts_2nd >= 5].count()

    # Calculate total statistics
    total_innings = int(innings_1st +innings_2nd)
    total_balls_delivered = balls_delivered_1st + balls_delivered_2nd
    total_runs_given = runs_given_1st + runs_given_2nd
    total_wickets_taken = wickets_1st + wickets_2nd
    total_economy = 0 if total_balls_delivered==0 else round(total_runs_given / (total_balls_delivered / 6), 2)
    total_avg = ((wicket_runs_1st.sum() + wicket_runs_2nd.sum()) / total_wickets_taken).round(2) if total_wickets_taken > 0 else 0
    total_strike_rate = (total_balls_delivered / total_wickets_taken).round(2) if total_wickets_taken > 0 else 0
    total_five_wickets_hauls = five_wickets_hauls_1st + five_wickets_hauls_2nd
    
    # Create DataFrames for each innings and the total
    innings_1st_df = pd.DataFrame({

        'Inns': [innings_1st],
        'Balls': [balls_delivered_1st],
        'Runs': [runs_given_1st],
        'Wkts': [wickets_1st],
        'Econ': [economy_1st],
        'Avg': [avg_1st],
        'SR': [strike_rate_1st],
        '5W': [five_wickets_hauls_1st]
    })
    
    innings_2nd_df = pd.DataFrame({

        'Inns': [innings_2nd],
        'Balls': [balls_delivered_2nd],
        'Runs': [runs_given_2nd],
        'Wkts': [wickets_2nd],
        'Econ': [economy_2nd],
        'Avg': [avg_2nd],
        'SR': [strike_rate_2nd],
        '5W': [five_wickets_hauls_2nd]
    })
    
    total_df = pd.DataFrame({
        'Inns': [int(total_innings)],
        'Balls': [total_balls_delivered],
        'Runs': [total_runs_given],
        'Wkts': [total_wickets_taken],
        'Econ': [total_economy],
        'Avg': [total_avg],
        'SR': [total_strike_rate],
        '5W': [total_five_wickets_hauls]
    })
    
    # Concatenate DataFrames and reset index
    result_df = pd.concat([innings_1st_df, innings_2nd_df, total_df]).reset_index(drop=True)
    result_df.index =  ["1st", "2nd","Total"] 
    


    html_table = result_df.to_html(index=True)

    return html_table
    
def html_runs_balls_per_match(player_name="V Kohli"):
    data = pd.read_csv("all_matches.csv", dtype={"season": str})
    player_data = data[data['striker'] == player_name]
    
    match_stats = []

    for match_id, group in player_data.groupby('match_id'):
        total_runs = group['runs_off_bat'].sum()
        total_balls = len(group)
        total_dismissals = len(group[group['wicket_type'].notnull()])
        match_stats.append({'Match ID': match_id, 'Total Runs': total_runs, 'Total Balls': total_balls, "total_dismissals": total_dismissals})

    stats_df = pd.DataFrame(match_stats)
    stats_df['Match Index'] = range(len(stats_df))
    stats_df['Cumulative Runs'] = stats_df['Total Runs'].cumsum()
    stats_df['Cumulative Dismissals'] = stats_df['total_dismissals'].cumsum()
    stats_df['Running Average'] = stats_df['Cumulative Runs'] / stats_df['Cumulative Dismissals']

    sns.set(style="white")
    plt.figure(figsize=(10, 6))

    # Create a bar plot for non-zero runs using Seaborn
    sns.barplot(data=stats_df, x='Match Index', y='Total Runs', color='black')

    # Create a scatter plot for zero runs without legend
    sns.scatterplot(data=stats_df[stats_df['Total Runs'] == 0], x='Match Index', y='Total Runs', color='red', s=80, label='Ducks')

    plt.title("Scores by Match", fontsize=20)
    plt.xlabel("")
    plt.ylabel("")
    plt.yticks(fontsize=16)
    plt.xticks(ticks=stats_df['Match Index'][::20], labels=stats_df['Match Index'][::20], rotation=0, fontsize=16)
    plt.plot(stats_df['Match Index'], stats_df['Running Average'], color='darkgreen', linestyle='-', label='Running Average', linewidth=3)

    plt.legend()
    plt.tight_layout()

    sns.despine()
    plt.gca().set_frame_on(False)
    plt.savefig("static/graph_images/runs_bar_plot_{}.png".format(player_name))
    plt.close()

def png_runs_scored_per_season(player_name="V Kohli"):
    data = pd.read_csv("all_matches.csv", dtype={"season": str})
    player_data = data[data['striker'] == player_name]
    
    season_stats = player_data.groupby('season')['runs_off_bat'].sum()

    sns.set(style="whitegrid")
    sns.despine()

    plt.figure(figsize=(10, 6))

    # Create a bar plot for runs scored per season using Seaborn
    sns.barplot(data=season_stats.reset_index(), x='season', y='runs_off_bat', color='darkgreen')

    plt.title("Runs Scored by Season", fontsize=20)
    plt.xlabel("", fontsize=12)
    plt.ylabel("", fontsize=12)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.gca().set_frame_on(False)
    plt.savefig("static/graph_images/runs_per_season_bar_plot_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_runs_and_strike_rate_curve(player_name="V Kohli"):
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})
    df['over_no'] = df['ball'].apply(lambda x: int(x.split('.')[0]) + 1)
    player_df = df[(df['striker'] == player_name)]

    runs_by_over = {}
    balls_faced_by_over = {}

    for over in range(1, 21):
        over_df = player_df[player_df['over_no'] == over]
        runs_by_over[over] = over_df['runs_off_bat'].sum()
        balls_faced_by_over[over] = over_df.shape[0]

    strike_rate_by_over = {over: (runs_by_over[over] / balls_faced_by_over[over] * 100).round(2)
                            if balls_faced_by_over[over] > 0 else 0 for over in range(1, 21)}

    overs = list(range(1, 21))
    runs = [runs_by_over[over] for over in overs]
    strike_rates = [strike_rate_by_over[over] for over in overs]

    overs_smooth = [i / 100 for i in range(1, 2001)]
    runs_spline = make_interp_spline(overs, runs, k=2)
    strike_rate_spline = make_interp_spline(overs, strike_rates, k=2)
    runs_smooth = runs_spline(overs_smooth)
    strike_rate_smooth = strike_rate_spline(overs_smooth)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'black'
    ax1.set_xlabel('')
    ax1.set_ylabel('', color=color)
    ax1.plot(overs_smooth, runs_smooth, color=color, label='Runs', linewidth=3)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'darkgreen'
    ax2.set_ylabel('', color=color)
    ax2.plot(overs_smooth, strike_rate_smooth, color=color, marker='', label='Strike Rate', linewidth=3)
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()
    plt.title(f"Runs and Strike Rate Curve for {player_name}",fontsize=20)
    ax1.grid(False)
    ax2.grid(False)

    # Add legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    ax1.grid(False)
    ax2.grid(False)
    
    sns.despine(ax=ax1, top=True, right=True)
    sns.despine(ax=ax2, top=True, right=True)

    plt.savefig("static/graph_images/plot_runs_and_strike_rate_curve_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_dismissals_and_balls_faced_dual_axis(player_name="V Kohli"):
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})
    df['over_no'] = df['ball'].apply(lambda x: int(x.split('.')[0]))
    player_df = df[(df['striker'] == player_name)]

    dismissals_by_over = {}
    balls_faced_by_over = {}

    for over in range(1, 21):
        over_df = player_df[player_df['over_no'] == over]
        dismissals_by_over[over] = over_df['player_dismissed'].count()
        balls_faced_by_over[over] = over_df.shape[0]

    overs = list(range(1, 21))
    dismissals = [dismissals_by_over[over] for over in overs]
    balls_faced = [balls_faced_by_over[over] for over in overs]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'darkgreen'
    ax1.set_xlabel('')
    ax1.set_ylabel('', color=color)
    sns.lineplot(data=dismissals, marker='o', color=color, label='Dismissals', ax=ax1, linewidth=3)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'black'
    ax2.set_ylabel('', color=color)
    sns.lineplot(data=balls_faced, marker='o', color=color, label='Balls Faced', ax=ax2, linewidth=3)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title(f"Dismissals and Balls Faced per Over for {player_name}",fontsize=20)
    plt.xticks(overs)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    ax1.grid(True, linestyle='--', alpha=0.5)
    ax2.grid(False)

    


    sns.despine(ax=ax1, top=True, right=True, left=True, bottom=True)
    sns.despine(ax=ax2, top=True, right=True)

    plt.savefig("static/graph_images/plot_balls_and_dismissals_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_metrics_balls_per_bar_chart(player_name="V Kohli"):
    fig, ax = plt.subplots(figsize=(10, 6))
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})
    df['over_no'] = df['ball'].apply(lambda x: int(x.split('.')[0]))
    player_df = df[(df['striker'] == player_name)]

    balls_per_4 = [0, 0, 0, 0]
    balls_per_6 = [0, 0, 0, 0]
    balls_per_wicket = [0, 0, 0, 0]
    balls_per_0_runs = [0, 0, 0, 0]
    total_balls = [0, 0, 0, 0]

    for index, row in player_df.iterrows():
        over = row['over_no']
        runs = row['runs_off_bat']
        wicket_type = row['wicket_type']

        if over >= 1 and over <= 6:
            period = 0
        elif over >= 7 and over <= 16:
            period = 1
        else:
            period = 2

        total_balls[period] += 1
        total_balls[3] += 1

        if runs == 4:
            balls_per_4[period] += 1
            balls_per_4[3] += 1
        elif runs == 6:
            balls_per_6[period] += 1
            balls_per_6[3] += 1

        if wicket_type:
            balls_per_wicket[period] += 1
            balls_per_wicket[3] += 1

        if runs == 0:
            balls_per_0_runs[period] += 1
            balls_per_0_runs[3] += 1

    periods = ['1-6', '7-16', '17-20', 'Overall']

    balls_per_4 = [total_balls[i] / balls_per_4[i] if balls_per_4[i] != 0 else 0 for i in range(4)]
    balls_per_6 = [total_balls[i] / balls_per_6[i] if balls_per_6[i] != 0 else 0 for i in range(4)]
    balls_per_wicket = [total_balls[i] / balls_per_wicket[i] if balls_per_wicket[i] != 0 else 0 for i in range(4)]
    balls_per_0_runs = [total_balls[i] / balls_per_0_runs[i] if balls_per_0_runs[i] != 0 else 0 for i in range(4)]

    data = {
        'Period': periods * 4,
        'Metric': ['Balls per 4'] * 4 + ['Balls per 6'] * 4 + ['Balls per Wicket'] * 4 + ['Balls per 0 Runs'] * 4,
        'Value': balls_per_4 + balls_per_6 + balls_per_wicket + balls_per_0_runs
    }

    sns.set(style="darkgrid")
    sns.barplot(data=data, x='Period', y='Value', hue='Metric', palette='light:green')

    plt.xlabel('')
    plt.ylabel('')
    plt.title(f"Over Periods for {player_name}", fontsize=16)
    plt.xticks(rotation=0)
    plt.legend(title=None)
    plt.grid(False)

    sns.despine()

    plt.savefig("static/graph_images/plot_metrics_balls_per_bar_chart_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_dismissal_types_bar(player_name="V Kohli"):
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})
    player_df = df[(df['striker'] == player_name) & (df['wicket_type'].notna())]
    player_df['wicket_type'] = player_df['wicket_type'].replace("caught and bowled", "c&b")

    dismissal_types = player_df['wicket_type'].value_counts()

    total_dismissals = dismissal_types.sum()

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    
    # Convert the index of dismissal_types to a DataFrame
    dismissal_types_df = dismissal_types.reset_index()
    dismissal_types_df.columns = ['Dismissal Type', 'Frequency']
    
    
    ax = sns.barplot(data=dismissal_types_df, x='Dismissal Type', y='Frequency', palette='Greens', ci=None)

    plt.xlabel('')
    plt.ylabel('')
    plt.title(f"Dismissal Types for {player_name}", fontsize=20)
    plt.xticks(rotation=0, ha='right',fontsize=16)

    # Adding data labels on top of each bar
    for i, count in enumerate(dismissal_types):
        percentage = (count / total_dismissals) * 100
        plt.text(i, count + 0.2, f"({percentage:.0f}%)", ha='center', va='bottom', fontsize=14)

    plt.tight_layout()
    sns.despine()
    plt.savefig("static/graph_images/dismissal_types_bar_chart_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_average_runs_by_stadium(player_name="V Kohli", min_unique_matches=5):
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})
    player_df = df[df['striker'] == player_name]

    avg_runs_by_stadium = player_df.groupby('venue')['runs_off_bat'].sum() / player_df.groupby('venue')['match_id'].nunique()

    # Filter venues based on the minimum number of matches played
    qualified_venues = avg_runs_by_stadium.index[player_df.groupby('venue')['match_id'].nunique() >= min_unique_matches]

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set(style="whitegrid")

    # Check if there are enough qualified venues to plot
    if len(qualified_venues) < 5:
        message = f"{player_name} has not played enough matches in any venue. Not enough data to plot."
        # Display the message as text in the center of the plot
        ax.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=16)
    else:
        qualified_player_df = player_df[player_df['venue'].isin(qualified_venues)]
        avg_runs_by_stadium = qualified_player_df.groupby('venue')['runs_off_bat'].sum() / qualified_player_df.groupby('venue')['match_id'].nunique()

        avg_runs_by_stadium = avg_runs_by_stadium.sort_values(ascending=False)

        avg_runs_by_stadium = avg_runs_by_stadium.reset_index()
        avg_runs_by_stadium.columns = ["venue", "runs_off_bat"]
        avg_runs_by_stadium["runs_off_bat"] = avg_runs_by_stadium["runs_off_bat"].astype(float)

        ax = sns.barplot(data=avg_runs_by_stadium, x='runs_off_bat', y='venue', palette='Greens', errorbar=None, orient='h')

        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(f"Average Runs by {player_name} in Each Stadium (Min {min_unique_matches} matches)", fontsize=16, y=1.1)

        sns.despine()

    plt.tight_layout()
    # plt.show()

    sns.despine()
    plt.savefig("static/graph_images/stadium_average_chart_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_average_runs_against_teams(player_name="V Kohli", min_unique_matches=5):
    # Read the CSV file
    df = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    # Filter rows for the specified player
    player_df = df[df['striker'] == player_name]

    # Group by bowling team and calculate average runs per unique match
    avg_runs_against_teams = (player_df.groupby('bowling_team')['runs_off_bat'].sum() /
                              player_df.groupby('bowling_team')['match_id'].nunique())

    # Filter teams where the player has played at least min_unique_matches
    qualified_teams = avg_runs_against_teams.index[player_df.groupby('bowling_team')['match_id'].nunique() >= min_unique_matches]

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set(style="whitegrid")

    # Check if there are enough qualified teams to plot
    if len(qualified_teams) < 1:
        message = f"{player_name} has not played enough matches against any bowling team. Not enough data to plot."
        # Display the message as text in the center of the plot
        ax.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=16)
    else:
        # Filter rows for qualified teams and group by team to calculate average runs
        qualified_player_df = player_df[player_df['bowling_team'].isin(qualified_teams)]

        # Replace team names with abbreviations using teams_dict
        qualified_player_df['bowling_team'] = qualified_player_df['bowling_team'].replace(teams_dict)

        # Calculate average runs against teams
        avg_runs_against_teams = (qualified_player_df.groupby('bowling_team')['runs_off_bat'].sum() /
                                  qualified_player_df.groupby('bowling_team')['wicket_type'].count())

        avg_runs_against_teams = avg_runs_against_teams.sort_values(ascending=False)

        ax = sns.barplot(x=avg_runs_against_teams.index, y=avg_runs_against_teams.values, palette="Greens")

        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(f"Average Runs by {player_name} Against Each Bowling Team (Min {min_unique_matches} matches)", fontsize=16, y=1.1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='right')

        for i, avg_runs in enumerate(avg_runs_against_teams):
            ax.text(i, avg_runs + 0.5, f"{avg_runs:.0f}", ha='center', va='bottom', fontsize=14)

    sns.despine()

    plt.tight_layout()
    plt.savefig("static/graph_images/opposition_average_chart_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def generate_player_bowler_plots(player_name="V Kohli", min_balls=20): 

    # Load the CSV file into a pandas DataFrame
    file_name = "all_matches.csv"
    match_data = pd.read_csv(file_name)

    # Filter matches for the specified player
    player_matches = match_data[match_data['striker'] == player_name]

    # Group matches by bowler and calculate stats
    bowler_stats = player_matches.groupby('bowler').agg({'runs_off_bat': 'sum', 'ball': 'count'})
    
    # Filter bowlers based on minimum balls bowled
    bowler_stats = bowler_stats[bowler_stats['ball'] >= min_balls]

    # Check if there are enough qualified bowlers to plot
    if bowler_stats.empty:
        # Create a figure and a message subplot
        fig, ax_message = plt.subplots(figsize=(10, 5))
        ax_message.axis('off')  # Turn off axis for the message subplot
        message = f"{player_name} has not faced enough deliveries from any bowler. Not enough data to plot."
        ax_message.text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center', fontsize=16)
        plt.show()
        return

    bowler_stats['strike_rate'] = (bowler_stats['runs_off_bat'] / bowler_stats['ball']) * 100

    # Create a figure with subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Sort bowlers by ascending and descending strike rates
    top_bowlers_asc = bowler_stats.sort_values(by='strike_rate').head(10)
    top_bowlers_desc = bowler_stats.sort_values(by='strike_rate', ascending=False).head(10)

    # Plot for best strike rates
    axs[0].barh(top_bowlers_asc.index, top_bowlers_asc['strike_rate'], color='#93C572')
    axs[0].set_xlabel('Strike Rate')
    axs[0].set_ylabel('Bowler')
    axs[0].set_title('Top 10 Bowlers (Worst Strike Rate)', fontsize=16, y=1.1)

    # Plot for worst strike rates
    axs[1].barh(top_bowlers_desc.index, top_bowlers_desc['strike_rate'], color='#228B22')
    axs[1].set_xlabel('Strike Rate')
    axs[1].set_ylabel('Bowler')
    axs[1].set_title('Top 10 Bowlers (Best Strike Rate)', fontsize=16, y=1.1)

    # Adding maximum dismissals plot
    player_dismissals = match_data[match_data['player_dismissed'] == player_name]
    bowler_dismissals = player_dismissals['bowler'].value_counts()
    
    # Filter bowlers based on minimum balls bowled
    # bowler_dismissals = bowler_dismissals[bowler_stats.index.isin(bowler_dismissals.index) & (bowler_stats['ball'] >= min_balls)]
    filtered_bowler_stats = bowler_stats[bowler_stats['ball'] >= min_balls]

    # Filter bowler_dismissals using the filtered index
    bowler_dismissals = bowler_dismissals[bowler_dismissals.index.isin(filtered_bowler_stats.index)]
    
    if bowler_dismissals.empty:
        # Create a message subplot for maximum dismissals
        axs[2].axis('off')  # Turn off axis for the message subplot
        message = f"{player_name} has not been dismissed by any qualified bowler. Not enough data to plot."
        axs[2].text(0.5, 0.5, message, horizontalalignment='center', verticalalignment='center', fontsize=16)
    else:
        top_bowlers_max_dismissals = bowler_dismissals.head(10)
        axs[2].barh(top_bowlers_max_dismissals.index, top_bowlers_max_dismissals.values, color='darkgreen')
        axs[2].set_xlabel('Dismissals')
        axs[2].set_ylabel('Bowler')
        axs[2].set_title('Top 10 Bowlers Dismissing {}'.format(player_name), fontsize=16, y=1.1)

    plt.tight_layout()

    sns.despine()
    plt.savefig("static/graph_images/bowler_bar_plots_{}.png".format(player_name))
    plt.close()
   
def plot_runs_warm(player_name="V Kohli"):
    # Read the CSV file
    data = pd.read_csv("all_matches.csv")

    # Filter for the specified player and 1st innings
    player_innings1_data = data[(data['striker'] == player_name) & (data['innings'] == 1)]

    # Filter for the specified player and 2nd innings
    player_innings2_data = data[(data['striker'] == player_name) & (data['innings'] == 2)]

    # Group the data by match for 1st innings
    grouped_innings1_data = player_innings1_data.groupby('match_id')

    # Group the data by match for 2nd innings
    grouped_innings2_data = player_innings2_data.groupby('match_id')

    # Initialize lists to store cumulative balls and runs for each match
    cumulative_balls_innings1 = []
    cumulative_runs_innings1 = []

    cumulative_balls_innings2 = []
    cumulative_runs_innings2 = []

    # Iterate through each group and calculate cumulative balls and runs per match for 1st innings
    for group_name, group_data in grouped_innings1_data:
        cumulative_balls = 0
        cumulative_runs = 0
        balls_per_match = []
        runs_per_match = []

        for index, row in group_data.iterrows():
            runs_off_bat = row['runs_off_bat']
            wides = row['wides']

            if pd.isna(wides):
                cumulative_balls += 1

            if pd.notna(runs_off_bat):
                cumulative_runs += runs_off_bat
                balls_per_match.append(cumulative_balls)
                runs_per_match.append(cumulative_runs)

        cumulative_balls_innings1.extend(balls_per_match)
        cumulative_runs_innings1.extend(runs_per_match)



    # Iterate through each group and calculate cumulative balls and runs per match for 2nd innings
    for group_name, group_data in grouped_innings2_data:
        cumulative_balls = 0
        cumulative_runs = 0
        balls_per_match = []
        runs_per_match = []

        for index, row in group_data.iterrows():
            runs_off_bat = row['runs_off_bat']
            extras = row['extras']
            wides = row['wides']

            if pd.isna(wides):
                cumulative_balls += 1

            if pd.notna(runs_off_bat):
                cumulative_runs += runs_off_bat
                balls_per_match.append(cumulative_balls)
                runs_per_match.append(cumulative_runs)

        cumulative_balls_innings2.extend(balls_per_match)
        cumulative_runs_innings2.extend(runs_per_match)

    # Create DataFrames to hold the cumulative data for each innings
    cumulative_data_innings1 = pd.DataFrame({
        'Cumulative Balls': cumulative_balls_innings1,
        'Cumulative Runs': cumulative_runs_innings1,
        'Innings': '1st Innings'
    })
    

    cumulative_data_innings2 = pd.DataFrame({
        'Cumulative Balls': cumulative_balls_innings2,
        'Cumulative Runs': cumulative_runs_innings2,
        'Innings': '2nd Innings'
    })

    # Combine the data for both innings
    combined_data = pd.concat([cumulative_data_innings1, cumulative_data_innings2])

    # Plot the curve using Seaborn
    sns.set(style="whitegrid")
    plt.figure(figsize=(5,5))
    sns.lineplot(x='Cumulative Balls', y='Cumulative Runs', hue='Innings', data=combined_data, marker='.', palette={'1st Innings': 'black', '2nd Innings': 'darkgreen'})
    plt.xlabel('Balls')
    plt.ylabel('Runs')
    plt.title(f'{player_name}\'s Innings progression against balls',fontsize = 14)
    plt.legend()
    plt.grid()
    sns.despine()
    plt.tight_layout()
    plt.savefig("static/graph_images/runs_warm_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_boundaries_for_player(player_name='V Kohli'):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv('all_matches.csv')

    # Filter data for the specific player as the striker
    player_data = data[data['striker'] == player_name]
    
    # Calculate over number for each ball
    player_data['over_no'] = player_data['ball'].apply(math.ceil)
    
    # Remove wides from the count
    valid_balls = player_data[player_data['wides'].isnull()]

    # Group data by over number and calculate balls, 4s, and 6s
    grouped_data = valid_balls.groupby('over_no').agg(
        balls_faced=('ball', 'count'),
        fours_hit=('runs_off_bat', lambda x: (x == 4).sum()),
        sixes_hit=('runs_off_bat', lambda x: (x == 6).sum()),
        total_runs=('runs_off_bat', 'sum')
    ).reset_index()

    # Calculate balls per 4s and balls per 6s
    grouped_data['balls_per_4'] = (grouped_data['balls_faced'] / grouped_data['fours_hit']).replace([np.inf, -np.inf], 0) 
    grouped_data['balls_per_6'] = (grouped_data['balls_faced'] / grouped_data['sixes_hit']).replace([np.inf, -np.inf], 0) 

    max_balls_per_4 = max(grouped_data['balls_per_4'])
    max_balls_per_6 = max(grouped_data['balls_per_6'])
    max_y_limit = max(max_balls_per_4, max_balls_per_6) + 1

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    sns.barplot(data=grouped_data, x='over_no', y='balls_per_4', color='darkgreen')
    plt.title(f'Over wise Balls per 4 for {player_name}', fontsize=16)
    plt.xlabel('Over Number')
    plt.ylabel('')
    plt.xticks(rotation=0, ticks=grouped_data[grouped_data['over_no'] % 2 == 0]['over_no'])
    plt.gca().yaxis.grid(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylim(0, max_y_limit)  # Set y-axis limits

    plt.subplot(1, 2, 2)
    sns.barplot(data=grouped_data, x='over_no', y='balls_per_6', color='grey')
    plt.title(f'Over wise Balls per 6 for {player_name}', fontsize=16)
    plt.xlabel('Over Number')
    plt.ylabel('')
    plt.xticks(rotation=0, ticks=grouped_data[grouped_data['over_no'] % 2 == 0]['over_no'])
    plt.gca().yaxis.grid(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.ylim(0, max_y_limit)  # Set y-axis limits

    # plt.subplot(1, 3, 3)
    # plt.pie([grouped_data['fours_hit'].sum() * 4 + grouped_data['sixes_hit'].sum() * 6, grouped_data['total_runs'].sum()],
    #         labels=['4s and 6s', 'Others'], colors=['tab:blue', 'tab:red'],
    #         autopct='%1.1f%%', shadow=True, startangle=140)
    # plt.title('Distribution of Runs from 4s and 6s', fontsize=16)

    # plt.tight_layout()
    # sns.despine()
    plt.savefig("static/graph_images/boundaries_for_player_{}.png".format(player_name), bbox_inches='tight', pad_inches=0)
    plt.close()

# ##########################    team.html   ############################################################################


def generate_average_total_runs_per_inning(team_name="Chennai Super Kings"):
    data = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    team_data = data[data['batting_team'] == team_name]

    team_data['total_runs'] = team_data['runs_off_bat'] + team_data['extras']

    data['total_runs'] = data['runs_off_bat'] + data['extras']

    inning_average_runs = (
        team_data.groupby(['season', 'match_id', 'innings'])
        .agg({'total_runs': 'sum'})
        .groupby(['season', 'innings'])
        .agg({'total_runs': 'mean'})
        .reset_index()
    )


    inning_average_runs1 = (
        data.groupby(['season', 'match_id', 'innings'])
        .agg({'total_runs': 'sum'})
        .groupby(['season', 'innings'])
        .agg({'total_runs': 'mean'})
        .reset_index()
    )
    
    unique_seasons = inning_average_runs['season'].unique()
    for season in unique_seasons:
        inning_average_runs['season'] = inning_average_runs['season'].str.replace(season, season[-2:])

    sns.set_style("white")
    plt.figure(figsize=(10, 4))  # Increase the width for two scatterplots

    # 1st Inning subplot
    plt.subplot(1, 2, 1)
    inning1_data = inning_average_runs[inning_average_runs['innings'] == 1]
    max_runs = max(inning1_data['total_runs'].max(), inning_average_runs[inning_average_runs['innings'] == 2]['total_runs'].max())
    if np.isnan(max_runs) or np.isinf(max_runs):
        max_runs = 300
    sns.barplot(x='season', y='total_runs', data=inning1_data, color='grey')
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Average Total Runs in 1st Inning per Season')
    plt.ylim(130, max_runs+5)  # Set y-axis limit

    # Calculate and plot the overall average line for the team name in the 1st inning
    overall_avg_1st_inning = inning1_data['total_runs'].mean()
    plt.axhline(overall_avg_1st_inning, color='red', linestyle='-', label=f'Overall Average ({team_name})')
    plt.grid(False) 
    ax1 = plt.gca()
    ax1.set_facecolor('none')  
    # Add scatterplot for 1st inning and all seasons
    # all_seasons_data_1st_inning = inning_average_runs1[(inning_average_runs1['innings'] == 1)]
    # sns.scatterplot(x='season', y='total_runs', data=all_seasons_data_1st_inning, color='black', label='All Seasons', marker='o')

    # Calculate and plot the average runs for all teams in the 1st inning
    all_teams_avg_1st_inning = inning_average_runs[(inning_average_runs['innings'] == 1)]
    all_teams_avg_1st_inning = all_teams_avg_1st_inning.groupby('season')['total_runs'].mean().reset_index()

    # 2nd Inning subplot
    plt.subplot(1, 2, 2)
    inning2_data = inning_average_runs[inning_average_runs['innings'] == 2]
    sns.barplot(x='season', y='total_runs', data=inning2_data, color='darkgreen')
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Average Total Runs in 2nd Inning per Season')
    plt.ylim(120, max_runs)  # Set y-axis limit

    # Calculate and plot the overall average line for the team name in the 2nd inning
    overall_avg_2nd_inning = inning2_data['total_runs'].mean()
    plt.axhline(overall_avg_2nd_inning, color='red', linestyle='-', label=f'Overall Average ({team_name})')
    plt.grid(False) 
    ax2 = plt.gca()
    ax2.set_facecolor('none')  
    # Add scatterplot for 2nd inning and all seasons
    # all_seasons_data_2nd_inning = inning_average_runs1[(inning_average_runs1['innings'] == 2)]
    # sns.scatterplot(x='season', y='total_runs', data=all_seasons_data_2nd_inning, color='black', label='All Seasons', marker='o')

    # Calculate and plot the average runs for all teams in the 2nd inning
    all_teams_avg_2nd_inning = inning_average_runs[(inning_average_runs['innings'] == 2)]
    all_teams_avg_2nd_inning = all_teams_avg_2nd_inning.groupby('season')['total_runs'].mean().reset_index()
    plt.grid(False) 

    plt.tight_layout()
    plt.savefig("static/graph_images_team/ave_runs_per_season_{}.png".format(team_name))
    plt.close()

def generate_boxplot_per_season(team_name="Chennai Super Kings"):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    data = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    team_data = data[(data['batting_team'] == team_name) & ((data['innings'] == 1) | (data['innings'] == 2))]

    team_data['total_runs'] = team_data['runs_off_bat'] + team_data['extras']

    inning_average_runs = (
        team_data.groupby(['season', 'match_id', 'innings'])
        .agg({'total_runs': 'sum'})
        .reset_index()
    )

    plt.figure(figsize=(10, 4))
    
    palette = {1: 'darkgreen', 2: 'grey'}
    
    sns.boxplot(
        data=inning_average_runs,
        x='season',
        y='total_runs',
        hue='innings',
        palette=palette,
        width=0.8,  # Increase the width of the boxes
        flierprops=dict(marker='o', markersize=6, markerfacecolor='red', markeredgecolor='red')
    )
    
    plt.xlabel('', fontsize=12)
    plt.ylabel('', fontsize=12)
    plt.title('Spread of Runs per Season and Inning', fontsize=14)
    plt.xticks(rotation=0, ha="right")
    plt.ylim(75, max(inning_average_runs['total_runs'].max(), 275))  # Set y-axis limit
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    plt.legend(title='Inning', loc='upper right', labels=['Inning 1', 'Inning 2'])
    
    plt.tight_layout()
    plt.savefig(f"static/graph_images_team/boxplot_per_season_{team_name}.png")
    plt.close()


def generate_average_scores_curves(team_name="Chennai Super Kings"):
    # Import necessary modules
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    data = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    team_data = data[data['batting_team'] == team_name]

    team_data['total_runs'] = team_data['runs_off_bat'] + team_data['extras']
    team_data['over'] = team_data['ball'].apply(lambda x: int(x.split('.')[0]))

    over_ranges = [(0, 6), (7, 15), (16, 20)]

    plt.figure(figsize=(10, 4))
    
    sns.set_style("white")  # Set style to white to have no grids and a white background

    max_y = 15  # Set the minimum y-axis value to 15

    for i, over_range in enumerate(over_ranges, start=1):
        over_start, over_end = over_range
        range_data = team_data[(team_data['over'] >= over_start) & (team_data['over'] <= over_end)]
        
        # Calculate average scores
        average_scores = range_data.groupby(['season', 'match_id'])['total_runs'].sum().groupby('season').mean()
        max_y = max(80, average_scores.max())  # Update max_y with the maximum value
        
        # Calculate wicket count
        wickets_count = range_data[range_data['wicket_type'].notna()].groupby(['season', 'match_id'])['wicket_type'].count().groupby('season').mean()

        plt.subplot(1, 3, i)
        ax1 = sns.lineplot(x=average_scores.index, y=average_scores.values, marker='o', label=f'{over_start}-{over_end} overs',color='darkgreen')
        ax1.set_xlabel('')
        ax1.set_ylabel('')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        ax1.grid(False)  # Remove grid lines
        ax2 = ax1.twinx()
        ax2.set_ylabel('')
        ax1.set_ylim(20, max_y)  # Set the y-axis limit for average runs
        ax2.set_ylim(0.5, wickets_count.max() + 1)  # Set the y-axis limit for wickets
        sns.lineplot(x=wickets_count.index, y=wickets_count.values, marker='o', color='black')
        
        ax2.grid(False)  # Remove grid lines for the secondary axis

    plt.tight_layout()
    plt.savefig("static/graph_images_team/avg_runs_per_period_{}.png".format(team_name))
    plt.close()


def generate_dismissals_per_period(team_name="Chennai Super Kings"):
    data = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    team_data = data[data['batting_team'] == team_name]

    team_data['total_runs'] = team_data['runs_off_bat'] + team_data['extras']
    team_data['over'] = team_data['ball'].apply(lambda x: int(x.split('.')[0]))

    over_ranges = [(0, 6), (7, 15), (16, 20)]

    # Set Seaborn style to remove grey background and grid lines
    sns.set_style("white")

    plt.figure(figsize=(10, 4))

    max_y_scores = 15  # Set the minimum y-axis value for scores
    max_y_dismissals = 1  # Set the minimum y-axis value for dismissals
    
    for i, over_range in enumerate(over_ranges, start=1):
        over_start, over_end = over_range
        range_data = team_data[(team_data['over'] >= over_start) & (team_data['over'] <= over_end)]
        
        # Average Scores Plot
        average_scores = range_data.groupby(['season', 'match_id'])['total_runs'].sum().groupby('season').mean()
        max_y_scores = max(max_y_scores, average_scores.max())
        
        plt.subplot(2, 3, i)
        plt.grid(False)  # Remove grid lines
        sns.lineplot(x=average_scores.index, y=average_scores.values, marker='o', label=f'{over_start}-{over_end} overs',color='black')
        plt.xlabel('')
        plt.ylabel('')
        plt.title(f'Average Score for {over_start}-{over_end} overs')
        plt.xticks(rotation=45)
        plt.legend()
        
        # Average Dismissals Plot (Curve)
        dismissals_per_period = range_data.groupby(['season', 'match_id'])['player_dismissed'].count().groupby('season').mean()
        max_y_dismissals = max(max_y_dismissals, dismissals_per_period.max())
        
        plt.subplot(2, 3, i + 3)
        plt.grid(False)  # Remove grid lines
        sns.lineplot(x=dismissals_per_period.index, y=dismissals_per_period.values, marker='o', color='darkgreen', label=f'{over_start}-{over_end} overs')
        plt.xlabel('')
        plt.ylabel('')
        plt.title(f'Average Dismissals for {over_start}-{over_end} overs')
        plt.xticks(rotation=45)
        plt.ylim(1, max_y_dismissals)
        plt.legend()
    
    plt.tight_layout()
    plt.savefig("static/graph_images_team/avg_runs_dismissals_per_period_{}.png".format(team_name), dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()


def get_unique_strikers(team_name="Channai Super Kings"):
    strikers = []

    with open("all_matches.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['batting_team'] == team_name and row['season'] == '2022':
                strikers.append(row['striker'])

    return list(set(strikers))

def get_unique_bowlers(team_name="Chennai Super Kings"):
    bowlers = []

    with open("all_matches.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['bowling_team'] == team_name and row['season'] == '2022':
                bowlers.append(row['bowler'])

    return list(set(bowlers))

