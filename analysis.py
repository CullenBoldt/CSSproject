import pandas as pd
# data cleaning and tallying of relationships

def list_to_tuples(input_list1, input_list2):
    """Gives the cartesian product in a list of tuples from two lists

        Args:
            input_list1 (list): list of subreddits
            input_list2 (list): list of subreddits

        Returns:
            list: a list of tuples.

        """
    output = []
    for i in input_list1:
        for j in input_list2:
            output.append((i, j))
    return output


if __name__ == '__main__':

    # Loading comment data and unique user statistics
    # these are .csv files were exported from google BigQuery. Please see the queries in the github repository
    comments = pd.read_csv('comments.csv')
    unique_users = pd.read_csv('unique_users.csv')
    unique_users = unique_users.set_index('subreddit')
    mental_health_subs = ['Anxiety', 'SanctionedSuicide', 'SuicideWatch', 'addiction', 'depression','mentalhealth']

    #dictionary containing all the location subreddits for each state
    states = {}
    states['Maine'] = ["Maine"]
    states['Vermont'] = ['vermont']
    states['New Hampshire'] = ['newhampshire']
    states['Maryland'] = ['baltimore', 'maryland']
    states['New York'] = ['nyc', 'newyork', 'Buffalo']
    states['New Jersey'] = ['newjersey', 'Newark', 'jerseycity']
    states['Massachusetts'] = ['massachusetts', 'boston', 'WorcesterMA']
    states['Pennsylvania'] = ['pittsburgh', 'philadelphia']
    states['Connecticut'] = ['newhaven', 'Connecticut']
    states['Rhode Island'] = ['providence', 'RhodeIsland']
    states['Delaware'] = ['Delaware', 'WilmingtonDE']
    states['Virginia'] = ['Virginia', 'VirginiaBeach', 'norfolk']
    states['West Virginia'] = ['WestVirginia']
    states['Ohio'] = ['Ohio', 'Cleveland', 'Columbus', 'cincinnati']
    states['Kentucky'] = ['Louisville', 'Kentucky', 'lexington']
    states['Indiana'] = ['Indiana', 'indianapolis', 'bloomington']
    states['Michigan'] = ['Michigan', 'Detroit', 'lansing']
    states['North Carolina'] = ['NorthCarolina', 'Charlotte', 'raleigh']
    states['Tennessee'] = ['Tennessee', 'Knoxville', 'Chattanooga']
    states['South Carolina'] = ['Charleston', 'southcarolina', 'ColumbiYEAH']
    states['Georgia'] = ['Atlanta', 'Georgia', 'Augusta']
    states['Florida'] = ['florida', 'Miami', 'orlando', 'tampa', 'jacksonville']
    states['Alabama'] = ['Alabama', 'Birmingham', 'HuntsvilleAlabama']
    states['Mississippi'] = ['mississippi']
    states['Illinois'] = ['chicago', 'illinois', 'SpringfieldIL']
    states['Wisconsin'] = ['wisconsin', 'madisonwi', 'milwaukee']
    states['Iowa'] = ['Iowa', 'desmoines', 'ames']
    states['Missouri'] = ['missouri', 'springfieldMO', 'StLouis', 'kansascity']
    states['Arkansas'] = ['Arkansas', 'LittleRock', 'fayetteville']
    states['Louisiana'] = ['Louisiana', 'NewOrleans', 'batonrouge', 'shreveport']
    states['Minnesota'] = ['minnesota', 'saintpaul', 'Minneapolis', 'duluth']
    states['North Dakota'] = ['northdakota']
    states['South Dakota'] = ['SouthDakota']
    states['Nebraska'] = ['Omaha', 'Nebraska', 'lincoln']
    states['Kansas'] = ['wichita', 'kansas', 'Lawrence']
    states['Oklahoma'] = ['oklahoma', 'okc', 'tulsa']
    states['Texas'] = ['sanantonio', 'houston', 'Dallas']
    states['New Mexico'] = ['NewMexico', 'SantaFe', 'Albuquerque']
    states['Colorado'] = ['Colorado', 'Denver', 'ColoradoSprings']
    states['Wyoming'] = ['wyoming']
    states['Montana'] = ['Montana']
    states['Arizona'] = ['arizona', 'phoenix', 'Tucson']
    states['Utah'] = ['SaltLakeCity', 'Utah']
    states['Idaho'] = ['Idaho', 'Boise']
    states['Washington'] = ['Washington','Seattle', 'Spokane']
    states['Oregon'] = ['oregon', 'Portland', 'Eugene']
    states['Nevada'] = ['Nevada', 'LasVegas', 'vegas', 'Reno']
    states['California'] = ['California', 'LosAngeles', 'sanfrancisco', 'sandiego', 'Sacramento']

    # make a list of all the specific subreddit cities
    cities = []
    for i in states.values():
        cities += i

    # create a data frame to tall the weights for each subreddit
    scores = pd.DataFrame(columns = mental_health_subs)
    scores['city'] = cities
    scores = scores.set_index('city')
    scores[:] = 0.0

    # combine the weights from each city and mental health subreddit into a weighted average score for each state.
    state_averages = pd.DataFrame(columns = mental_health_subs)
    state_averages['State'] = list(states.keys())
    state_averages = state_averages.set_index('State')
    state_averages[:] = 0.0


    # Tally scores for each unique user
    x = len(list(comments.author.unique()))
    for i in list(comments.author.unique()):
        each_edges = list_to_tuples([i for i in list(comments.loc[comments['author'] == i]['subreddit'].unique()) if i in mental_health_subs], [i for i in list(comments.loc[comments['author'] == i]['subreddit'].unique()) if i in cities])
        for l in each_edges:
            scores[l[0]][l[1]] += 1
        x -= 1
        if x % 100 == 0:
            print(str(x) + ' users remaining')


    # sum scores from each city at a state level and adjust by unique users for those subs
    # this represents what percentage of the unique users are participating in these subreddits
    for i in mental_health_subs:
        for j in list(states.keys()):
            sum_scores = 0
            sum_unique = 0
            for k in list(states[j]):
                sum_scores += scores[i][k]
                sum_unique += unique_users['unique_users'][k]
            state_averages[i][j] = (sum_scores/sum_unique)


    # Calculate the total sum score for each state
    state_averages['total_combined'] = 0
    for i in list(states.keys()):
        sum_total_score = 0
        for j in mental_health_subs:
            sum_city = 0
            for k in list(states[i]):
                sum_city += scores[j][k]
            sum_total_score += sum_city
        state_averages['total_combined'][i] = sum_total_score


    # Calculate the total number of unique users in all states
    state_averages['total_unique'] = 0
    for i in list(states.keys()):
        sum_unique_state = 0
        for j in list(states[i]):
            sum_unique_state += unique_users['unique_users'][j]
        state_averages['total_unique'][i] = sum_unique_state

    # Calculate total average participation
    state_averages['total_average'] = state_averages['total_combined'] / state_averages['total_unique']



    # WITHOUT SUICIDE
    # Calculate the total sum score for each state
    mental_health_subs_no_suicide = ['Anxiety', 'addiction', 'depression', 'mentalhealth']
    state_averages['total_combined_no_suicide'] = 0
    for i in list(states.keys()):
        sum_total_score = 0
        for j in mental_health_subs_no_suicide:
            sum_city = 0
            for k in list(states[i]):
                sum_city += scores[j][k]
            sum_total_score += sum_city
        state_averages['total_combined_no_suicide'][i] = sum_total_score


    # Calculate the total number of unique users in all states
    state_averages['total_unique_no_suicide'] = 0
    for i in list(states.keys()):
        sum_unique_state = 0
        for j in list(states[i]):
            sum_unique_state += unique_users['unique_users'][j]
        state_averages['total_unique_no_suicide'][i] = sum_unique_state

    # Calculate total average participation
    state_averages['total_average_no_suicide'] = state_averages['total_combined_no_suicide'] / state_averages['total_unique_no_suicide']


    # ONLY SUICIDE
    # Calculate the total sum score for each state
    mental_health_subs_only_suicide = ['SanctionedSuicide', 'SuicideWatch']
    state_averages['total_combined_suicide'] = 0
    for i in list(states.keys()):
        sum_total_score = 0
        for j in mental_health_subs_only_suicide:
            sum_city = 0
            for k in list(states[i]):
                sum_city += scores[j][k]
            sum_total_score += sum_city
        state_averages['total_combined_suicide'][i] = sum_total_score


    # Calculate the total number of unique users in all states
    state_averages['total_unique_suicide'] = 0
    for i in list(states.keys()):
        sum_unique_state = 0
        for j in list(states[i]):
            sum_unique_state += unique_users['unique_users'][j]
        state_averages['total_unique_suicide'][i] = sum_unique_state

    # Calculate total average participation
    state_averages['total_average_suicide'] = state_averages['total_combined_suicide'] / state_averages['total_unique_suicide']

    # Export output to csv
    state_averages.to_csv('state_averages.csv')

