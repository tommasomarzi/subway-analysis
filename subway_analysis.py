#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import os 
import scipy.optimize
import time

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
drop_lines = ['t']              #In ASC:        'u' = underground, 'd' = dlr + overground, 'r' = elizabeth + rails, 't' = trams

# %%
##------------------ FILTER DATAFRAME --------------------##
##--------------------------------------------------------##

##---- Save info and analysis
loads_df = (loads_control.iloc[:,0:10]).join((loads_control[analysis].round()).astype(int))
entries_df = (entries_control.iloc[:,0:3]).join((entries_control[analysis].round()).astype(int))
exits_df = (exits_control.iloc[:,0:3]).join((exits_control[analysis].round()).astype(int))

##---- Drop lines
for line in drop_lines:
    loads_df = loads_df[np.invert(loads_df['From ASC'].str.endswith(line))]
    entries_df = entries_df[np.invert(entries_df['ASC'].str.endswith(line))]
    exits_df = exits_df[np.invert(exits_df['ASC'].str.endswith(line))]

# %%
##------------------ GRAPH CREATION ----------------------##
##--------------------------------------------------------##

G = nx.from_pandas_edgelist(loads_df, 'From NLC', 'To NLC', analysis)
nx.draw(G, node_size=20)

# %%
##--------- GRAPH ANALYSIS: DEGREE DISTRIBUTION ----------##
##--------------------------------------------------------##

degrees = [val for (node, val) in G.degree()]
plt.hist(degrees, bins=100)
plt.title("Degrees distribution")

# %%
##---------------CONSTRUCTION OF THE MATRICES-------------##
##--------------------------------------------------------##
"""
Compute the matrices in list form.
Be careful: F takes some time to be computed.
Remark: f_{ij} is defined as the flow from i to j. 
F follows this notation, but in order to build it properly jdx also spans in loads_df['From NLC'].unique() (otherwise I would have different indexes and f_{kk} =/= 0).
"""

B = [(loads_df[loads_df['From NLC'] == idx_station][analysis]).sum() for idx_station in loads_df['From NLC'].unique()]
C = [(loads_df[loads_df['To NLC'] == idx_station][analysis]).sum() for idx_station in loads_df['From NLC'].unique()]
F = [[(loads_df[(loads_df['From NLC'] == idx) & (loads_df['To NLC'] == jdx)][analysis]).sum() for jdx in loads_df['From NLC'].unique()] for idx in loads_df['From NLC'].unique()]
V = (((entries_df.set_index(entries_df['NLC'])).reindex(index = loads_df['From NLC'].unique())).reset_index(drop=True))[analysis].tolist()
U = (((exits_df.set_index(exits_df['NLC'])).reindex(index = loads_df['From NLC'].unique())).reset_index(drop=True))[analysis].tolist()
T_in = [(v_i + sum(f_i_T)) for v_i, f_i_T in zip(V, list(map(list, zip(*F))))]
T_out = [(u_i + sum(f_i)) for u_i, f_i in zip(U, F)]
