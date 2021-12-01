#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import os 

#%%

abs_path = os.path.dirname(os.path.realpath(__file__))

#%%

original_db = pd.ExcelFile(abs_path + '/data/NBT19FRI_Outputs.xlsx')

# %%
##--------------------------------------------------------##
##          SHEETS LOAD                                   ##
##--------------------------------------------------------##

loads_db = pd.read_excel(original_db, "Link_Loads", header=1, skiprows=[0], thousands='.')
#freq_db = pd.read_excel(original_db, "Link_Frequencies", header=1, skiprows=[0], thousands='.')
#l_boarders_db = pd.read_excel(original_db, "Line_Boarders", header=1, skiprows=[0], thousands='.')
#flow_db = pd.read_excel(original_db, "Station_Flows", header=1, skiprows=[0], thousands='.')
entries_db = pd.read_excel(original_db, "Station_Entries", header=1, skiprows=[0], thousands='.')
exits_db = pd.read_excel(original_db, "Station_Exits", header=1, skiprows=[0], thousands='.')
#boarders_db = pd.read_excel(original_db, "Station_Boarders", header=1, skiprows=[0], thousands='.')
#alighters_db = pd.read_excel(original_db, "Station_Alighters", header=1, skiprows=[0], thousands='.')

# %%
##--------------------------------------------------------##
##          HYPERPARAMETERS FOR FILTER                    ##
##--------------------------------------------------------##

analysis = "AM Peak   "
df = (loads_db.iloc[:,0:10]).join(loads_db[analysis])

# %%
##--------------------------------------------------------##
##          GRAPH CREATION                                ##
##--------------------------------------------------------##

G_loads = nx.from_pandas_edgelist(df, 'From NLC', 'To NLC', analysis)
nx.draw(G_loads)

# %%
##--------------------------------------------------------##
##          GRAPH ANALYSIS: DEGREE DISTRIBUTION           ##
##--------------------------------------------------------##

degrees_dict = G_loads.degree
degrees = [val for (node, val) in G_loads.degree()]
plt.hist(degrees, bins=100)
plt.title("Degrees distribution")

# %%
