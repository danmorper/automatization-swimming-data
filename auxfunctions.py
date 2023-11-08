import tabula
import pandas as pd

def gender_distance_style_category(lista):
    """
    lista: result of tabula.read_pdf
    Output is (gender, distance, style, category) of the pdf IT NEEDS TO BE USED BEFORE nas_rows
    """
    df = lista
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

    return gender, distance, style, category

def add_columns(df, gender, distance, style, category): 
    """"
    add to df 3 columns gender, distance, style, category.
    It should be used together with gender_distance_style_category
    """
    #add to df 3 columns
    # First gender
    df["gender"] = [gender]*df.shape[0]
    # Second distance
    df["distance"] = [distance]*df.shape[0]
    # Third style
    df["style"] = [style]*df.shape[0]
    # Fourth category
    df["category"] = [category]*df.shape[0]
    return df

#Datacleaning
def nas_rows(df):
    """
    df: dataframe
    Output: df with rows with only NaN removed and it removes the first two rows
    """
    # Remove columns with more than 20% NaN
    df.dropna(axis=1, thresh=int(0.8*df.shape[0]), inplace=True)
    # Remove rows with more than 20% NaN
    df.dropna(axis=0, thresh=int(0.8*df.shape[1]), inplace=True)
    # Remove first two rows
    df.drop([0,1], axis=0, inplace=True)
    
    return df

def puntos(df):
    """
    df: dataframe
    Output: list of points and df without the column of points. From now on I will say scores instead of points
    """
    # extract the forth column starting by the end
    points = df.iloc[:,-5].tolist()
    # remove elements from puntos which are "-"
    points = [point for point in points if point != "-"]
    # remove the column
    df.drop(df.columns[-5], axis=1, inplace=True)
    return points, df
def even_odd(df):
    """
    df: dataframe
    Output: df with only even rows and df with only odd rows
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
    """
    even, _ = even_odd(df)
    score, _ = puntos(df)
    # convert to float
    score = [float(x) for x in score]
    # add puntos to even
    even["score"] = score
    # reset index
    even.reset_index(drop=True, inplace=True)
    return even

def surnames_names_team (df):
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
    # remove numbers from teams
    teams = [''.join(char for char in item if not char.isdigit()).strip() for item in teams]
    # remove first whitespace
    teams = [team.lstrip() for team in teams]
    print(teams)
    # add teams as the fourth column
    df.insert(loc = 3, column = "team", value = teams)

    # reset index
    df.reset_index(drop=True, inplace=True)

    df.columns = ["first_surname", "second_surname", "name", "team", "time", "gender","distance", "style", "category", "score"]
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
    gender, distance, style, category = gender_distance_style_category(tabu)
    tabu = add_columns(tabu, gender=gender, distance=distance, style=style, category=category) #add_columns has dataframe as input
    tabu = nas_rows(tabu)
    # reset index of tabu
    tabu.reset_index(drop=True, inplace=True)
    # tabu = delete_columns(tabu) 
    tabu = evenANDpuntos(tabu)
    tabu = surnames_names_team(tabu)
    return tabu

