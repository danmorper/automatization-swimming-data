import tabula
import pandas as pd
import os
# Import 20mmfunctions.py
import functions200m as fun200
import functions100m as fun100
import functions50m as fun50
## Get all files in pdfs folder
files = os.listdir('pdfs')

def selectfun(pdf):
    tabu = tabula.read_pdf(pdf, pages='all')
    df = tabu[0]
    names = df.columns
    # Get the second name
    namessplitpoint = names[1].split('.')
    distance = namessplitpoint[1].split(' ')[1]
    # remove letters in distance
    distance = ''.join([i for i in distance if not i.isalpha()])

    return distance

for file in files:
    ## Read pdf file
    file = "pdfs/" + file

    ## Select function
    distance = selectfun(file)

    ## Apply function
    if distance == '200':
        fun200.pdf_to_df(file)
    elif distance == '100':
        fun100.pdf_to_df(file)
    elif distance == '50':
        fun50.pdf_to_df(file)
    else:
        print("Distance not found")
    

    
