import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import seaborn as sns

def html_runs_balls_per_match(player_name="V Kohli"):
    data = pd.read_csv("all_matches.csv", dtype={"season": str})
    player_data = data[data['striker'] == player_name]
    
    match_stats = []

    for match_id, group in player_data.groupby('match_id'):
        total_runs = group['runs_off_bat'].sum()
        total_balls = len(group)
        total_dismissals = len(group[group['wicket_type'].notnull()])
        match_stats.append({'Match ID': match_id, 'Total Runs': total_runs, 'Total Balls': total_balls,"total_dismissals":total_dismissals})

    # Creating a pandas DataFrame from the list of dictionaries
    stats_df = pd.DataFrame(match_stats)

    # Add a new column for match index
    stats_df['Match Index'] = range(len(stats_df))

    stats_df['Cumulative Runs'] = stats_df['Total Runs'].cumsum()
    stats_df['Cumulative Dismissals'] = stats_df['total_dismissals'].cumsum()
    stats_df['Running Average'] = stats_df['Cumulative Runs']/stats_df['Cumulative Dismissals']

    sns.set(style="white")  # Set Seaborn style with no grid lines

    plt.figure(figsize=(10, 4))

    # Create a bar plot for non-zero runs
    sns.barplot(data=stats_df, x='Match Index', y='Total Runs', color='black')

    # Create a scatter plot for zero runs without legend
    sns.scatterplot(data=stats_df[stats_df['Total Runs'] == 0], x='Match Index', y='Total Runs', color='red', s=80,label='Ducks')

    plt.title("Scores by Match", fontsize=20)
    plt.xlabel("")  # No x-axis title
    plt.ylabel("")
    plt.yticks(fontsize=16)
    # Remove x-axis labels
    plt.xticks(ticks=stats_df['Match Index'][::20], labels=stats_df['Match Index'][::20], rotation=0,fontsize=16)
    plt.plot(stats_df['Match Index'], stats_df['Running Average'], color='tab:blue', linestyle='-', label='Running Average',linewidth=3)

    plt.legend()
    plt.tight_layout()

    # Remove background grid lines and top/right spines
    sns.despine()
    plt.gca().set_frame_on(False)
    # Save the plot as an image (e.g., PNG)
    plt.savefig("static/graph_images/runs_bar_plot_{}.png".format(player_name))
    plt.close()


