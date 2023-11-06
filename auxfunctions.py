import tabula
import pandas as pd

def gender_distance_style_category(lista):
    """
    lista: result of pdf_to_csv
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