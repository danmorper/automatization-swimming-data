#%%
import tabula
import pandas as pd
import os

# Read pdf
df = tabula.read_pdf("pdfs/ResultList_25.pdf", pages='all')

print(df)
# %%
