#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os 

#%%

abs_path = os.path.dirname(os.path.realpath(__file__))

#%%

original_db = pd.ExcelFile(abs_path + '/data/NBT19FRI_Outputs.xlsx')

# %%

loads_db = pd.read_excel(original_db, "Link_loads", header=1, skiprows=[0], thousands='.')
#freq_db = pd.read_excel(original_db, "Link_Frequencies", header=1, skiprows=[0], thousands='.')
#l_boarders_db = pd.read_excel(original_db, "Line_Boarders", header=1, skiprows=[0], thousands='.')
flow_db = pd.read_excel(original_db, "Station_Flows", header=1, skiprows=[0], thousands='.')
entries_db = pd.read_excel(original_db, "Station_Entries", header=1, skiprows=[0], thousands='.')
exits_db = pd.read_excel(original_db, "Station_Exits", header=1, skiprows=[0], thousands='.')
#boarders_db = pd.read_excel(original_db, "Station_Boarders", header=1, skiprows=[0], thousands='.')
#alighters_db = pd.read_excel(original_db, "Station_Alighters", header=1, skiprows=[0], thousands='.')

# %%
