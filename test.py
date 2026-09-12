import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


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
    team_name= team_name.lower().replace(' ', '_') 
    plt.savefig("/Users/yogesh/Desktop/PERSONAL/PYTHON/Yogesh_ENV/IPL1/team_graphs/ave_runs_per_season_{}.png".format(team_name))
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
    team_name = team_name.lower().replace(' ', '_') 
    plt.savefig(f"/Users/yogesh/Desktop/PERSONAL/PYTHON/Yogesh_ENV/IPL1/team_graphs/boxplot_per_season_{team_name}.png")
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

    team_name = team_name.lower().replace(' ', '_') 
    plt.savefig("/Users/yogesh/Desktop/PERSONAL/PYTHON/Yogesh_ENV/IPL1/team_graphs/avg_runs_dismissals_per_period_{}.png".format(team_name), dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()

team_names = [
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Sunrisers Hyderabad",
    "Delhi Capitals",
    "Punjab Kings",
    "Gujarat Titans",
    "Lucknow Super Giants"
]

for i in team_names:
    generate_average_total_runs_per_inning(i)
    generate_boxplot_per_season(i)
    generate_dismissals_per_period(i)
