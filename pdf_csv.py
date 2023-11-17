import tabula
import pandas as pd
import os
# Import 20mmfunctions.py
import functions200m as fun200
import functions100m as fun100
import functions50m as fun50
## Get all files in pdfs folder
files = os.listdir('pdfs')
files = [file for file in files if file.endswith('.pdf')]
def selectfun(pdf):
    # if any column name has the string '4 x ' then omit do nothing
    tabu = tabula.read_pdf(pdf, pages='all')
    df = tabu[0]
    names = df.columns
    if any('4 x ' in name for name in names):
        print('relevo')
    else:
        # Detect in which column the distance is
        posible_distances = ['50m', '100m', '200m', '400m']
        for distance in posible_distances:
            for name in names:
                if (distance in name):
                    distance = ''.join([i for i in distance if not i.isalpha()])
                    return distance

# for file in files:
#     ## Read pdf file
#     file = "pdfs/" + file

#     ## Select function
#     distance = selectfun(file)

#     ## Apply function
#     if distance == '200':
#         fun200.pdf_to_df(file)
#     elif distance == '100':
#         fun100.pdf_to_df(file)
#     elif distance == '50':
#         fun50.pdf_to_df(file)
#     else:
#         print("Distance not found")
    

    
pdf = 'pdfs/ResultList_37.pdf'
distance = selectfun(pdf)
if distance == '200':
    fun200.pdf_to_df(pdf)
elif distance == '100':
    fun100.pdf_to_df(pdf)
elif distance == '50':
    fun50.pdf_to_df(pdf)
else:
    print("Distance not found")