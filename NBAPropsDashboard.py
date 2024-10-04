import streamlit as st
import pandas as pd

# Load data
players_df = pd.read_csv('players.csv')
teamdefense_df = pd.read_csv('teamdefense.csv')

# Title of the dashboard
st.title("NBA Prop Picks Dashboard")

# User Input: Select a player
player_name = st.text_input("Type a player's name:")

# Search and store player information
if player_name:
    player_row = players_df[players_df['Name'].str.contains(player_name, case=False, na=False)]
    if not player_row.empty:
        player_position = player_row.iloc[0]['Position'].upper()
        st.write(f"Selected Player: {player_row.iloc[0]['Name']}, Position: {player_position}")
    else:
        st.write("Player not found!")
        player_position = None
else:
    player_position = None

# User Input: Select an opposing team
team_name = st.selectbox("Select the opposing team:", teamdefense_df['Team'].unique())

# User Input: Choose a prop type (Points, Rebounds, Assists)
prop_type = st.selectbox("Select a prop type:", ["Points", "Rebounds", "Assists"])

# Mapping props to the respective column in teamdefense_df based on position
def get_defense_column(position, prop):
    prop = prop.lower()  # Ensure lowercase for matching column names
    if position == 'PG':
        return f'pg_{prop}'
    elif position == 'SG':
        return f'sg_{prop}'
    elif position == 'SF':
        return f'sf_{prop}'
    elif position == 'PF':
        return f'pf_{prop}'
    elif position == 'C':
        return f'c_{prop}'
    return None

# Prop pick logic
def get_pick_suggestion(position, team, prop):
    if not position:
        return "No player selected."
    
    # Get defense rankings for the selected team
    team_row = teamdefense_df[teamdefense_df['Team'] == team]
    
    # Determine the correct column name
    prop_column = get_defense_column(position, prop)
    
    if not team_row.empty and prop_column in team_row.columns:
        ranking = team_row.iloc[0][prop_column]
        
        # Classify based on ranking
        if 1 <= ranking <= 5:
            return 'Under'
        elif 6 <= ranking <= 10:
            return 'Slight Under'
        elif 11 <= ranking <= 20:
            return 'Stay Away'
        elif 21 <= ranking <= 25:
            return 'Slight Over'
        elif 26 <= ranking <= 30:
            return 'Over'
    return "Invalid prop selection."

# Button to make the pick
if st.button("Make Pick"):
    if player_position and team_name and prop_type:
        result = get_pick_suggestion(player_position, team_name, prop_type)
        st.write(f"Pick Suggestion: {result}")
    else:
        st.write("Please select a valid player, team, and prop.")

# --- New Section: Interactive Team Defense Table ---

st.subheader("Team Defense Table")

# Display the interactive table
st.dataframe(teamdefense_df)