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
##-------------- LOAD SHEETS OF THE EXCEL ----------------##
##--------------------------------------------------------##

loads_control = pd.read_excel(original_db, "Link_Loads", header=1, skiprows=[0], thousands='.')
#freq_control = pd.read_excel(original_db, "Link_Frequencies", header=1, skiprows=[0], thousands='.')
#l_boarders_control = pd.read_excel(original_db, "Line_Boarders", header=1, skiprows=[0], thousands='.')
flow_control = pd.read_excel(original_db, "Station_Flows", header=1, skiprows=[0], thousands='.')
entries_control = pd.read_excel(original_db, "Station_Entries", header=1, skiprows=[0], thousands='.')
exits_control = pd.read_excel(original_db, "Station_Exits", header=1, skiprows=[0], thousands='.')
#boarders_control = pd.read_excel(original_db, "Station_Boarders", header=1, skiprows=[0], thousands='.')
#alighters_control = pd.read_excel(original_db, "Station_Alighters", header=1, skiprows=[0], thousands='.')

# %%
##------------- HYPERPARAMETERS FOR FILTER ---------------##
##--------------------------------------------------------##

analysis = "AM Peak   "         #column in analysis (be careful to the extra spaces)

# %%
##------------------ FILTER DATAFRAME --------------------##
##--------------------------------------------------------##

loads_df = (loads_control.iloc[:,0:10]).join((loads_control[analysis].round()).astype(int))
entries_df = (entries_control.iloc[:,0:3]).join((entries_control[analysis].round()).astype(int))
exits_df = (exits_control.iloc[:,0:3]).join((exits_control[analysis].round()).astype(int))

# %%
##------------------ GRAPH CREATION ----------------------##
##--------------------------------------------------------##

G = nx.from_pandas_edgelist(loads_df, 'From NLC', 'To NLC', analysis)
nx.draw(G, node_size=20)

# %%
##--------- GRAPH ANALYSIS: DEGREE DISTRIBUTION ----------##
##--------------------------------------------------------##

degrees_dict = G.degree
degrees = [val for (node, val) in G.degree()]
plt.hist(degrees, bins=100)
plt.title("Degrees distribution")

# %%
##---------------CONSTRUCTION OF THE MATRICES-------------##
##--------------------------------------------------------##
"""
Compute the matrices in list form.
Be careful: F takes some time to be computed.
"""

B = [(loads_df[loads_df.iloc[:,4] == idx_station][analysis]).sum() for idx_station in loads_df.iloc[:,4].unique()]
C = [(loads_df[loads_df.iloc[:,7] == idx_station][analysis]).sum() for idx_station in loads_df.iloc[:,4].unique()]
#F = [[(loads_df[(loads_df.iloc[:,4] == idx) & (loads_df.iloc[:,7] == jdx)][analysis]).sum() for jdx in loads_df.iloc[:,4].unique()] for idx in loads_df.iloc[:,4].unique()]
V = (((entries_df.set_index(entries_df['NLC'])).reindex(index = loads_df.iloc[:,4].unique())).reset_index(drop=True))[analysis].tolist()
U = (((exits_df.set_index(exits_df['NLC'])).reindex(index = loads_df.iloc[:,4].unique())).reset_index(drop=True))[analysis].tolist()

# %%

