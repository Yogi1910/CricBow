import pandas as pd
import json,csv


def calculate_teams_statistics(team1, team2):

    if team1 == team2:
        statistics_html =  '''
        <table class="table table-striped" border="0" style="width:50%; margin:0 auto;">
            <tr>
                <td style="text-align:center;">
                    Both teams can't be the same! 😄. Please select different teams to get the statistics.
                </td>
            </tr>
        </table>
        '''
        return statistics_html

    # ... (the rest of your existing code)


    def get_last_n_items(lst, n, fill_value='N/A'):
        return lst[-n:] + [fill_value] * (n - len(lst))

    def get_last_5_matches_all(team):
        last_5_matches = []
        for match_id, match_info in match_data.items():
            if team in match_info['team']:
                if "winner" in match_info:
                    winner = match_info['winner']

                    # Custom emojis for Win and Loss
                    outcome_icon = '\U0001F7E2' if winner == team else '\U0001F534'
                else:
                    outcome_icon = '\U0001F6AB'  # Draw or No result

                last_5_matches.insert(0, outcome_icon)
            if len(last_5_matches) >= 5:
                break
        return get_last_n_items(last_5_matches, 5)

    def get_last_5_toss_decisions(team):
        last_5_toss_decisions = []
        for match_id, match_info in match_data.items():
            if team in match_info['team']:
                toss_winner = match_info['toss_winner']
                toss_decision = match_info['toss_decision']

                # Custom emojis for Bat and Field
                toss_icon = 'Bat' if toss_winner == team else 'F'

                last_5_toss_decisions.insert(0, toss_icon)
            if len(last_5_toss_decisions) >= 5:
                break
        return get_last_n_items(last_5_toss_decisions, 5)

    with open('all_match_info.json', 'r') as file:
        match_data = json.load(file)

    matches_played_team1 = 0
    matches_played_team2 = 0
    team1_wins = 0
    team2_wins = 0
    outcome = []

    for match_id, match_info in match_data.items():



        if team1 in match_info['team'] and team2 in match_info['team']:
            matches_played_team1 += 1
            matches_played_team2 += 1
            if "winner" in match_info:
                winner = match_info['winner']
                if winner == team1:
                    team1_wins += 1
                elif winner == team2:
                    team2_wins += 1


            else:
                outcome.append(match_info['outcome'])

            

        

    last_5_matches_team1 = get_last_5_matches_all(team1)
    last_5_matches_team2 = get_last_5_matches_all(team2)
    
    last_5_toss_decisions_team1 = get_last_5_toss_decisions(team1)
    last_5_toss_decisions_team2 = get_last_5_toss_decisions(team2)

    team1_win_percentage = (team1_wins / matches_played_team1) * 100 if matches_played_team1 > 0 else 0
    team2_win_percentage = (team2_wins / matches_played_team2) * 100 if matches_played_team2 > 0 else 0

    data = {
    team1: [matches_played_team1, f'{team1_wins} ({int(team1_win_percentage)}%) ', ', '.join(last_5_matches_team1), ', '.join(last_5_toss_decisions_team1)],
    'Statistic': ['Total Matches', f'Wins by {team1}', 'Last 5 Match Results', 'Last 5 Toss Decisions'],
    team2: [matches_played_team2, f' {team2_wins} ({int(team2_win_percentage)}%)', ', '.join(last_5_matches_team2), ', '.join(last_5_toss_decisions_team2)]
    }

    df_performance = pd.DataFrame(data)

    # Load the CSV data into a pandas DataFrame
    data_matches = pd.read_csv('all_matches.csv')

    data_matches = data_matches[(data_matches['batting_team'].isin([team1, team2])) & (data_matches['bowling_team'].isin([team1, team2]))]

    numeric_columns = ['runs_off_bat', 'extras', 'wides', 'noballs', 'byes', 'legbyes']

    data_matches[numeric_columns] = data_matches[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Calculate the total runs for each row
    data_matches['total_runs'] = data_matches[numeric_columns].sum(axis=1)
    extras_columns = ['extras', 'wides', 'noballs', 'byes', 'legbyes']
    data_matches['extras_runs'] = data_matches[extras_columns].sum(axis=1)
    
    # Filter data for the specified teams
    team1_data = data_matches[(data_matches['batting_team'] == team1)]
    team2_data = data_matches[(data_matches['batting_team'] == team2)]

    # Calculate average innings total
    team1_avg_innings1_runs = team1_data[team1_data['innings'] == 1].groupby('match_id')['total_runs'].sum().mean()
    team2_avg_innings1_runs = team2_data[team2_data['innings'] == 1].groupby('match_id')['total_runs'].sum().mean()
    team1_avg_innings2_runs = team1_data[team1_data['innings'] == 2].groupby('match_id')['total_runs'].sum().mean()
    team2_avg_innings2_runs = team2_data[team2_data['innings'] == 2].groupby('match_id')['total_runs'].sum().mean()

    statistics = {
    'Avg Innings 1 Total (head to head)': [int(team1_avg_innings1_runs), int(team2_avg_innings1_runs)],
    'Avg Innings 2 Total (head to head)': [int(team1_avg_innings2_runs), int(team2_avg_innings2_runs)],
    }

    statistics_rows = []

    for stat_name, stat_values in statistics.items():
        statistics_rows.append({team1: f'{stat_values[0]:,}', 'Statistic': stat_name, team2: f'{stat_values[1]:,}'})

    statistics_df = pd.DataFrame(statistics_rows)

    # Combine the two DataFrames vertically
    combined_df = pd.concat([df_performance, statistics_df])

    statistics_html = combined_df.to_html(index=False, classes='table table-striped', border=0, justify='center')


    return statistics_html



def analyze_stadium(stadium_name):
    summary_table = {
        "Total Matches": 0,
        "Toss winning team won": 0,
        "Toss winning team lost": 0,
        "Team batting first won": 0,
        "Team batting first lost": 0,
        "Average score 1st Innings": 0,
        "Average score 2nd Innings": 0,
        "Minimum Runs to Win 1st Innings": float('inf'),
        "Average 4s per Innings": 0,
        "Average 6s per Innings": 0,
        "Highest total chased": 0,
        "Highest total chased by": [],
        "Last 5 toss decisions": [],
        "Last 5 frst innings results": []
    }

    total_runs_1st_innings = 0
    total_runs_2nd_innings = 0
    total_wickets_1st_innings = 0
    total_wickets_2nd_innings = 0
    total_4s_1st_innings = 0
    total_6s_1st_innings = 0
    total_4s_2nd_innings = 0
    total_6s_2nd_innings = 0
    total_1st_innings_matches = 0
    total_2nd_innings_matches = 0
    total_matches = 0

    first_innings_scores_when_losing = []

    last_5_toss_decisions = []
    last_5_first_innings_results = []

    with open("all_match_info_from_yaml.csv", 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if stadium_name.lower() in row['venue'].lower():
                summary_table["Total Matches"] += 1
                toss_decision = row['toss_decision'].lower()
                toss_winner = row['toss_winner'].lower()
                winner = row['winner'].lower()
                first_innings_team = row['1st innings team'].lower()
                second_innings_team = row['2nd innings team'].lower()

                last_5_toss_decisions.append(toss_decision)

                if len(last_5_toss_decisions) > 5:
                    last_5_toss_decisions.pop(0)

                if toss_decision == 'bat':
                    summary_table["Toss Decision - Bat"] = summary_table.get("Toss Decision - Bat", 0) + 1
                elif toss_decision == 'field':
                    summary_table["Toss Decision - Field"] = summary_table.get("Toss Decision - Field", 0) + 1

                if toss_winner == winner:
                    summary_table["Toss winning team won"] += 1
                else:
                    summary_table["Toss winning team lost"] += 1

                if first_innings_team == winner:
                    summary_table["Team batting first won"] += 1
                    last_5_first_innings_results.append("W")
                else:
                    summary_table["Team batting first lost"] += 1
                    last_5_first_innings_results.append("L")

                # Extract runs, wickets, 4s, and 6s from innings scores
                innings_score_1st = row['1st innings score'].split('-')
                innings_score_2nd = row['2nd innings score'].split('-')

                if len(innings_score_1st) == 2:
                    runs_1st = int(innings_score_1st[0])
                    wickets_1st = int(innings_score_1st[1])
                    total_runs_1st_innings += runs_1st
                    total_wickets_1st_innings += wickets_1st
                    total_4s_1st_innings += int(row['Fours_1'])
                    total_6s_1st_innings += int(row['Sixes_1'])
                    total_1st_innings_matches += 1

                    if first_innings_team != winner:
                        first_innings_scores_when_losing.append((runs_1st, second_innings_team))

                    if first_innings_team == winner:
                        summary_table["Minimum Runs to Win 1st Innings"] = min(
                            summary_table["Minimum Runs to Win 1st Innings"], runs_1st
                        )

                if len(innings_score_2nd) == 2:
                    runs_2nd = int(innings_score_2nd[0])
                    total_runs_2nd_innings += runs_2nd
                    # total_wickets += wickets_1st
                    total_matches += 1
                    total_4s_2nd_innings += int(row['Fours_2'])
                    total_6s_2nd_innings += int(row['Sixes_2'])
                    total_2nd_innings_matches += 1

                    if runs_2nd > summary_table["Highest total chased"]:
                        summary_table["Highest total chased"] = runs_2nd
                        summary_table["Highest total chased by"] = second_innings_team.capitalize()+" VS "+first_innings_team.capitalize()

    if total_1st_innings_matches > 0:
        summary_table["Average score 1st Innings"] = total_runs_1st_innings / total_1st_innings_matches
        # summary_table["Average Wickets per Innings"] = (total_wickets_1st_innings+total_wickets_2nd_innings)/(total_1st_innings_matches+total_2nd_innings_matches)

    if total_2nd_innings_matches > 0:
        summary_table["Average score 2nd Innings"] = total_runs_2nd_innings / total_2nd_innings_matches

    if (total_1st_innings_matches + total_2nd_innings_matches) > 0:
        summary_table["Average 4s per Innings"] = (total_4s_1st_innings + total_4s_2nd_innings) / (total_1st_innings_matches + total_2nd_innings_matches)
        summary_table["Average 6s per Innings"] = (total_6s_1st_innings + total_6s_2nd_innings) / (total_1st_innings_matches + total_2nd_innings_matches)

    summary_table["Last 5 toss decisions"] = ", ".join([decision.capitalize() for decision in last_5_toss_decisions])
    summary_table["Last 5 frst innings results"] = ", ".join(last_5_first_innings_results[:5])

    # Create a DataFrame from the summary_table dictionary
    # Create a DataFrame from the summary_table dictionary
    summary_df = pd.DataFrame.from_dict(summary_table, orient='index', columns=["Value"]).reset_index()
    summary_df.rename(columns={"index": "Metric"}, inplace=True)
    pd.options.display.float_format = '{:.0f}'.format

    # Convert DataFrame to HTML
    stad_table = summary_df.to_html(index=False)

    # Add stadium name as a header in the HTML table
    stad_table = stad_table.replace('<table border="1" class="dataframe">',
                                    f'<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th colspan="2" style="text-align: center;font-size: 1.5em">{stadium_name}</th>\n    </tr>\n  </thead>', 1)

    return stad_table


def generate_player_stats(player1, player2):
    # Load the CSV file into a DataFrame
    df = pd.read_csv('all_matches.csv')

    # Filter the DataFrame for the specified players as striker and bowler
    filtered_df = df[(df['striker'] == player1) & (df['bowler'] == player2)]

    print(filtered_df.shape)

    # Calculate the required statistics
    balls_played = filtered_df[filtered_df['wides'].isnull()].shape[0]
    dot_balls = filtered_df[(filtered_df['wides'].isnull()) & (filtered_df['runs_off_bat'] == 0)].shape[0]
    runs_scored = filtered_df['runs_off_bat'].sum()
    runs_scored = filtered_df['runs_off_bat'].sum()
    dismissals = filtered_df[filtered_df['wicket_type'].notnull()].shape[0]
    sixes = filtered_df[filtered_df['runs_off_bat'] == 6].shape[0]
    avg = round((runs_scored / dismissals),1) if dismissals > 0 else "NA"
    strike_rate = round((runs_scored * 100/ balls_played),1)  if balls_played > 0 else 0

    # Create a new DataFrame with the calculated statistics
    stats_df = pd.DataFrame({
        'Balls Played': [balls_played],
        'Dot Balls': [dot_balls],
        'Runs Scored': [runs_scored],
        'Dismissals': [dismissals],
        'No of 6s': [sixes],
        'Strike Rate':[strike_rate],
        'Avg': [avg]
    })

    players_table = stats_df.to_html(index=False)
    return players_table


def generate_team_stats(team1, player2):
    # Load the CSV file into a DataFrame
    df = pd.read_csv('all_matches.csv')

    bowler_batsmen_df = pd.read_csv('data/bowler_and_batsmen.csv')

    # Extract the list of unique bowlers from team1
    unique_bowlers = bowler_batsmen_df[bowler_batsmen_df['bowling_team'] == team1]['bowler'].unique()

    # Initialize an empty list to store individual bowler statistics
    all_bowler_stats = []

    # Iterate through each unique bowler and calculate statistics
    for bowler in unique_bowlers:
        # Filter the DataFrame for the specified team1, player2, and the current bowler
        filtered_df = df[(df['bowler'] == bowler) & (df['striker'] == player2)]

        if not filtered_df.empty:
            # Calculate the required statistics for the current bowler
            balls_played = filtered_df[filtered_df['wides'].isnull()].shape[0]
            dot_balls = filtered_df[(filtered_df['wides'].isnull()) & (filtered_df['runs_off_bat'] == 0)].shape[0]
            runs_scored = filtered_df['runs_off_bat'].sum()
            dismissals = filtered_df[filtered_df['wicket_type'].notnull()].shape[0]
            sixes = filtered_df[filtered_df['runs_off_bat'] == 6].shape[0]
            avg = round((runs_scored) / dismissals, 1) if balls_played > 0 and dismissals > 0 else "NA"
            strike_rate = round((runs_scored * 100) / balls_played,1) if balls_played > 0 else "NA"

            # Create a new DataFrame with the calculated statistics for the current bowler
            bowler_stats = pd.DataFrame({
                'Bowler': [bowler],
                'Balls Played': [balls_played],
                'Dot Balls': [dot_balls],
                'Runs Scored': [runs_scored],
                'Dismissals': [dismissals],
                'No of 6s': [sixes],
                'Strike Rate': [strike_rate],
                'Avg': [avg]
            })

            all_bowler_stats.append(bowler_stats)

    if not all_bowler_stats:
        return "No data available for the specified criteria."

    # Concatenate all bowler statistics into a single DataFrame
    final_stats_df = pd.concat(all_bowler_stats, ignore_index=True)
    final_stats_df = final_stats_df.sort_values(by='Balls Played', ascending=False)

    # Convert the final DataFrame to an HTML table
    players_table = final_stats_df.to_html(index=False)
    return players_table


def find_last_5_scores_for_team(team_name="Chennai Super Kings"):
    # Read the "data/bowler_and_batsmen.csv" file to get bowling and batting data
    data = pd.read_csv("data/bowler_and_batsmen.csv")

    # Filter data for the specified team as the bowling team
    filtered_data = data[data["batting_team"] == team_name]

    # Extract the list of unique strikers from the filtered data
    unique_strikers = filtered_data["striker"].unique()

    last_5_scores_list = []
    runs_list = []
    


    # Loop through unique strikers and calculate their last 5 scores
    for striker in unique_strikers:
        # Read the "your_dataset.csv" file to get individual match data
        individual_match_data = pd.read_csv("all_matches.csv")

        # Filter data for the specific striker
        striker_data = individual_match_data[(individual_match_data["striker"] == striker)]

        # Sort the data by start_date in descending order
        striker_data = striker_data.sort_values(by="start_date", ascending=False)

        # Select the last 5 unique match IDs by date
        last_5_unique_match_ids = (
            striker_data.sort_values(by="start_date", ascending=False)
            .drop_duplicates(subset=["match_id"])
            .head(5)["match_id"]
            .tolist()
        )

        runs_in_last_5_matches = []
        balls = []
        runs_list = []
        out = 0

        # Iterate through the last 5 unique match IDs
        for match_id in last_5_unique_match_ids:
            match_data = striker_data[striker_data["match_id"] == match_id]

            
            

            # Check if the player's name is in the "player_dismissed" column for the match
            if striker in match_data["player_dismissed"].values:
                runs_in_match = match_data["runs_off_bat"].sum()
                runs = match_data["runs_off_bat"].sum()
                out+=1
            else:
                runs_in_match = str(match_data["runs_off_bat"].sum())+"*"
                runs = match_data["runs_off_bat"].sum()

            balls_played = len(match_data[~match_data["wides"].notnull()])
            balls.append(balls_played)

            runs_in_last_5_matches.append(runs)
            runs_list.append(f"  {runs_in_match}({balls_played})")

            

        # Calculate the total runs for the last 5 matches
        
        total_runs = sum(runs_in_last_5_matches)
        total_balls = sum(balls)
        avg = round(total_runs/out,1)
        sr =  round(total_runs*100/total_balls,1)
        no = 5-out
        inngs = len(runs_in_last_5_matches)


        last_5_scores_list.append({"Striker": striker, "Inngs":inngs, "Runs": total_runs,"Balls":total_balls,"Avg":avg,"SR":sr,"NO":no,"Last 5 scores": ', '.join(map(str, runs_list))})

    # Create a DataFrame with the "Total" column
    result_df = pd.DataFrame(last_5_scores_list)
    
    # Sort the DataFrame by "Total" column in descending order
    result_df = result_df.sort_values(by="Runs", ascending=False)
    
    last5 = result_df.to_html(index=False)
    return last5

    
def find_bowler_stats_for_team(team_name="CHennai Super Kings"):
    # Read the "data/bowler_and_batsmen.csv" file to get bowling and batting data
    data = pd.read_csv("data/bowler_and_batsmen.csv")

    # Filter data for the specified team as the bowling team
    filtered_data = data[data["bowling_team"] == team_name]

    # Extract the list of unique bowlers from the filtered data
    unique_bowlers = filtered_data["bowler"].unique()

    bowler_stats_list = []
    

    # Loop through unique bowlers and calculate their stats
    for bowler in unique_bowlers:

        
        # Read the "your_dataset.csv" file to get individual match data
        individual_match_data = pd.read_csv("all_matches.csv")

        # Filter data for the specific bowler
        bowler_data = individual_match_data[(individual_match_data["bowler"] == bowler)]

        # Sort the data by start_date in descending order
        bowler_data = bowler_data.sort_values(by="start_date", ascending=False)

        # Select the last 5 unique match IDs by date
        last_5_unique_match_ids = (
            bowler_data.sort_values(by="start_date", ascending=False)
            .drop_duplicates(subset=["match_id"])
            .head(5)["match_id"]
            .tolist()
        )

        # Initialize variables to calculate total runs and wickets
        total_runs_given = 0
        total_wickets_taken = 0
        individual_stats = []
        total_balls =0

        def convert_balls_to_overs(balls):
            overs = balls // 6
            remaining_balls = balls % 6
            return f"{overs}.{remaining_balls}"

        # Iterate through the last 5 unique match IDs
        for match_id in last_5_unique_match_ids:
            match_data = bowler_data[bowler_data["match_id"] == match_id]

            # Calculate total runs given by the bowler in this match
            runs_off_bat = match_data["runs_off_bat"].sum()
            wides = match_data["wides"].sum()
            noballs = match_data["noballs"].sum()
            total_runs_given += runs_off_bat + wides + noballs

            # Calculate total wickets taken by the bowler in this match
            wickets_taken = match_data[~match_data["player_dismissed"].isnull()]["player_dismissed"].count()
            total_wickets_taken += wickets_taken

            # Calculate the number of balls bowled in this match (excluding wides and no-balls)
            balls_bowled = len(match_data[(match_data["wides"].isnull()) & (match_data["noballs"].isnull())])

            # Convert balls to overs and balls format
            overs_balls = convert_balls_to_overs(balls_bowled)

            # Create a string representation of runs, wickets, and overs/balls for this match
            match_stats_str = f"{runs_off_bat}-{wickets_taken}({overs_balls})"
            individual_stats.append(match_stats_str)

            total_balls =total_balls+balls_bowled

        # Create a string representation of total runs given and total wickets taken
        bowler_stats_str = f"{int(total_runs_given)}-{total_wickets_taken} ({convert_balls_to_overs(total_balls)})"

        avg_economy = round(total_runs_given*6/total_balls,1)

        avg_sr =  int(total_balls/total_wickets_taken) if total_wickets_taken>0 else"NA"



        maches_bowled =  len(individual_stats)

        

        bowler_stats_list.append({"Bowler": bowler, "Inngs":maches_bowled,"Wkts":total_wickets_taken,"Total": bowler_stats_str,"Economy":avg_economy,"SR":avg_sr, "Individual_stats": '  ,  '.join(map(str, individual_stats))})

    # Create a DataFrame for bowler statistics
    result_df = pd.DataFrame(bowler_stats_list)
    result_df = result_df.sort_values(by="Wkts", ascending=False)

    last5 = result_df.to_html(index=False)
    return last5
    