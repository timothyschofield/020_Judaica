
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

metadata_rec_search__input = Path(f"metadata_input/_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - Benchmark.csv")

if os.path.exists(metadata_rec_search__input) != True:
    print(f"ERROR: {metadata_rec_search__input} file does not exits")
    exit()

df_rec_search = pd.read_csv(metadata_rec_search__input)
print(df_rec_search)

df_rec_search.set_index("Item name", inplace=True)

this_line = df_rec_search.loc["uni-ucl-jud-0015091-001"] # returns a Series
print(this_line)

print(this_line.loc["<title>"])




















