import tabula
import pandas as pd
from datetime import datetime as dt
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
    # Get the second name
    namessplitpoint = names[1].split('.')
    gender = namessplitpoint[0]
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

def columns_df (df):
    """
    df: dataframe
    Output: df with column's names "first_surname", "second_surname", "name", "team", "race_time", "gender", "distance", "style", "category", "date", "event_time"
    It uses even_odd and puntos functions and it uses add_columns function
    Functions in which it is being used: pdf_to_df
    """
    df.iloc[:,0] = df.iloc[:,0].str.split('.')
    # df[['first_surname', 'second_surname', 'name']] = df.iloc[:,0].str.split(' ', 2, expand=True)
    # remove the first column
    first_column = df.columns[0]
    df[["drop", "full_name"]] = pd.DataFrame(df[first_column].tolist(), index= df.index)
    df.drop(first_column, axis=1, inplace=True)
    df.drop("drop", axis=1, inplace=True)
    # Reset index
    df.reset_index(drop=True, inplace=True)

    # remove , in full_name
    df["full_name"] = df["full_name"].str.replace(',', '')
    # split full_name in three columns: firstname, secondname and name
    name_parts = df['full_name'].str.split()
    
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

    # drop column 5
    df.drop(df.columns[5], axis=1, inplace=True)

    # reset index
    df.reset_index(drop=True, inplace=True)

    # remove numbers and first whitespace in third column
    teams = df.iloc[:,3]
    df.drop(df.columns[3], axis=1, inplace=True)
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

    print(df)

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

def pdf_to_df(pdf): 
    tabu = tabula.read_pdf(pdf, pages='all')
    tabu = tabu[0]
    gender, distance, style, category, date, time = gender_distance_style_category_date_time(tabu)
    tabu = add_columns(tabu, gender=gender, distance=distance, style=style, category=category, date_string=date, time_string=time) #add_columns has dataframe as input
    tabu = nas_rows(tabu)
    # reset index of tabu
    tabu.reset_index(drop=True, inplace=True)
    # tabu = delete_columns(tabu) 
    tabu = evenANDpuntos(tabu)
    tabu = columns_df(tabu)
    return tabu

