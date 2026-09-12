from flask import Flask, render_template, request,jsonify,send_from_directory
import time ,os
import pandas as pd
from bs4 import BeautifulSoup


from data_preparation import batsmen_statistics_to_html, bowler_statistics_to_html,html_runs_balls_per_match, png_runs_scored_per_season
from data_preparation import plot_runs_and_strike_rate_curve,plot_dismissals_and_balls_faced_dual_axis
from data_preparation import plot_metrics_balls_per_bar_chart, plot_dismissal_types_bar, plot_average_runs_by_stadium
from data_preparation import plot_average_runs_against_teams,generate_player_bowler_plots
from data_preparation import generate_average_scores_curves, generate_dismissals_per_period, generate_boxplot_per_season
from data_preparation import plot_runs_warm,plot_boundaries_for_player, generate_average_total_runs_per_inning


from fantasy import calculate_teams_statistics, analyze_stadium, generate_player_stats,find_last_5_scores_for_team, find_bowler_stats_for_team,generate_team_stats

from ipl import get_top_players, get_players_df_with_most_teams

from team import generate_top_players_table, get_players_df_with_most_seasons_for_team, get_top_players_for_team


app = Flask(__name__)



@app.route('/')
def home(): 
    return render_template('base.html')

player_data = pd.read_csv("data/all_players.csv")
@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    input_text = request.args.get('input_text', '')
    
    # Search for player names that match the input_text
    matched_players = [player for player in player_data['player_name'] if input_text.lower() in player.lower()]
    response = jsonify({'suggestions': matched_players})
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return jsonify({'suggestions': matched_players})

@app.route('/player', methods=['GET', 'POST'])  
def player():
    start_time = time.time()

    player_name = request.args.get('name', 'V Kohli')  # Default to "V Kohli" if not provided
    
    html_table = batsmen_statistics_to_html(player_name)
    html_table1 = bowler_statistics_to_html(player_name)
    graph_html = html_runs_balls_per_match(player_name)
    png_runs_scored_per_season(player_name)
    plot_runs_and_strike_rate_curve(player_name)
    plot_dismissals_and_balls_faced_dual_axis(player_name)
    plot_metrics_balls_per_bar_chart(player_name)
    plot_dismissal_types_bar(player_name)
    plot_average_runs_by_stadium(player_name)
    plot_average_runs_against_teams(player_name)
    generate_player_bowler_plots(player_name)
    plot_runs_warm(player_name)
    plot_boundaries_for_player(player_name)

    player_data = pd.read_csv('data/all_players.csv')

    # Find the player's information by filtering the DataFrame based on player_name
    player_info = player_data[player_data['player'] == player_name]

    
        # Extract the relevant information
    country = player_info['country'].values[0]
    ipl_team = player_info['ipl_team'].values[0]
    batting_style = player_info['batting_style'].values[0]
    age = player_info['age'].values[0]
    debut = player_info['debut'].values[0]
    
    

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Player route took {elapsed_time:.2f} seconds to execute")
    return render_template('player.html', player_name=player_name, html_table=html_table, graph_html=graph_html,html_table1=html_table1,
                           country=country, ipl_team=ipl_team, batting_style=batting_style, age=age, debut=debut)



@app.route('/team', methods=['GET', 'POST'])
def team():
    team_name = request.args.get('team_name','Chennai Super Kings')
    print(team_name)
    html1 = generate_top_players_table(team_name)  # Implement this function
    generate_average_total_runs_per_inning(team_name)
    generate_average_scores_curves(team_name)
    generate_dismissals_per_period(team_name)
    generate_boxplot_per_season(team_name)
    html2 = get_top_players_for_team(team_name)
    html3 = get_players_df_with_most_seasons_for_team(team_name)
    return render_template('team.html', html1=html1,team_name=team_name,html2=html2,html3=html3)






@app.route('/ipl')
def ipl():

    most_matches = get_top_players()  
    most_teams = get_players_df_with_most_teams()

    return render_template('ipl.html',most_matches=most_matches,most_teams=most_teams)


@app.route('/run-team-player-function', methods=['POST'])
def run_team_player_function():
    team1 = request.form['team1']
    player2 = request.form['player2']
    
    result = generate_team_stats(team1, player2)
    
    return result


@app.route('/run-function', methods=['POST'])
def run_function():
    bowler = request.form.get('bowler')
    striker = request.form.get('striker')
    # Run your Python function here with the selected bowler and striker
    players_table = generate_player_stats(striker, bowler)
    return players_table

########################################################################################

@app.route('/fantasy', methods=['GET', 'POST'])
def fantasy():
    team1 = request.form.get('team1', "Royal Challengers Bangalore")
    team2 = request.form.get('team2', "Mumbai Indians")
    selectedTeam3 = request.form.get('team3', "Chennai Super Kings")
    selectedTeam4 = request.form.get('team4', "Chennai Super Kings")

    data = pd.read_csv('data/bowler_and_batsmen.csv')
    bowlers = data['bowler'].dropna().unique().tolist()
    strikers = data['striker'].dropna().unique().tolist()

    
    teams = data['bowling_team'].dropna().unique().tolist()
    players = data['striker'].dropna().unique().tolist()

    teams.sort()
    players.sort()

    # Sort the lists alphabetically
    bowlers.sort()
    strikers.sort()

    # Replace the following lines with your actual functions
    statistics_html = calculate_teams_statistics(team1, team2)

    stadium_name = request.args.get('stadium', "Arun Jaitley Stadium")

    analysis_table = analyze_stadium(stadium_name)

    batsman_last5 = find_last_5_scores_for_team(selectedTeam3)

    bowler_last5 = find_bowler_stats_for_team(selectedTeam4)

    return render_template('fantasy.html', team1=team1, team2=team2,selectedTeam3=selectedTeam3,
                        statistics_html=statistics_html,
                        analysis_table=analysis_table, stadium_name=stadium_name,batsman_last5=batsman_last5,bowler_last5=bowler_last5,
                        bowlers=bowlers,strikers=strikers,teams=teams,players=players)





@app.route('/update_statistics', methods=['POST'])
def update_statistics():
    selectedTeam3 = request.form.get('team3', "Chennai Super Kings")
    batsman_last5 = find_last_5_scores_for_team(selectedTeam3)

    return batsman_last5


@app.route('/update_statistics_bowler', methods=['POST'])
def update_statistics_bowler():
    selectedTeam4 = request.form.get('team4', "Chennai Super Kings")
    bowler_last5 = find_bowler_stats_for_team(selectedTeam4)

    return bowler_last5



# Handle other cases or return an error message as needed

@app.route('/update-summary')
def update_summary():
    # Get the value of the 'stadium' query parameter from the request URL
    stadium_name = request.args.get('stadium', "Arun Jaitley Stadium")
    
    # Call the analyze_stadium function with the specified stadium name
    analysis_table = analyze_stadium(stadium_name)
    
    # Return a JSON response containing the analysis summary
    return analysis_table





################################################################################################################################################################################


@app.route('/data/<path:filename>')
def serve_file(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'data'), filename)


@app.route('/records')
def records():

    most_runs = pd.read_csv('static/records_data/most_runs.csv')  # Load the CSV data
    most_runs_html = most_runs.to_html(classes='table table-striped')

    highest_scores = pd.read_csv('static/records_data/highest_scores.csv')  # Load the CSV data
    highest_scores_html = highest_scores.to_html(classes='table table-striped')

    fastest_fifty = pd.read_csv('static/records_data/fastest_fifty.csv')  # Load the CSV data
    fastest_fifty_html = fastest_fifty.to_html(classes='table table-striped')

    most_hundreds = pd.read_csv('static/records_data/most_hundreds.csv')  # Load the CSV data
    most_hundreds_html = most_hundreds.to_html(classes='table table-striped')   

    most_sixes = pd.read_csv('static/records_data/most_sixes.csv')  # Load the CSV data
    most_sixes_html = most_sixes.to_html(classes='table table-striped')

    most_fours = pd.read_csv('static/records_data/most_fours.csv')  # Load the CSV data
    most_fours_html = most_fours.to_html(classes='table table-striped')

    most_wickets = pd.read_csv('static/records_data/most_wickets.csv')  # Load the CSV data
    most_wickets_html = most_wickets.to_html(classes='table table-striped')

    best_figures = pd.read_csv('static/records_data/best_figures.csv')  # Load the CSV data
    best_figures_html = best_figures.to_html(classes='table table-striped')

    best_bowling_averages = pd.read_csv('static/records_data/best_bowling_average.csv')  # Load the CSV data
    best_bowling_averages_html = best_bowling_averages.to_html(classes='table table-striped')

    best_bowling_sr = pd.read_csv('static/records_data/best_bowling_sr.csv')  # Load the CSV data
    best_bowling_sr_html = best_bowling_sr.to_html(classes='table table-striped')

    best_bowling_economy = pd.read_csv('static/records_data/best_bowling_economy.csv')  # Load the CSV data
    best_bowling_economy_html = best_bowling_economy.to_html(classes='table table-striped')

    four_plus_wickets = pd.read_csv('static/records_data/four_plus_wickets.csv')
    four_plus_wickets.index = range(1, len(four_plus_wickets) + 1)
      # Load the CSV data
    four_plus_wickets_html = four_plus_wickets.to_html(classes='table table-striped')

    hat_tricks = pd.read_csv('static/records_data/hat_tricks.csv') 
    hat_tricks.index = hat_tricks.index + 1 # Load the CSV data
    hat_tricks_html = hat_tricks.to_html(classes='table table-striped')

    highest_innings_totals = pd.read_csv('static/records_data/highest_innings_total.csv')  # Load the CSV data
    highest_innings_totals_html = highest_innings_totals.to_html(classes='table table-striped')

    most_matches_teams =  pd.read_csv('static/records_data/most_no_of_matches_teams.csv')
    most_matches_teams_html = most_matches_teams.to_html(classes='table table-striped')

    most_head_to_head =  pd.read_csv('static/records_data/most_head_to_head.csv')
    most_head_to_head_html = most_head_to_head.to_html(classes='table table-striped')

    biggest_victories =  pd.read_csv('static/records_data/biggest_victories.csv')
    biggest_victories_html = biggest_victories.to_html(classes='table table-striped')

    best_win_per =  pd.read_csv('static/records_data/best_win_per_teams.csv')
    best_win_per_html = best_win_per.to_html(classes='table table-striped')

    most_stumped =  pd.read_csv('static/records_data/most_stumped.csv')
    most_stumped_html = most_stumped.to_html(classes='table table-striped')

    most_catches =  pd.read_csv('static/records_data/most_catches.csv')
    most_catches_html = most_catches.to_html(classes='table table-striped')

    most_stumping =  pd.read_csv('static/records_data/most_stumping_done.csv')
    most_stumping_html = most_stumping.to_html(classes='table table-striped')

    
    most_run_out =  pd.read_csv('static/records_data/most_run_out.csv')
    most_run_out_html = most_run_out.to_html(classes='table table-striped')



    
    return render_template('records.html',fastest_fifty_html=fastest_fifty_html,highest_scores_html=highest_scores_html,
                           most_fours_html=most_fours_html,most_hundreds_html=most_hundreds_html,
                           most_runs_html=most_runs_html,most_sixes_html=most_sixes_html,
                           most_wickets_html = most_wickets_html,best_figures_html=best_figures_html,
                           best_bowling_averages_html=best_bowling_averages_html,best_bowling_sr_html=best_bowling_sr_html,
                           best_bowling_economy_html=best_bowling_economy_html,four_plus_wickets_html=four_plus_wickets_html,
                           hat_tricks_html=hat_tricks_html,
                           highest_innings_totals_html=highest_innings_totals_html,most_matches_teams_html=most_matches_teams_html,
                           most_head_to_head_html=most_head_to_head_html,biggest_victories_html=biggest_victories_html,
                           best_win_per_html=best_win_per_html,most_catches_html=most_catches_html,most_stumped_html=most_stumped_html,
                           most_stumping_html=most_stumping_html,most_run_out_html=most_run_out_html)


def load_articles_from_directory(directory_path):
    articles = []
    for filename in os.listdir(directory_path):
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                # Extract the title from the HTML content
                soup = BeautifulSoup(content, 'html.parser')
                title_element = soup.title

                # Extract the summary
                summary_div = soup.find('div', class_='article-summary')
                if summary_div:
                    summary_paragraph = summary_div.find('p')
                    if summary_paragraph:
                        summary = summary_paragraph.get_text()

                title = title_element.text if title_element else "Title Not Found"
                image =  filename.split(".")[0]+ ".jpeg" # Extract the title element's text or provide a default value
                # Add the new article to the list
                articles.append({'id': len(articles) + 1, 'title': title, 'content': content,'summary':summary,"image":image})
    return articles

@app.route('/articles/<int:article_id>')
def articles(article_id):
    # Load articles from the directory within the articles route handler
    articles_data = load_articles_from_directory('templates/articles')

    # Find the article with the matching article_id
    article = next((article_data for article_data in articles_data if article_data['id'] == article_id), None)

    if article:
        # Render the 'article.html' template with the 'article' variable
        return render_template('article.html', article=article)
    else:
        # Handle the case where the article is not found (e.g., display an error message)
        return "Article not found", 404

    
def load_news_from_directory(directory_path):
    news_articles = []
    for filename in os.listdir(directory_path):
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
            content = file.read()
            # Extract the title from the HTML content
            soup = BeautifulSoup(content, 'html.parser')
            title_element = soup.title

            # Extract the summary
            summary_div = soup.find('div', class_='news-summary')
            if summary_div:
                summary_paragraph = summary_div.find('p')
                if summary_paragraph:
                    summary = summary_paragraph.get_text()

            title = title_element.text if title_element else "Title Not Found"
            image = filename.split(".")[0] + ".jpeg"  # Extract the title element's text or provide a default value
            # Add the new news article to the list
            news_articles.append({'id': len(news_articles) + 1, 'title': title, 'content': content, 'summary': summary, "image": image})
    return news_articles

@app.route('/news/<int:news_id>')
def news_article(news_id):
    # Load news articles from the directory within the news_article route handler
    news_articles_data = load_news_from_directory('templates/news')

    # Find the news article with the matching news_id
    news_article = next((article_data for article_data in news_articles_data if article_data['id'] == news_id), None)

    if news_article:
        # Render a template with the news article content
        return render_template('news_article.html', news_article=news_article)
    else:
        # Handle the case where the news article is not found (e.g., display an error message)
        return "News article not found", 404


@app.route('/news')
def news():
    # Load articles from the directory when rendering the 'news.html' template
    articles_data = load_articles_from_directory('templates/articles')
    news_articles_data = load_news_from_directory('templates/news')
    return render_template('news.html', articles=articles_data,news_articles=news_articles_data)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Replace 5001 with your desired port number

