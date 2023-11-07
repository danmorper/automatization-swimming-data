import tabula
import pandas as pd

def gender_distance_style_category(lista):
    """
    lista: result of tabula.read_pdf
    Output is (gender, distance, style, category) of the pdf IT NEEDS TO BE USED BEFORE nas_rows
    """
    lista = lista[0]
    names = lista.columns
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

    namessplitspace = names[4].split(' ')
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
    # Remove columns with all NaN
    df.dropna(axis=1, how='all', inplace=True)
    # Remove rows with all NaN
    df.dropna(axis=0, how='all', inplace=True)
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