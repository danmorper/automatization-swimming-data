import datetime
import os
import pandas as pd

# Get list of files in csvs folder
files = os.listdir('csvs')

# List to store dataframes
dfs = []

# Iterate through files
for file in files:
    if file.endswith('.csv'):
        # Read file
        file_path = os.path.join('csvs', file)
        df_temp = pd.read_csv(file_path)
        # Append to list
        dfs.append(df_temp)

# Concatenate all dataframes
df = pd.concat(dfs, ignore_index=True)

# Define columns (if necessary)
df = df[['first_surname', 'second_surname', 'name', 'team', 'race_time', 'gender', 'distance', 'style', 'category', 'date', 'event_time', "Piscina Corta"]]
# Removing digits from the 'team' column
df['team'] = df['team'].str.replace('\d+', '', regex=True)

# export df as csv
df.to_csv('merged.csv', index=False)

# Managing correct data types: 
# Converting data types as per the user's request
df['first_surname'] = df['first_surname'].astype('string')
df['second_surname'] = df['second_surname'].astype('string')
df['name'] = df['name'].astype('string')
df['gender'] = df['gender'].astype('string')
df['category'] = df['category'].astype('string')

# Converting 'distance' to integer. This assumes that all values in 'distance' can be converted to integers.
df['distance'] = pd.to_numeric(df['distance'], errors='coerce').astype('Int64')

# Converting 'race_time' and 'event_time' to time format and 'date' to date format
df['event_time'] = pd.to_datetime(df['event_time'], format='%H:%M:%S', errors='coerce').dt.time
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Race_time
# Aplicando la conversión correcta para 'race_time'
def convert_race_time(time_str):
    """ Convert race time from string to datetime.time, accounting for minutes, seconds, and centiseconds. """
    if ':' in time_str:
        # Format is MM:SS.cc
        minutes, seconds = time_str.split(':')
        seconds, centiseconds = seconds.split('.')
        return datetime.time(minute=int(minutes), second=int(seconds), microsecond=int(centiseconds)*10000)
    else:
        # Format is SS.cc
        seconds, centiseconds = time_str.split('.')
        return datetime.time(second=int(seconds), microsecond=int(centiseconds)*10000)

# Convert 'race_time' to string
df['race_time'] = df['race_time'].astype('string')

# Aplicando la conversión a la columna 'race_time'
df['race_time'] = df['race_time'].apply(convert_race_time)

# Remove rows in which gender is neither 'masc' nor 'fem'
data_cleaned = df[df['gender'].isin(['masc', 'fem'])]

# Be sure that new df is correct
remaining_issues = data_cleaned[~data_cleaned['gender'].isin(['masc', 'fem'])]
# Save df as csv
data_cleaned.to_csv('merged_datatype.csv', index=False)


