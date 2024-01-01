import pandas as pd
import matplotlib.pyplot as plt


def preprocess(path_to_file):

    df = pd.read_csv(path_to_file)
    return df


def total_teams(df):

    teams = df['team1'].unique().tolist()
    return teams


def team_wise(df, team_name, column):

    column = column.lower()
    column_1 = column + ' team1'
    column_2 = column + ' team2'
    df[column_1] = df[column_1].apply(lambda x: int(x))
    df[column_2] = df[column_2].apply(lambda x: int(x))
    # creating team 1 and team 2 variable for storing goals
    team_1 = df[df['team1'] == team_name]
    team_2 = df[df['team2'] == team_name]

    opp_team_scored1 = sum(team_2[column_1].tolist())
    opp_team_scored2 = sum(team_1[column_2].tolist())

    team_1 = sum(team_1[column_1].tolist())
    team_2 = sum(team_2[column_2].tolist())

    total_goals_scored = team_1 + team_2
    total_opposition_scored = opp_team_scored1 + opp_team_scored2

    return total_goals_scored, total_opposition_scored


def pie_chart(df, team_name, column):

    team_score, opp_score = team_wise(df, team_name, column)

    # pie chart

    pie_chart = plt.pie([team_score, opp_score],
                        labels=[f'{team_name}: {team_score}',
                                f'Opposition: {opp_score}'])
    return pie_chart


def football_calc(df, team, variable):

    a = df[variable][df['team1'] == team].sum()
    variable = variable.replace("1", "2")
    b = df[variable][df['team2'] == team].sum()

    return a + b


def match_calc(df, team, variable):

    a = df[variable][df['team1'] == team].count()
    variable = variable.replace("1", "2")
    b = df[variable][df['team2'] == team].count()

    return a + b


def total_calc(df, names, var):

    total_attempts = {}
    for i in names:
        value = football_calc(df, i, var)
        total_attempts[i] = value

    return total_attempts


def total_matches(df, team_names):

    total_matches = {}
    for i in team_names:
        value = match_calc(df, i, 'team1')
        total_matches[i] = value

    return total_matches


def new_dataframe(df, team_names, total_matches):

    total_attempts = total_calc(df, team_names, 'total attempts team1')
    total_assists = total_calc(df, team_names, 'assists team1')
    total_on_target_attempts = total_calc(df,
                                          team_names,
                                          'on target attempts team1')
    total_off_target_attempts = total_calc(df,
                                           team_names,
                                           'off target attempts team1')
    total_off_sides = total_calc(df, team_names, 'offsides team1')
    total_passes_completed = total_calc(df,
                                        team_names,
                                        'passes completed team1')
    total_goal_prevention = total_calc(df,
                                       team_names,
                                       'goal preventions team1')
    total_goals = total_calc(df, team_names, 'number of goals team1')

    new_df = pd.DataFrame(total_attempts.values(),
                          index=total_attempts.keys(),
                          columns=['total attempts'])

    asfs = pd.DataFrame(total_assists.values(),
                        index=total_assists.keys(),
                        columns=['total_assists'])

    otfs = pd.DataFrame(total_on_target_attempts.values(),
                        index=total_on_target_attempts.keys(),
                        columns=['total_on_target_attempts'])

    offs = pd.DataFrame(total_off_target_attempts.values(),
                        index=total_off_target_attempts.keys(),
                        columns=['total_off_target_attempts'])

    osfs = pd.DataFrame(total_off_sides.values(),
                        index=total_off_sides.keys(),
                        columns=['total_off_sides'])

    pcfs = pd.DataFrame(total_passes_completed.values(),
                        index=total_passes_completed.keys(),
                        columns=['total_passes_completed'])

    gpfs = pd.DataFrame(total_goal_prevention.values(),
                        index=total_goal_prevention.keys(),
                        columns=['total_goal_prevention'])

    gofs = pd.DataFrame(total_goals.values(),
                        index=total_goals.keys(),
                        columns=['total_goals'])

    total_match = pd.DataFrame(total_matches.values(),
                               index=total_matches.keys(),
                               columns=['total_matches_played'])

    a_list = [asfs, otfs, pcfs, gpfs, offs, osfs, gofs, total_match]
    for i in a_list:
        new_df = new_df.merge(right=i, right_index=True, left_index=True)

    columns = new_df.columns.tolist()
    del columns[-1]
    del columns[-1]

    return new_df, columns


def data_analyser(dataframe, column, matches):

    a = []
    for i in range(len(dataframe)):
        a.append(dataframe[column].iloc[i]/(dataframe[matches].iloc[i]))
    return a


def rank_data(dataframe, columns, matches):

    rank_df = pd.DataFrame(index=dataframe.index)
    for column in columns:
        b = column.replace("total", "Average")
        rank_df[b] = data_analyser(dataframe, column, matches)

    rank_df = rank_df.drop(rank_df.columns[-1], axis=1)
    return rank_df


def rank_calc(dataframe, team):

    rank_list = []
    a = dataframe.columns.tolist()
    descending, ascending = a[:-2], a[-2:]

    for i in range(len(descending)):
        dataframe.sort_values(by=descending[i], ascending=False, inplace=True)
        value = dataframe.index.get_loc(team)
        rank_list.append(f"#{value+1}")

    for i in range(len(ascending)):
        dataframe.sort_values(by=ascending[i], inplace=True)
        value = dataframe.index.get_loc(team)
        rank_list.append(f"#{value+1}")

    return rank_list


def display_rank(dataframe, team):

    column_names = dataframe.columns.tolist()
    rankings = {'Basis': column_names, 'Ranking': rank_calc(dataframe, team)}

    return pd.DataFrame(rankings)
