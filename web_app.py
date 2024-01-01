import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import data_analysis

df = data_analysis.preprocess('Fifa_world_cup_matches.csv')
team_names = data_analysis.total_teams(df)

user_menu = st.sidebar.radio(
    'Select an option',
    ('Full Dataset', 'Team wise Pie Chart', 'Team wise Rankings')
)

if user_menu == 'Full Dataset':

    st.dataframe(df)

if user_menu == 'Team wise Pie Chart':

    selected_country = st.sidebar.selectbox('Select Country',
                                            team_names)
    columns = ['Number of goals',
               'Goal preventions',
               'Forced turnovers',
               'Defensive Pressures applied']
    selected_basis = st.sidebar.selectbox('Choose the basis of Analysis',
                                          columns)
    st.title(selected_basis)
    fig = plt.figure(figsize=(12, 8))
    data_analysis.pie_chart(df, selected_country, selected_basis)
    st.pyplot(fig)


if user_menu == 'Team wise Rankings':

    total_matches = data_analysis.total_matches(df, team_names)
    new_df, columns = data_analysis.new_dataframe(df,
                                                  team_names,
                                                  total_matches)
    rank_df = data_analysis.rank_data(new_df, columns, 'total_matches_played')

    selected_country = st.sidebar.selectbox('Select a Country',
                                            team_names)

    rank_list = data_analysis.display_rank(rank_df, selected_country)
    st.title(selected_country)
    st.dataframe(rank_list)
