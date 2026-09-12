import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def get_top_players():
    # Fixed JSON file path
    json_file_path = 'all_match_info.json'
    
    # Load the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a dictionary to store the match count for each player
    player_match_count = {}

    # Iterate through the matches and update match counts for each player
    for match_id, match_info in data.items():
        teams = match_info['team']
        for team_players in teams:
            for player in match_info[team_players]:
                if player in player_match_count:
                    player_match_count[player] += 1
                else:
                    player_match_count[player] = 1

    # Sort the players by match count in descending order
    sorted_players = sorted(player_match_count.items(), key=lambda x: x[1], reverse=True)

    # Get the top 20 players with the most matches played
    # top_20_players = sorted_players[:20]

    # Convert the top 20 players into a DataFrame
    df = pd.DataFrame(sorted_players, columns=['Player', 'Matches'])
    html_table = df.to_html(index=False)

    return html_table



def get_players_df_with_most_teams():
    # Load the JSON data from the fixed file path
    with open('all_match_info.json', 'r') as json_file:
        data = json.load(json_file)

    # Create a dictionary to store the list of teams each player has played for
    player_teams = {}

    # Iterate through the matches and update the teams for each player
    for match_info in data.values():
        teams = match_info['team']
        for team_players in teams:
            for player in match_info[team_players]:
                if player in player_teams:
                    player_teams[player].add(team_players)
                else:
                    player_teams[player] = {team_players}

    # Create a DataFrame from the data
    df = pd.DataFrame(player_teams.items(), columns=["Player", "Teams"])

    # Calculate the number of teams each player has played for
    df['Num of Teams'] = df['Teams'].apply(len)

    # Filter players who have played for more than 3 teams
    df = df[df['Num of Teams'] > 3]

    # Sort the DataFrame based on the number of teams in descending order
    df = df.sort_values(by="Num of Teams", ascending=False)

    html_table = df.to_html(index=False)

    return html_table



def total_unique_players_for_team_by_season(team_name):
    # Load the JSON data from the fixed file path
    with open("all_match_info.json", 'r') as json_file:
        data = json.load(json_file)

    # Create a set to store unique players for all seasons
    total_unique_players_all_seasons = set()

    # Create a dictionary to store the total unique players for each season
    unique_players_by_season = {}

    # Iterate through the matches and add players who played for the specified team to the sets
    for match_info in data.values():
        teams = match_info['team']
        season = match_info['season']
        if team_name in teams:
            if season not in unique_players_by_season:
                unique_players_by_season[season] = set()
            for player in match_info[team_name]:
                unique_players_by_season[season].add(player)
                total_unique_players_all_seasons.add(player)

    # Calculate the total number of unique players across all seasons
    total_unique_players_count = len(total_unique_players_all_seasons)

    # Calculate the sum of player counts for all seasons
    total_players_all_seasons = sum(len(players) for players in unique_players_by_season.values())

    # Calculate the average number of unique players per season
    average_unique_players_per_season = round(total_players_all_seasons / len(unique_players_by_season), )

    return unique_players_by_season, total_unique_players_count, total_players_all_seasons, average_unique_players_per_season

# List of teams
teams = [
    "Chennai Super Kings",
    "Punjab Kings",
    "Gujarat Titans",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Mumbai Indians",
    "Sunrisers Hyderabad",
    "Rajasthan Royals",
    "Lucknow Super Giants",
    "Delhi Capitals"
]

# Create an empty dictionary to store DataFrames for each team
team_dfs = {}

# Define the desired order of "Season" values (excluding 'All_teams')
desired_season_order = [
    "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
    "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023",
    "Average", "Total"
]

# Iterate through the teams and create DataFrames for each team
for team_name in teams:
    (unique_players_by_season, total_unique_players_count, total_players_all_seasons, average_unique_players_per_season) = total_unique_players_for_team_by_season(team_name)

    # Create a list of dictionaries for each season
    table_data = [{'Season': season, 'Total Players': len(players)} for season, players in unique_players_by_season.items()]

    # Add a row for the total and average
    table_data.append({'Season': 'Total', 'Total Players': int(total_unique_players_count)})
    table_data.append({'Season': 'Average', 'Total Players': int(average_unique_players_per_season)})

    # Create a DataFrame for the current team
    df = pd.DataFrame(table_data)

    # Transpose the DataFrame
    df_transposed = df.T

    # Set the 'Season' values as the header (top row) and reorder the columns
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.iloc[1:]
    
    # Reindex the columns to match the desired order
    df_transposed = df_transposed.reindex(columns=desired_season_order)

    # Store the DataFrame for the current team in the dictionary
    team_dfs[team_name] = df_transposed

# Concatenate all DataFrames into a single MultiIndex DataFrame
result_df = pd.concat(team_dfs.values(), keys=team_dfs.keys())
result_df_filtered = result_df.loc[:, result_df.columns != 'Total']

# Reorder the columns to match the desired season order
result_df_filtered = result_df_filtered[desired_season_order[:-2]]  # Exclude 'Average' and 'Total' columns

# Replace empty strings with NaN values
result_df_filtered = result_df_filtered.replace('', np.nan)

# Convert the data to float
result_df_float = result_df_filtered.astype(float)

cmap = sns.color_palette("coolwarm", as_cmap=True)
vmin, vmax = result_df_float.min().min(), result_df_float.max().max()

# Create the heatmap with custom color thresholds
plt.figure(figsize=(2, 2))
sns.set(font_scale=0.8)  # Adjust the font scale for smaller fonts
sns.heatmap(result_df_float, annot=True, cmap=cmap, fmt=".0f", linewidths=.5, cbar=False, vmin=vmin, vmax=vmax)

# Customize the plot
plt.title("Total Unique Players by Season for IPL Teams (Excluding 'Total')")
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

# plt.savefig("static/graph_images/total_unique_players_for_team_by_season.png", bbox_inches='tight', pad_inches=0)
# plt.close()