import tabula
import pandas as pd
import os
# Import 20mmfunctions.py
import functions200m as fun200
## Get all files in pdfs folder
files = os.listdir('pdfs')


# Read pdf file
ResultList_25_path = "pdfs/ResultList_25.pdf"
# convert ResultList_25 dataframe into ResultList_25.csv
ResultList_25_df = fun200.pdf_to_df(ResultList_25_path)
ResultList_25_df.to_csv("csvs/ResultList_25.csv", index=False)
print(ResultList_25_df)

ResultList_26 = "pdfs/ResultList_26.pdf"
# convert ResultList_26 dataframe into ResultList_26.csv
ResultList_26_df = fun200.pdf_to_df(ResultList_26)
ResultList_26_df.to_csv("csvs/ResultList_26.csv", index=False)

ResultList_27 = "pdfs/ResultList_27.pdf"
# convert ResultList_27 dataframe into ResultList_27.csv
ResultList_27_df = fun200.pdf_to_df(ResultList_27)
ResultList_27_df.to_csv("csvs/ResultList_27.csv", index=False)

# for file in files:
#     ## Read pdf file
#     file = "pdfs/" + file
#     print(file)
#     print(fun200.pdf_to_df(file))
