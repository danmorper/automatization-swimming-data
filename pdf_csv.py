import tabula
import pandas as pd
import os
# Import auxfunctions.py
import auxfunctions as aux
## Get all files in pdfs folder
files = os.listdir('pdfs')

for file in files:
    ## Read pdf file
    lista = tabula.read_pdf(file, pages='all')
    
