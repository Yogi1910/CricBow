import pandas  as pd

global data
data = pd.read_csv('all_matches.csv',dtype={"season": str})


def get_top_run_scorers(data):
    # Read the CSV data into a Pandas DataFrame
    # data = pd.read_csv('all_matches.csv')

    # Group data by player and calculate total runs
    player_runs = data.groupby('striker')['runs_off_bat'].sum()

    # Sort players by total runs in descending order
    sorted_players = player_runs.sort_values(ascending=False)

    # Create a DataFrame with player names and total runs
    top_scorers_df = pd.DataFrame({
        'Player': sorted_players.index[:50],
        'Total Runs': sorted_players.values[:50]
    })

    top_scorers_df.to_csv("static/records_data/most_runs.csv",index=False)

def get_highest_run_scorers(data):
    # Read the CSV data into a Pandas DataFrame
    # data = pd.read_csv('all_matches.csv')

    # Group data by player and match, then calculate the sum of runs
    player_match_runs = data.groupby(['striker', 'match_id'])['runs_off_bat'].sum().reset_index()

    # Sort the DataFrame by runs in descending order
    sorted_player_match_runs = player_match_runs.sort_values(by='runs_off_bat', ascending=False)

    # Filter rows where runs are greater than 99
    top_scorers_filtered = sorted_player_match_runs[sorted_player_match_runs['runs_off_bat'] > 99]


    selected_columns = ['striker', 'runs_off_bat']
    result = top_scorers_filtered.merge(data[['match_id', 'season' ]].drop_duplicates(), on='match_id')
    result = result[selected_columns + ['season']]

    # # Rename the columns for clarity
    result.columns = ['Player', 'Runs', 'Season']

    result.to_csv("static/records_data/highest_scores.csv",index=False)

def get_players_with_more_than_100_sixes(data):
    # Read the CSV data into a Pandas DataFrame
    # data = pd.read_csv('all_matches.csv')

    # Filter rows where the runs_off_bat column is 6 (indicating a six)
    sixes = data[data['runs_off_bat'] == 6]

    # Group data by player and calculate the count of sixes
    player_six_count = sixes.groupby('striker')['runs_off_bat'].count()

    # Filter players with more than 100 sixes
    players_with_more_than_100_sixes = player_six_count[player_six_count > 100]

    # Sort players by the count of sixes in descending order
    sorted_players = players_with_more_than_100_sixes.sort_values(ascending=False)

    # Create a DataFrame with player names and their six count
    result_df = pd.DataFrame({
        'Player': sorted_players.index,
        'Six Count': sorted_players.values
    })

    result_df.to_csv("static/records_data/most_sixes.csv",index=False)

def get_players_with_more_than_100_fours(data):
    # Read the CSV data into a Pandas DataFrame
    # data = pd.read_csv('all_matches.csv')

    # Filter rows where the runs_off_bat column is 4 (indicating a four)
    fours = data[data['runs_off_bat'] == 4]

    # Group data by player and calculate the count of fours
    player_four_count = fours.groupby('striker')['runs_off_bat'].count()

    # Filter players with more than 100 fours
    players_with_more_than_100_fours = player_four_count[player_four_count > 100]

    # Sort players by the count of fours in descending order
    sorted_players = players_with_more_than_100_fours.sort_values(ascending=False)

    # Create a DataFrame with player names and their four count
    result_df = pd.DataFrame({
        'Player': sorted_players.index,
        'Four Count': sorted_players.values
    })

    result_df.to_csv("static/records_data/most_fours.csv",index=False)

def most_hundreds(data):
    # Read the CSV file
    # data = pd.read_csv('all_matches.csv')

    # Create a dictionary to store match-wise player scores
    match_player_scores = {}

    # Iterate through the rows
    for index, row in data.iterrows():
        match_id = row['match_id']
        striker = row['striker']
        runs_off_bat = row['runs_off_bat']

        if match_id not in match_player_scores:
            match_player_scores[match_id] = {}

        if striker not in match_player_scores[match_id]:
            match_player_scores[match_id][striker] = 0

        match_player_scores[match_id][striker] += runs_off_bat

    # Create a list to store the data
    result_data = []

    # Iterate through match IDs and player scores
    for match_id, player_scores in match_player_scores.items():
        for player, runs in player_scores.items():
            if runs > 99:
                result_data.append({'Match_ID': match_id, 'Player': player, 'Runs': runs})

    # Create a DataFrame from the result data
    result_df = pd.DataFrame(result_data)

    # Create a dictionary to store player-wise counts
    player_count = {}

    # Iterate through the result DataFrame
    for index, row in result_df.iterrows():
        player = row['Player']

        if player not in player_count:
            player_count[player] = 0

        player_count[player] += 1

    # Create a DataFrame from the player count data
    count_data = [{'Player': player, 'Count': count} for player, count in player_count.items()]
    count_df = pd.DataFrame(count_data)
    
    # Sort the player count DataFrame in descending order
    sorted_count_df = count_df.sort_values(by='Count', ascending=False)
    
    sorted_count_df.to_csv("static/records_data/most_hundreds.csv",index=False)

def generate_fastest_50_table(data):    
    # Read the CSV file into a DataFrame
    # data = pd.read_csv('all_matches.csv')

    # Remove rows where wides occurred
    data = data[data['wides'].isnull()]

    # Calculate the cumulative sum of runs scored off the bat and count of non-wide balls for each player in each match
    data['cumulative_runs'] = data.groupby(['match_id', 'striker'])['runs_off_bat'].cumsum()
    data['cumulative_balls'] = data.groupby(['match_id', 'striker']).cumcount() + 1

    # Find the records where cumulative_runs cross 50 and balls_taken is less than 20
    fastest_50_records = data[(data['cumulative_runs'] >= 50) & (data['cumulative_balls'] < 20)]

    fastest_50_sorted = fastest_50_records.sort_values('cumulative_balls')

    fastest_50_sorted =  fastest_50_sorted[['season', 'striker', 'cumulative_balls']]
    fastest_50_sorted = fastest_50_sorted.rename(columns={
    'striker': 'Batsman',
    'cumulative_balls': 'Balls',
    'season': 'Season'
        })

    fastest_50_sorted.to_csv("static/records_data/fastest_fifty.csv",index=False)

def most_wickets(data):

    data = pd.read_csv("all_matches.csv")
    # Filter out rows with unwanted wicket types
    unwanted_wicket_types = ["retired out", "retired hurt", "run out"]
    filtered_data = data[~data["wicket_type"].isin(unwanted_wicket_types)]

    # Remove rows where bowler is null
    filtered_data = filtered_data.dropna(subset=["wicket_type"])

    # Group by bowler and count the number of wickets taken by each
    wickets_by_bowler = filtered_data["bowler"].value_counts().reset_index()

    # Print the top bowlers with most wickets
    wickets_by_bowler.head(50).to_csv("static/records_data/most_wickets.csv",index=False)

def best_figures(data):
    # Load the CSV data into a pandas DataFrame

    # Filter out rows with unwanted wicket types
    unwanted_wicket_types = ["retired out", "retired hurt", "run out"]
    filtered_data = data[~data["wicket_type"].isin(unwanted_wicket_types)]

    # Fill NA values in 'wides' and 'noballs' columns with 0
    filtered_data["wides"].fillna(0, inplace=True)
    filtered_data["noballs"].fillna(0, inplace=True)

    # Calculate runs given (runs off bat + wides + noballs) for each row
    filtered_data["runs_given"] = filtered_data["runs_off_bat"] + filtered_data["wides"] + filtered_data["noballs"]

    # Group by match ID and bowler, then count the number of wickets taken and sum of runs given by each bowler in each match
    grouped_data = filtered_data.groupby(["match_id", "bowler"]).agg({"wicket_type": "count", "runs_given": "sum", "season": "first"})

    # Reset the index of the grouped data
    grouped_data = grouped_data.reset_index()

    # Calculate the required format (wickets-runs) and add it as a new column
    grouped_data["wickets_runs_format"] = grouped_data["wicket_type"].astype(str) + "-" + grouped_data["runs_given"].astype(int).astype(str)

    # Sort the data first by wickets in descending order, then by runs in ascending order
    top_wickets_runs_by_bowler = grouped_data.sort_values(by=["wicket_type", "runs_given"], ascending=[False, True]).head(20)

    # Create a DataFrame with the desired columns
    result_table = top_wickets_runs_by_bowler[["bowler", "wickets_runs_format", "season"]]

    # Save the DataFrame to a CSV file
    result_table.to_csv("static/records_data/best_figures.csv", index=False)

def calculate_bowling_stats(data):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv("all_matches.csv")

    # Filter out rows with unwanted wicket types
    unwanted_wicket_types = ["retired out", "retired hurt", "run out"]
    filtered_data = data[~data["wicket_type"].isin(unwanted_wicket_types)]

    # Fill NA values in 'wides' and 'noballs' columns with 0
    filtered_data["wides"].fillna(0, inplace=True)
    filtered_data["noballs"].fillna(0, inplace=True)

    # Calculate runs given (runs off bat + wides + noballs) for each row
    filtered_data["runs_given"] = filtered_data["runs_off_bat"] + filtered_data["wides"] + filtered_data["noballs"]

    # Group by bowler and calculate total wickets taken, total balls bowled, and total runs given by each bowler
    grouped_data = filtered_data.groupby("bowler").agg({"wicket_type": "count", "ball": "count", "runs_given": "sum"})

    # Calculate bowling averages and strike rates only for players who have bowled at least 'min_balls' balls
    grouped_data = grouped_data[grouped_data["ball"] >= 60]
    grouped_data["bowling_average"] = grouped_data["runs_given"] / grouped_data["wicket_type"]
    grouped_data["strike_rate"] = grouped_data["ball"] / grouped_data["wicket_type"]
    grouped_data["economy_rate"] = grouped_data["runs_given"] / (grouped_data["ball"] / 6)

    # Sort the data by bowling averages and strike rates in ascending order
    sorted_by_average = grouped_data.sort_values(by="bowling_average", ascending=True).head(20)
    sorted_by_strike_rate = grouped_data.sort_values(by="strike_rate", ascending=True).head(20)
    sorted_by_economy_rate = grouped_data.sort_values(by="economy_rate", ascending=True).head(20)

    # Format columns as requested
    for df in [sorted_by_average, sorted_by_strike_rate,sorted_by_economy_rate]:
        df["bowling_average"] = df["bowling_average"].round(1)
        df["strike_rate"] = df["strike_rate"].round(1)
        df["economy_rate"] = df["economy_rate"].round(2)

    # Reset the index and return the resulting tables
    best_average = sorted_by_average.reset_index()[["bowler", "ball", "bowling_average"]]
    best_sr      = sorted_by_strike_rate.reset_index()[["bowler", "ball", "strike_rate"]]
    best_economy = sorted_by_economy_rate.reset_index()[["bowler", "ball", "strike_rate"]]


    best_average.to_csv("static/records_data/best_bowling_average.csv",index=False)
    best_sr.to_csv("static/records_data/best_bowling_sr.csv",index=False)
    best_economy.to_csv("static/records_data/best_bowling_sr.csv",index=False)

def players_with_four_wickets(data):
    # Load the CSV data into a pandas DataFrame


    # Filter out rows with unwanted wicket types
    unwanted_wicket_types = ["retired out", "retired hurt", "run out"]
    filtered_data = data[~data["wicket_type"].isin(unwanted_wicket_types)]

    # Group by player and match_id and count the number of wickets taken by each player in each match
    wickets_count = filtered_data.groupby(["bowler", "match_id"])["wicket_type"].count()

    # Filter players who have taken 4 or more wickets in a match
    high_wickets_players = wickets_count[wickets_count >= 4]

    # Count the frequency of such occurrences for each player
    player_frequency = high_wickets_players.index.get_level_values("bowler").value_counts()

    # Create a DataFrame from the player frequency data
    result_df = pd.DataFrame({"Bowler": player_frequency.index, "4+ wickets": player_frequency.values})

    result_df.to_csv("static/records_data/four_plus_wickets.csv",index=False)
    
def highest_innings_totals(data):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv("all_matches.csv")

    # Group by match_id, innings, batting_team, and season, and sum the runs scored and extras
    grouped_data = data.groupby(["match_id", "innings", "batting_team", "season"]).agg({"runs_off_bat": "sum", "extras": "sum", "wicket_type": "count"})

    # Calculate the total runs scored (including extras) in each innings
    grouped_data["total_runs"] = grouped_data["runs_off_bat"] + grouped_data["extras"]

    # Group by match_id and innings, and find the maximum total runs scored
    max_totals = grouped_data.groupby(["match_id", "innings"]).agg({"total_runs": "max", "wicket_type": "max"})

    # Get the top 10 highest totals in descending order
    top_10_totals = max_totals.nlargest(10, "total_runs")

    # Create a DataFrame to store the results
    result_df = pd.DataFrame(columns=["Season", "Batting Team","Innings",  "Total Score"])

    # Iterate through the top 10 highest totals and add details to the result DataFrame
    for (match_id, innings), row in top_10_totals.iterrows():
        match_info = grouped_data.loc[(match_id, innings)]
        result_df = result_df._append({
            
            "Innings": innings,
            "Batting Team": match_info.index.get_level_values("batting_team")[0],
            "Season": match_info.index.get_level_values("season")[0],
            "Total Score": str(row["total_runs"])+"-"+str(row["wicket_type"])
            
        }, ignore_index=True)

    result_df.to_csv("static/records_data/highest_innings_total.csv",index=False)



get_top_run_scorers(data)
get_highest_run_scorers(data)
get_players_with_more_than_100_sixes(data)
get_players_with_more_than_100_fours(data)
most_hundreds(data)
generate_fastest_50_table(data)
most_wickets(data)
best_figures(data)
calculate_bowling_stats(data)
players_with_four_wickets(data)
highest_innings_totals(data)