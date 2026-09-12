
import pandas as pd
import os    
import json

# Define the file path
file_path = '/Users/yogesh/Desktop/PERSONAL/PYTHON/Yogesh_ENV/IPL/Raw_data/ipl_csv'


# data_path = 'path_to_your_file.txt'  # Replace with the actual path to your data file
file_list = os.listdir(file_path)
print(len(file_list))
file_list = [filename for filename in file_list if '_info' in filename]
print(len(file_list))

  # Replace with the actual path to your data file
match_dict= {}


for file_path in file_list:
    data_dict = {}
    with open("Raw_data/ipl_csv/"+file_path, 'r') as file:
        for line in file:

            parts = line.strip().split(',')[1:]
            if len(parts) == 2:
                key, value = parts
                if key in ['team','umpire']:
                    if key in data_dict:
                        data_dict[key].append(value)
                    else:
                        data_dict[key] = [value]
                else:
                    data_dict[key] = value
            parts = line.strip().split(',')[2:]
            if len(parts) == 2:
                key, value = parts
                if key in data_dict:
                    data_dict[key].append(value)
                else:
                    data_dict[key] = [value]
    match_id = file_path.split("_")[0]
    match_dict[match_id] = data_dict


# Save the dictionary to a JSON file
with open('all_match_info.json', 'w') as json_file:
    json.dump(match_dict, json_file)

###########################################   2   ###############################################
import pandas as pd

# Define the venue name mapping
venue_mapping = {
    "Arun Jaitley Stadium": "Arun Jaitley Stadium Delhi",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium Delhi",
    "Feroz Shah Kotla": "Arun Jaitley Stadium Delhi",
    "Barabati Stadium": "Barsapara Cricket Stadium Guwahati",
    "Barsapara Cricket Stadium, Guwahati": "Barsapara Cricket Stadium Guwahati",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium Lucknow",
    "Brabourne Stadium": "Brabourne Stadium Mumbai",
    "Brabourne Stadium, Mumbai": "Brabourne Stadium Mumbai",
    "Dr DY Patil Sports Academy": "Dr DY Patil Sports Academy Mumbai",
    "Dr DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy Mumbai",
    "Eden Gardens, Kolkata": "Eden Gardens Kolkata",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala": "Himachal Pradesh Cricket Association Stadium Dharamsala",
    "M Chinnaswamy Stadium": "M Chinnaswamy Stadium Bengaluru",
    "M Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium Bengaluru",
    "M.Chinnaswamy Stadium": "M Chinnaswamy Stadium Bengaluru",
    "MA Chidambaram Stadium": "MA Chidambaram Stadium Chepauk Chennai",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium Chepauk Chennai",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium Chepauk Chennai",
    "Maharashtra Cricket Association Stadium": "Maharashtra Cricket Association Stadium Pune",
    "Maharashtra Cricket Association Stadium, Pune": "Maharashtra Cricket Association Stadium Pune",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium Ahmedabad",
    "Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association IS Bindra Stadium Mohali Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium Mohali Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh": "Punjab Cricket Association IS Bindra Stadium Mohali Chandigarh",
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium Mohali Chandigarh",
    "Rajiv Gandhi International Stadium": "Rajiv Gandhi International Stadium Uppal Hyderabad",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium Uppal Hyderabad",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad": "Rajiv Gandhi International Stadium Uppal Hyderabad",
    "Sardar Patel Stadium, Motera": "Sardar Patel Stadium Motera",
    "Saurashtra Cricket Association Stadium": "Saurashtra Cricket Association Stadium",
    "Sawai Mansingh Stadium": "Sawai Mansingh Stadium Jaipur",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium Jaipur",
    "Vidarbha Cricket Association Stadium, Jamtha": "Vidarbha Cricket Association Stadium Jamtha",
    "Wankhede Stadium": "Wankhede Stadium Mumbai",
    "Wankhede Stadium, Mumbai": "Wankhede Stadium Mumbai",
    "Zayed Cricket Stadium, Abu Dhabi": "Zayed Cricket Stadium Abu Dhabi"
}

# Read the CSV file into a DataFrame
df = pd.read_csv("all_matches.csv")

# Replace the venue names using the mapping
df['venue'] = df['venue'].replace(venue_mapping)

# Save the updated DataFrame to a new CSV file if needed
# df.to_csv("updated_matches.csv", index=False)

# Print the unique venue names with their updated names
for n, venue in enumerate(df['venue'].unique(), 1):
    print(venue, n)


################################  3   ##################################################################
import os
import yaml
import csv

# Define the folder containing YAML files
folder_path = 'ipl_yaml'

# Initialize lists to store the extracted data
data_list = []
fours_list = []  # Store fours count for both innings
sixes_list = []  # Store sixes count for both innings

# Function to extract the winner, by, teams, and venue details
def extract_outcome(outcome_data, teams, venue):
    winner = outcome_data.get('winner', None)
    if winner:
        by_runs = outcome_data['by'].get('runs', None)
        by_wickets = outcome_data['by'].get('wickets', None)
        if by_runs is not None:
            by = f'{by_runs} runs'
        elif by_wickets is not None:
            by = f'{by_wickets} wickets'
        else:
            by = ''
        
        formatted_teams = format_teams(teams)
        return [winner, by, formatted_teams, venue]
    elif 'result' in outcome_data:
        if outcome_data['result'] == 'tie':
            return ['Tie', '', format_teams(teams), venue]
        elif outcome_data['result'] == 'no result':
            return ['No Result', '', format_teams(teams), venue]
    
    return ['', '', format_teams(teams), venue]

# Function to format teams as a string
def format_teams(teams):
    # Reorder teams for consistent formatting
    sorted_teams = sorted(teams)
    return f'{sorted_teams[0]} vs {sorted_teams[1]}'

# Function to calculate the innings score and wickets
def calculate_innings_score(innings_data):
    total_runs = 0
    total_wickets = 0
    fours_count = 0  # Initialize fours count
    sixes_count = 0  # Initialize sixes count
    for delivery in innings_data['deliveries']:
        for ball, ball_data in delivery.items():
            total_runs += ball_data['runs']['total']
            if 'wicket' in ball_data:
                total_wickets += 1
            if 'batsman' in ball_data:
                batsman_runs = ball_data['runs']['batsman']
                if batsman_runs == 4:
                    fours_count += 1
                elif batsman_runs == 6:
                    sixes_count += 1
    return f'{total_runs}-{total_wickets}', fours_count, sixes_count

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".yaml"):
        file_path = os.path.join(folder_path, filename)
        
        # Extract match_id from the filename
        match_id = filename.replace('.yaml', '')
        
        # Read the YAML file
        with open(file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            
            # Convert date to string
            date_str = yaml_data['info']['dates'][0]
            
            # Extract the outcome value
            outcome_data = yaml_data['info']['outcome']
            venue = yaml_data['info']['venue']  # Extract venue
            winner, by, teams, venue = extract_outcome(outcome_data, yaml_data['info']['teams'], venue)
            
            # Extract toss data
            toss_winner = yaml_data['info']['toss']['winner']
            toss_decision = yaml_data['info']['toss']['decision']
            
            # Initialize innings data
            innings1_team = ''
            innings2_team = ''
            innings1_score = ''
            innings2_score = ''
            
            # Initialize fours and sixes count
            fours_1st = 0
            sixes_1st = 0
            fours_2nd = 0
            sixes_2nd = 0
            
            # Check if there are innings data available
            if 'innings' in yaml_data:
                innings1_data = yaml_data['innings'][0]['1st innings']
                innings1_team = innings1_data['team']
                innings1_score, fours_1st, sixes_1st = calculate_innings_score(innings1_data)
                
                if len(yaml_data['innings']) > 1:
                    innings2_data = yaml_data['innings'][1]['2nd innings']
                    innings2_team = innings2_data['team']
                    innings2_score, fours_2nd, sixes_2nd = calculate_innings_score(innings2_data)
            
            # Append the data to the lists
            data_list.append([match_id, date_str, winner, by, teams, venue, toss_winner, toss_decision, innings1_team, innings1_score, innings2_team, innings2_score])
            fours_list.append([fours_1st, fours_2nd])
            sixes_list.append([sixes_1st, sixes_2nd])

# Define the CSV file path for storing the results
csv_file_path = 'outcome_data.csv'

# Write the data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header
    csv_writer.writerow(['match_id', 'date', 'winner', 'by', 'teams', 'venue', 'toss_winner', 'toss_decision', '1st innings team', '1st innings score', '2nd innings team', '2nd innings score'])
    # Write the data and fours/sixes counts
    for i in range(len(data_list)):
        csv_writer.writerow(data_list[i] + fours_list[i] + sixes_list[i])

print(f'Data extracted and saved to {csv_file_path}')

#############################################        4        ###################################################

import pandas as pd


df =  pd.read_csv("all_matches.csv")
print(df.striker.nunique())
print(df.bowler.nunique())


# Create an empty DataFrame with a fixed length
index_length = 638  # Set this to the desired length
DF = pd.DataFrame(index=range(index_length))

# Assign unique values to the "Batsmen" and "Bowler" columns (as you've shown)
batsmen_values = df.striker.unique()
bowler_values = df.bowler.unique()

# Fill the DataFrame with empty strings
DF["Batsmen"] = [""] * index_length
DF["Bowler"] = [""] * index_length

# Assign unique values to the DataFrame based on the length of the unique lists
DF["Batsmen"][:len(batsmen_values)] = batsmen_values
DF["Bowler"][:len(bowler_values)] = bowler_values

# Save the DataFrame to a CSV file
# DF.to_csv("data/bowler_and_batsmen.csv", index=False)


############################################     5    ###################################################