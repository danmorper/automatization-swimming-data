import tabula
import pandas as pd
from datetime import datetime as dt
import csv
import re

# Define a function that checks if a string starts with an integer followed by a point, a whitespace, and then a letter
def check_string_format(s):
    # Regular expression pattern to match the specific format
    pattern = r"^\d+\.\s[a-zA-Z]"
    return bool(re.match(pattern, s))

def check_gender (x):
    if 'masc' in x:
        return 'masc'
    elif 'fem' in x:
        return 'fem'
    else:
        return None
    
def gender_distance_style_category_date_time(lista):
    """
    lista: result of tabula.read_pdf
    Output is (gender, distance, style, category) of the pdf IT NEEDS TO BE USED BEFORE nas_rows
    Functions in which it is being used: pdf_to_df
    """
    df = lista
    date_string = df.iloc[0,0].split(' ')[0]
    time_string = df.iloc[0,0].split(' ')[2]
    names = df.columns
    #names in lowercase
    names = [name.lower() for name in names]
    names = [name.replace('á','a') for name in names]
    names = [name.replace('é','e') for name in names]
    names = [name.replace('í','i') for name in names]
    names = [name.replace('ó','o') for name in names]
    names = [name.replace('ú','u') for name in names]
    # Find string in names which contains 50m, 100m, 200m or 400m
    gender_distance_style = [name for name in names if "50m" in name or "100m" in name or "200m" in name or "400m" in name]
    namessplitpoint = gender_distance_style[0].split('.')
    gender_str = namessplitpoint[0]
    gender = check_gender(gender_str)
    distance = namessplitpoint[1].split(' ')[1]
    # remove letters in distance
    distance = ''.join([i for i in distance if not i.isalpha()])
    style = namessplitpoint[1].split(' ')[2]

    # last element in names
    namessplitspace = names[-1].split(' ')
    category = namessplitspace[0]

    return gender, distance, style, category, date_string, time_string

def add_columns(df, gender, distance, style, category, date_string, time_string): 
    """"
    add to df 3 columns gender, distance, style, category.
    It should be used together with gender_distance_style_category
    Functions in which it is being used: pdf_to_df
    """
    #add to df 5 columns
    # First gender
    df["gender"] = [gender]*df.shape[0]
    # Second distance
    df["distance"] = [distance]*df.shape[0]
    # Third style
    df["style"] = [style]*df.shape[0]
    # Fourth category
    df["category"] = [category]*df.shape[0]
    # Fifth date
    df["date"] = [date_string]*df.shape[0]
    df["date"] = pd.to_datetime(df["date"], format='%d/%m/%Y')
    # Sixth time
    df["time"] = [time_string]*df.shape[0]
    df["time"] = pd.to_datetime(df["time"], format='%H:%M').dt.time
    return df

def race_timefun(df):
    # find column where there are some nan and it has the most rows with ":" in it
    columns = df.columns.tolist()
    previous_second_condition = 0
    second_condition = 0
    for column in columns:
        first_condition = df[column].isnull().any()
        previous_second_condition = second_condition
        second_condition = sum(df[column].apply(lambda x: isinstance(x, str) and x.count(':') == 1))
        # By adding second_condition > previous_second_condition I get at the end the column with the most rows with ":"
        if first_condition and second_condition > previous_second_condition:
            column_nan = column
    race_time = df[column_nan].tolist()
    # remove nan
    race_time = [x for x in race_time if str(x) != 'nan']

    # remove elements without :
    race_time = [x for x in race_time if ':' in x]
    
    race_time = [x.split(' ')[0] for x in race_time]
    df.drop(column_nan, axis=1, inplace=True)
    return race_time

#Datacleaning
def nas_rows(df):
    """
    df: dataframe
    Output: df with rows with only NaN removed and it removes the first two rows
    Functions in which it is being used: pdf_to_df
    """
    # Remove columns with more than 20% NaN
    df.dropna(axis=1, thresh=int(0.8*df.shape[0]), inplace=True)
    # Remove rows with more than 20% NaN
    df.dropna(axis=0, thresh=int(0.8*df.shape[1]), inplace=True)
    # Remove first two rows
    df.drop([0,1], axis=0, inplace=True)
    
    return df

# def column_points(df):
#     """
#     df: dataframe
#     Output: column with more than 20% of hyphens
#     We use this function in points function, in order to find the column we'll called score
#     """
#     for column in df.columns:
#         decimal_count = sum(df[column].apply(lambda x: isinstance(x, str) and x.count('.') == 1 and x.replace('.', '').isdigit()))
#         if decimal_count >= len(df) / 5:
#             return column
#     return  KeyError("No column with more than 20% hyphens found. list_hyphens: {}".format(list_hyphens))

# Example of usage:
# Replace 'your_data_frame' with the name of your DataFrame
# hyphen_columns = find_column_with_half_hyphens(your_data_frame)
# print(hyphen_columns)

# def puntos(df):
#     """
#     df: dataframe
#     Output: list of points and df without the column of points. From now on I will say scores instead of points
#     Functions being used: column_points
#     Functions in which it is being used: evenANDpuntos
#     """

#     # find the column with more than 20% of hyphens
#     column = column_points(df)
#     # extract the forth column starting by the end
#     points = df[column].tolist()
#     # remove elements from puntos which are "-"
#     points = [point for point in points if point != "-"]
#     # remove the column
#     df.drop(column, axis=1, inplace=True)
#     return points, df
def even_odd(df):
    """
    df: dataframe
    Output: df with only even rows and df with only odd rows
    It uses even_odd function
    Functions in which it is being used: evenANDpuntos
    """
    # create a new dataframe with even rows
    even = df.iloc[::2]
    # create a new dataframe with odd rows
    odd = df.iloc[1::2]
    return even, odd

def evenANDpuntos(df):
    """
    df: dataframe
    Output: df with only even rows and a new column for scores
    It uses even_odd and puntos functions
    Functions in which it is being used: pdf_to_df
    """
    even, _ = even_odd(df)
    # score, _ = puntos(df)
    # convert to float
    # score = [float(x) for x in score]
    # add puntos to even
    # even["score"] = score
    # reset index
    even.reset_index(drop=True, inplace=True)
    return even

def make_lowercase(s):
    """Converts a string to lowercase."""
    return s.lower()

def remove_accents(s):
    """Removes accents from a string."""
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def remove_whitespace(s):
    """Removes whitespace from a string."""
    return ''.join(s.split())

def find_teams(df, teams_rfen):
    """
    Modifies the input function to normalize the data for comparison,
    and to check for partial matches in all columns.
    """
    columns_with_teams = []

    # Normalizing the team names
    teams = [make_lowercase(remove_accents(remove_whitespace(team))) for team in teams_rfen["clubes"].tolist()]

    # Iterating through each column in the dataframe
    for column in df.columns:
        # Normalizing the data in the column
        normalized_column = df[column].apply(lambda x: make_lowercase(remove_accents(remove_whitespace(str(x)))))
        
        # Checking for any match in the column
        for team in teams:
            if normalized_column.str.contains(team).any():
                columns_with_teams.append(column)
                break  # Breaks the inner loop if a team is found in the current column

    return columns_with_teams[0]

def teams_with_names(df, teams_column_name):
    if (check_string_format(df[teams_column_name].iloc[0])):
        # Regular expression pattern to extract the desired parts
        # Capturing everything after the initial number and dot as the name
        # Capturing the number followed by the team name as the second part
        pattern1 = r'\d+\. ([\w\s,]+) (\d+ [\w\s.]+)'
        # pattern2 is same but without digit at the beginning
        pattern2 = r'([\w\s,]+) (\d+ [\w\s.]+)'

        # Lists to store the extracted data
        names = []
        number_team = []

        for item in df[teams_column_name].tolist():
            match1 = re.match(pattern1, item)
            match2 = re.match(pattern2, item)
            if match1:
                name_append = match1.group(1).strip()  # Name
                number_team_append = match1.group(2).strip() # Number + Team

                # Remove digits, dots and first whitespace from name_append
                name_append = re.sub(r'^\d+\. ', '', name_append)
                # Remove digits from number_team_append
                number_team_append = re.sub(r'\d+', '', number_team_append)
                
                names.append(name_append)
                number_team.append(number_team_append)
            elif match2:
                name_append = match2.group(1).strip()  # Name
                number_team_append = match2.group(2).strip() # Number + Team
                # Remove digits, dots and first whitespace from number_team_append if they have them
                number_team_append = re.sub(r'^\d+\. ', '', match2.group(2).strip())

                names.append(name_append)
                number_team.append(number_team_append)
            else:
                # Append NaN or a placeholder if the pattern doesn't match
                names.append(pd.NA)
                number_team.append(pd.NA)
        # Add columns to the dataframe
        df.insert(loc = 3, column = "team", value = number_team)
        df.insert(loc = 4, column = "full_name", value = names)
        # Remove the original column
        df.drop(teams_column_name, axis=1, inplace=True)

        # Reset index
        df.reset_index(drop=True, inplace=True)
        return df
    return df
    
def columns_df (df, race_time, teams_column_name, teams_rfen):
    """
    df: dataframe
    Output: df with column's names "first_surname", "second_surname", "name", "team", "race_time", "gender", "distance", "style", "category", "date", "event_time"
    It uses even_odd and puntos functions and it uses add_columns function
    Functions in which it is being used: pdf_to_df
    """

    if ("full_name" in df.columns):
        pass
    else:
        df.iloc[:,0] = df.iloc[:,0].str.split('.')
        # df[['first_surname', 'second_surname', 'name']] = df.iloc[:,0].str.split(' ', 2, expand=True)
        # remove the first column
        names_column = df.columns[0]
        df[["drop", "full_name"]] = pd.DataFrame(df[names_column].tolist(), index= df.index)
        df.drop(names_column, axis=1, inplace=True)
        df.drop("drop", axis=1, inplace=True)
        # Reset index
        df.reset_index(drop=True, inplace=True)

    # remove , in full_name
    df["full_name"] = df["full_name"].str.replace(',', '')
    # remove first whitespace in full_name
    df["full_name"] = df["full_name"].str.replace(' ', '', 1)
    # split full_name in three columns: firstname, secondname and name
    df['full_name'].str.split()

    # remove rows with nan in full_name 
    df.dropna(subset=['full_name'], inplace=True)
    # reset index
    df.reset_index(drop=True, inplace=True)

    name_parts = df['full_name'].str.split()
    # Take guiris into account
    for name_part in name_parts:
        if len(name_part) == 2:
            name_part.insert(1, '')
    df['first_surname'] = name_parts.str[0]
    df['first_surname'] = df['first_surname'].str.lower()
    df['second_surname'] = name_parts.str[1]
    df['second_surname'] = df['second_surname'].str.lower()
    df['name'] = name_parts.str[2]
    df['name'] = df['name'].str.lower()
    # remove full_name
    df.drop("full_name", axis=1, inplace=True)

    # first surname first column second surname second column and name third column
    cols = df.columns.tolist()
    cols = cols[-3:] + cols[:-3]
    df = df[cols]

    # reset index
    df.reset_index(drop=True, inplace=True)

    if ("team" not in df.columns):
        # find teams column
        teams = df[teams_column_name]
        # remove the column
        df.drop(teams_column_name, axis=1, inplace=True)
        # remove numbers and first whitespace in third column
        # remove numbers from teams if they exist

        if teams.str.contains('\d').any():
            teams = teams.str.replace('\d+', '')
            # teams = [''.join(char for char in item if not char.isdigit()).strip() for item in teams]

        # remove first whitespace if it exists
        if teams.str.contains(' ').any():
            teams = teams.str.replace(' ', '', 1)
            # teams = [item.lstrip() for item in teams]
        # add teams as the fourth column
        df.insert(loc = 3, column = "team", value = teams)

        # reset index
        df.reset_index(drop=True, inplace=True)

    print(df.iloc[:,2:])
    df.insert(loc = 4, column = "race_time", value = race_time)
    
    # reset index
    df.reset_index(drop=True, inplace=True)

    # rename last column to event_time
    df.rename(columns={df.columns[-1]: "event_time"}, inplace=True)
    #drop columns if they are not 11
    if (len(df.columns) != 11):
        # drop columns named differently from ["first_surname", "second_surname", "name", "team", "race_time", "gender", "distance", "style", "category", "date", "event_time"]
        columns = df.columns.tolist()
        notdropping = ["first_surname", "second_surname", "name", "team", "race_time", "gender", "distance", "style", "category", "date", "event_time"]
        for column in columns:
            if column not in notdropping:
                df.drop(column, axis=1, inplace=True)
                # reset index
                df.reset_index(drop=True, inplace=True)

    df.columns = ["first_surname", "second_surname", "name", "team", "race_time", "gender", "distance", "style", "category", "date", "event_time"]
    return df

# def delete_columns(df):
#     """
#     df: dataframe
#     Output: df without columns 2 and 4
#     """
#     df.drop(df.columns[2], axis=1, inplace=True)
#     df.drop(df.columns[4], axis=1, inplace=True)
#     return df
def nas_rows_extreme(df, race_time):
    # keep index in which there's a row with a nan
    index = df.index[df.isnull().any(axis=1)]
    # remove rows with nan
    df.dropna(axis=0, inplace=True)
    # reset index
    df.reset_index(drop=True, inplace=True)
    # delete element in race_time with the same index as the row with nan
    race_time = [race_time[i] for i in range(len(race_time)) if i not in index]
    return df, race_time

def pdf_to_df(pdf): 
    tabu = tabula.read_pdf(pdf, pages='all')
    tabu = tabu[0]
    gender, distance, style, category, date, time = gender_distance_style_category_date_time(tabu)
    race_time = race_timefun(tabu)
    tabu = add_columns(tabu, gender=gender, distance=distance, style=style, category=category, date_string=date, time_string=time) #add_columns has dataframe as input
    tabu = nas_rows(tabu)
    # reset index of tabu
    tabu.reset_index(drop=True, inplace=True)

    # Teams
    file = open("clubs.csv", "r")
    # dataframe from csv file with header
    teams_rfen = pd.DataFrame(csv.reader(file, delimiter=","))
    # make first row as header
    teams_rfen.columns = teams_rfen.iloc[0]
    # remove first row
    teams_rfen = teams_rfen.iloc[1:]
    # find teams column


    teams_column_name = find_teams(tabu, teams_rfen)

    # tabu = delete_columns(tabu) 
    tabu = evenANDpuntos(tabu)
    # tabu to csv
    tabu.to_csv("tabu.csv", index=False)
    tabu = teams_with_names(tabu, teams_column_name)
    print(tabu)
    tabu, race_time = nas_rows_extreme(tabu, race_time)
    tabu = columns_df(df=tabu, race_time=race_time, teams_column_name=teams_column_name, teams_rfen=teams_rfen)
    return tabu

