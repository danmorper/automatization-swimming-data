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
df = df[['first_surname', 'second_surname', 'name', 'team', 'race_time', 'gender', 'distance', 'style', 'category', 'date', 'event_time']]
# # Correct format data for each column
# df['first_surname'] = df['first_surname'].str.title()
# df['second_surname'] = df['second_surname'].str.title()
# df['name'] = df['name'].str.title()
# df['team'] = df['team'].str.title()
# df['race_time'] = df['race_time'].str.replace(',', '.')
# Save df as csv
df.to_csv('merged.csv', index=False)


