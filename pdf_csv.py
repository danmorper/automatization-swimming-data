import tabula
import pandas as pd
import os
# Import auxfunctions.py
import auxfunctions as aux
## Get all files in pdfs folder
files = os.listdir('pdfs')


# Read pdf file
ResultList_25_path = "pdfs/ResultList_25.pdf"
# convert ResultList_25 dataframe into ResultList_25.csv
ResultList_25_df = aux.pdf_to_df(ResultList_25_path)
ResultList_25_df.to_csv("csvs/ResultList_25.csv", index=False)

ResultList_26 = "pdfs/ResultList_26.pdf"
# convert ResultList_26 dataframe into ResultList_26.csv
ResultList_26_df = aux.pdf_to_df(ResultList_26)
ResultList_26_df.to_csv("csvs/ResultList_26.csv", index=False)

# for file in files:
#     ## Read pdf file
#     file = "pdfs/" + file
#     print(file)
#     print(aux.pdf_to_df(file))
