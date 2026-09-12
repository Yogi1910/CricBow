# import json
# from collections import Counter

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Initialize a Counter to keep track of Player of the Match awards
# player_award_counter = Counter()

# # Iterate through the matches and count Player of the Match awards
# for match_id, match_data in data.items():
#     player_of_match = match_data.get("player_of_match")
#     if player_of_match:
#         player_award_counter[player_of_match] += 1

# # Get the top 10 players with most Player of the Match awards
# top_players = player_award_counter.most_common(50)

# # Print the results
# print("Top 10 Players of the Match:")
# for player, count in top_players:
#     print(f"{player},{count}")


# import json
# from collections import Counter

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Initialize a Counter to keep track of team appearances
# team_appearance_counter = Counter()

# # Iterate through the matches and count team appearances
# for match_data in data.values():
#     teams = match_data.get("team")
#     if teams and len(teams) == 2:
#         for team in teams:
#             team_appearance_counter[team] += 1

# # Get the top 5 teams with the most appearances
# top_teams = team_appearance_counter.most_common()

# # Print the result
# print("Top 5 teams with the most appearances:")
# for team, appearances in top_teams:
#     print(f"{team},{appearances}")


# import json

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Create a list to store match data with winner runs
# matches_with_runs = []

# # Iterate through the matches and extract winner runs and opposing team
# for match_id, match_data in data.items():
#     winner = match_data.get("winner")
#     winner_runs = match_data.get("winner_runs")
#     opposing_teams = [team for team in match_data.get("team") if team != winner]
    
#     if winner and winner_runs is not None:
#         for opposing_team in opposing_teams:
#             matches_with_runs.append((winner, int(winner_runs), opposing_team))

# # Sort the matches by winner runs in descending order
# matches_with_runs.sort(key=lambda x: x[1], reverse=True)

# # Get the top 10 victories by winner runs
# top_victories = matches_with_runs[:10]

# # Print the result
# print("Top 10 victories by winner runs:")
# for idx,(winning_team, runs, opposing_team) in enumerate(top_victories, start=1):
#     print(f"{winning_team} vs {opposing_team}, {runs}")






# import json
# from collections import Counter

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Initialize a Counter to keep track of umpire appearances
# umpire_appearance_counter = Counter()

# # Iterate through the matches and count umpire appearances
# for match_data in data.values():
#     umpires = match_data.get("umpire")
#     if umpires:
#         for umpire in umpires:
#             umpire_appearance_counter[umpire] += 1

# # Get the top 5 umpires with the most appearances
# top_umpires = umpire_appearance_counter.most_common(20)

# # Print the result
# print("Top 5 umpires with the most matches officiated:")
# for umpire, appearances in top_umpires:
#     print(f"{umpire},{appearances}")




# import json
# from collections import Counter
# from itertools import combinations

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Initialize a Counter to keep track of team combinations
# team_combination_counter = Counter()

# # Iterate through the matches and count team combinations
# for match_data in data.values():
#     teams = match_data.get("team")
#     if teams and len(teams) == 2:
#         team_combination = tuple(sorted(teams))  # Sort teams to ensure consistency
#         team_combination_counter[team_combination] += 1

# # Get the top 5 team combinations that have played against each other the most
# top_combinations = team_combination_counter.most_common(30)

# # Print the result
# print("Top 5 team combinations that have played against each other the most:")
# for teams, count in top_combinations:
#     team1, team2 = teams
#     print(f"{team1} vs {team2}, {count}")



# import json
# from collections import defaultdict

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Create a dictionary to store season-wise toss_decision composition
# season_toss_decision = defaultdict(lambda: {'field': 0, 'bat': 0})

# # Iterate through the matches and count toss_decision composition
# for match_data in data.values():
#     season = match_data.get("season")
#     toss_decision = match_data.get("toss_decision")

#     if season and toss_decision:
#         season_toss_decision[season][toss_decision] += 1

# # Print the result
# print("Season-wise toss decision composition:")
# for season, decisions in season_toss_decision.items():
#     total_matches = decisions['field'] + decisions['bat']
#     field_percent = (decisions['field'] / total_matches) * 100
#     bat_percent = (decisions['bat'] / total_matches) * 100
#     print(f"Season {season}: Field {field_percent:.2f}%, Bat {bat_percent:.2f}%")



# import json
# from collections import defaultdict

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Create a dictionary to store team-wise toss statistics
# team_toss_stats = defaultdict(lambda: {'total_matches': 0, 'toss_wins': 0})

# # Iterate through the matches and count toss statistics
# for match_data in data.values():
#     teams = match_data.get("team")
#     toss_winner = match_data.get("toss_winner")

#     if teams and toss_winner:
#         for team in teams:
#             team_toss_stats[team]['total_matches'] += 1
#             if team == toss_winner:
#                 team_toss_stats[team]['toss_wins'] += 1

# # Calculate the toss win percentage for each team
# team_toss_percentages = {}
# for team, stats in team_toss_stats.items():
#     total_matches = stats['total_matches']
#     toss_wins = stats['toss_wins']
#     toss_percentage = (toss_wins / total_matches) * 100
#     team_toss_percentages[team] = toss_percentage

# # Get the top 5 teams with the highest toss win percentages
# top_teams = sorted(team_toss_percentages.items(), key=lambda x: x[1], reverse=True)[:5]

# # Print the result
# print("Top 5 teams with the highest toss win percentages:")
# for team, percentage in top_teams:
#     print(f"{team}: {percentage:.2f}%")


# import json

# # Load JSON data from a file
# with open('all_match_info.json', 'r') as file:
#     data = json.load(file)

# # Create a dictionary to store team-wise match and win counts
# team_match_counts = {}
# team_win_counts = {}

# # Count matches and wins for each team
# for match_data in data.values():
#     teams = match_data.get("team")
#     winner = match_data.get("winner")
    
#     for team in teams:
#         if team not in team_match_counts:
#             team_match_counts[team] = 0
#         team_match_counts[team] += 1
        
#         if winner == team:
#             if team not in team_win_counts:
#                 team_win_counts[team] = 0
#             team_win_counts[team] += 1

# # Calculate the win percentage for each team
# team_win_percentages = {}
# for team, wins in team_win_counts.items():
#     total_matches = team_match_counts.get(team, 0)
#     win_percentage = (wins / total_matches) * 100 if total_matches > 0 else 0
#     team_win_percentages[team] = (win_percentage, total_matches)

# # Sort teams based on win percentage
# sorted_teams = sorted(team_win_percentages.keys(), key=lambda team: team_win_percentages[team][0], reverse=True)

# # Print the result
# print("Teams sorted by win percentage:")
# for idx, team in enumerate(sorted_teams, start=1):
#     win_percentage, total_matches = team_win_percentages[team]
#     print(f"{team} ,{win_percentage:.1f}%, {total_matches}")
