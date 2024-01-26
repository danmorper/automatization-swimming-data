import tabula
import pandas as pd
import os
# Import 20mmfunctions.py
import functions200m as fun200
import functions100m as fun100
import functions50m as fun50

import sys
# get the city name as an argument
city_name = sys.argv[1]

## Get all files in pdfs folder
folders = os.listdir('pdfs')
files_dict = dict()
files_dict = files_dict.fromkeys(folders)
for key in files_dict.keys():
    files_dict[key] = []
# Add files to files_dict
for folder in folders:
    folder_path = 'pdfs/' + folder
    if (os.path.isdir(folder_path)):
        files_in_folder = os.listdir(folder_path)
        for file in files_in_folder:
            files_dict[folder].append(file)
print(files_dict)
#export files_dict as json
import json
with open('files_dict.json', 'w') as fp:
    json.dump(files_dict, fp)

def selectfun(pdf):
    # if any column name has the string '4 x ' then omit do nothing
    tabu = tabula.read_pdf(pdf, pages='all')
    df = tabu[0]
    names = df.columns
    if any('4 x ' in name for name in names):
        print('relevo')
    else:
        # Detect in which column the distance is
        posible_distances = ['50m', '100m', '200m']
        for distance in posible_distances:
            for name in names:
                if (distance in name):
                    distance = ''.join([i for i in distance if not i.isalpha()])
                    return distance

errors = dict()
errors = errors.fromkeys(folders)
no_distance = {}
no_distance = no_distance.fromkeys(folders)
success = {}
success = success.fromkeys(folders)

def piscina_corta(df, path):
    # Create a new column called 'Piscina Corta' and set it to true if there exists a file called 'piscina_corta.txt' in the path
    if os.path.exists(os.path.join(path, 'piscina_corta.txt')):
        df['Piscina Corta'] = True
        return df
    else:
        df['Piscina Corta'] = False
        return df

def delegacion(df, city):
    df['delegacion'] = city
    return df

# iterate through folders
for folder in files_dict.keys():
    #iterate through files in folder
    for file in files_dict[folder]:
        print(file)
        ## Read pdf file
        file_path = "pdfs/{}/{}".format(folder, file)

        ## Select function
        try: 
            distance = selectfun(file_path)
            ## Apply function
            if distance == '200':
                try: 
                    df = fun200.pdf_to_df(file_path)
                    folder_path = os.path.join('pdfs', folder)
                    print(folder_path)
                    df = piscina_corta(df, folder_path)
                    df = delegacion(df, city_name)
                    # convert df to csv 
                    # remove .pdf from file name
                    file = file[:-4]
                    df.to_csv('csvs/' + folder + file + '.csv', index=False)
                    success[folder] = file
                    print("Success in file: {}".format(file))
                except:
                    errors[folder] = file
                    print("Error in file: {}".format(file) + ". Distance: {}".format(distance))
                    continue
            elif distance == '100':
                try:
                    df = fun100.pdf_to_df(file_path)
                    folder_path = os.path.join('pdfs', folder)
                    df = piscina_corta(df, folder_path)
                    df = delegacion(df, city_name)
                    # convert df to csv 
                    # remove .pdf from file name
                    file = file[:-4]
                    df.to_csv('csvs/' + folder + file + '.csv', index=False)
                    success[folder] = file
                    print("Success in file: {}".format(file))
                except:
                    errors[folder] = file
                    print("Error in file: {}".format(file) + ". Distance: {}".format(distance))
                    continue
            elif distance == '50':
                try:
                    df = fun50.pdf_to_df(file_path)
                    folder_path = os.path.join('pdfs', folder)
                    df = piscina_corta(df, folder_path)
                    df = delegacion(df, city_name)
                    # convert df to csv 
                    # remove .pdf from file name
                    file = file[:-4]
                    df.to_csv('csvs/' + folder + file + '.csv', index=False)
                    success[folder] = file
                    print("Error in file: {}".format(file) + ". Distance: {}".format(distance))
                except:
                    errors[folder] = file
                    print("Error in file: {}".format(file))
                    continue
            else:
                no_distance[folder] = file
        except:
            errors[folder] = file
            print("Error in file: {}".format(file) + "No distance found")
            continue

        
    
# save errors no_distance and success as json
import json
with open('errors.json', 'w') as fp:
    json.dump(errors, fp)
with open('no_distance.json', 'w') as fp:
    json.dump(no_distance, fp)
with open('success.json', 'w') as fp:
    json.dump(success, fp)

    
# pdf = 'pdfs/ResultList_37.pdf'
# distance = selectfun(pdf)
# if distance == '200':
#     fun200.pdf_to_df(pdf)
# elif distance == '100':
#     fun100.pdf_to_df(pdf)
# elif distance == '50':
#     fun50.pdf_to_df(pdf)
# else:
#     print("Distance not found")
