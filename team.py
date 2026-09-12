import json 
import pandas as pd


    
def get_top_players_for_team(team_name):

    with open('all_match_info.json', 'r') as json_file:
        data = json.load(json_file)
    # Create a dictionary to store the match count for each player in the specified team
    team_players_match_count = {}

    # Iterate through the matches and update match counts for players in the specified team
    for match_id, match_info in data.items():
        teams = match_info['team']
        if team_name in teams:
            for player in match_info[team_name]:
                if player in team_players_match_count:
                    team_players_match_count[player] += 1
                else:
                    team_players_match_count[player] = 1

    # Sort the players by match count in descending order
    sorted_players = sorted(team_players_match_count.items(), key=lambda x: x[1], reverse=True)[:50]

    # Create a DataFrame from the sorted players data
    df = pd.DataFrame(sorted_players, columns=['Player', 'Match Count'])
    html_table = df.to_html(index=False)

    return html_table


def get_players_df_with_most_seasons_for_team(team_name):
    # Load the JSON data from the fixed file path
    with open('all_match_info.json', 'r') as json_file:
        data = json.load(json_file)

    # Create a dictionary to store the list of seasons each player has participated in for the specified team
    player_seasons = {}

    # Iterate through the matches and update the seasons for each player in the specified team
    for match_info in data.values():
        teams = match_info['team']
        seasons = match_info['season']
        if team_name in teams:
            for player in match_info[team_name]:
                if player in player_seasons:
                    player_seasons[player].add(seasons)
                else:
                    player_seasons[player] = {seasons}

    # Create a DataFrame from the data
    df = pd.DataFrame(player_seasons.items(), columns=["Player", "Seasons"])

    # Calculate the number of seasons each player has been a part of
    df['Num of Seasons'] = df['Seasons'].apply(len)

    # Sort the DataFrame based on the number of seasons in descending order
    df = df.sort_values(by="Num of Seasons", ascending=False)
    html_table = df.to_html(index=False)

    return html_table


def generate_top_players_table(team_name="Chennai Super Kings"):
    data = pd.read_csv("all_matches.csv", dtype={"ball": str, "season": str})

    team_batting_data = data[data['batting_team'] == team_name]
    team_bowling_data = data[data['bowling_team'] == team_name]

    # Filtering out non-valid wicket types
    non_valid_wicket_types = ['run out', 'retired hurt', 'retired out', 'stumped']
    team_bowling_data = team_bowling_data[team_bowling_data['player_dismissed'].notna()]
    team_bowling_data = team_bowling_data[~team_bowling_data['other_wicket_type'].isin(non_valid_wicket_types)]

    top_scorers = (
        team_batting_data.groupby(['season', 'striker'])
        .agg({'runs_off_bat': 'sum'})
        .reset_index()
        .groupby('season')
        .apply(lambda x: x.loc[x['runs_off_bat'].idxmax()])
        .reset_index(drop=True)
    )

    top_wicket_takers = (
        team_bowling_data.groupby(['season', 'bowler'])
        .agg({'player_dismissed': 'count'})
        .reset_index()
        .groupby('season')
        .apply(lambda x: x.loc[x['player_dismissed'].idxmax()])
        .reset_index(drop=True)
    )

    combined_table = pd.merge(top_scorers, top_wicket_takers, on='season', suffixes=('_top_scorer', '_top_wicket_taker'))
    combined_table.columns = ['Season','Batsmen','Runs','Bowler','Wickets']

    html1 = combined_table.to_html(index=False)

    return html1



def generate_purple_orange_players(team_name="Chennai Super Kings"):
    # Read the CSV file into a DataFrame
    data = pd.read_csv('data/purple_orange_players.csv')
    
    # Filter the DataFrame for the specified team
    team_data = data[data['Team'] == team_name]
    
    # Drop the 'Team' column to exclude it from the result
    team_data = team_data.iloc[:, 1:]
    team_data = team_data.to_html(index=False)

    
    return team_data
