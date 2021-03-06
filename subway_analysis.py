#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
import os 
import time
import math
import importlib
import utilities

importlib.reload(utilities)

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
##------------------- HYPERPARAMETERS --------------------##
##--------------------------------------------------------##

##---- Filter
analysis = "15 min" #"AM Peak   "         #column in analysis (be careful to the extra spaces)
drop_lines = ['t']              #In ASC:        'u' = underground, 'd' = dlr + overground, 'r' = elizabeth + rails, 't' = tram

##---- Graph
graph_analysis = True

##---- Fine tuning
fine_tuning = False

# %%
##------------------ FILTER DATAFRAME --------------------##
##--------------------------------------------------------##

##---- Drop lines
for line in drop_lines:
    loads_df = loads_control[np.invert(loads_control['From ASC'].str.endswith(line))]
    entries_df = entries_control[np.invert(entries_control['ASC'].str.endswith(line))]
    exits_df = exits_control[np.invert(exits_control['ASC'].str.endswith(line))]

##---- Keep info and analysis
if analysis != "15 min":
    loads_df = (loads_df.iloc[:,0:10]).join((loads_df[analysis].round()).astype(int))
    entries_df = (entries_df.iloc[:,0:3]).join((entries_df[analysis].round()).astype(int))
    exits_df = (exits_df.iloc[:,0:3]).join((exits_df[analysis].round()).astype(int))
else:
    loads_df = (loads_df.iloc[:,0:10]).join((loads_df.iloc[:,17:].round()).astype(int))
    entries_df = (entries_df.iloc[:,0:3]).join((entries_df.iloc[:,11:].round()).astype(int))
    exits_df = (exits_df.iloc[:,0:3]).join((exits_df.iloc[:,11:].round()).astype(int))


# %%
##----------- GRAPH ANALYSIS: CREATE AND DRAW ------------##
##--------------------------------------------------------##

if graph_analysis:
    if (analysis != "15 min"):
        G = nx.from_pandas_edgelist(loads_df, 'From NLC', 'To NLC', analysis)
    else:
        G = nx.from_pandas_edgelist(loads_df, 'From NLC', 'To NLC')
    nx.draw(G, node_size=20)

# %%
##--------- GRAPH ANALYSIS: DEGREE DISTRIBUTION ----------##
##--------------------------------------------------------##

if graph_analysis:
    degrees = [val for (node, val) in G.degree()]
    plt.hist(degrees, bins=5)
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

##---- With analysis column
if analysis != "15 min":    
    B = [(loads_df[loads_df['From NLC'] == idx_station][analysis]).sum() for idx_station in loads_df['From NLC'].unique()]
    C = [(loads_df[loads_df['To NLC'] == idx_station][analysis]).sum() for idx_station in loads_df['From NLC'].unique()]
    V = (((entries_df.set_index(entries_df['NLC'])).reindex(index = loads_df['From NLC'].unique())).reset_index(drop=True))[analysis].tolist()
    U = (((exits_df.set_index(exits_df['NLC'])).reindex(index = loads_df['From NLC'].unique())).reset_index(drop=True))[analysis].tolist()

    if False:
        F = [[(loads_df[(loads_df['From NLC'] == idx) & (loads_df['To NLC'] == jdx)][analysis]).sum() for jdx in loads_df['From NLC'].unique()] for idx in loads_df['From NLC'].unique()]
        T_in = [(v_i + sum(f_i_T)) for v_i, f_i_T in zip(V, list(map(list, zip(*F))))]
        T_out = [(u_i + sum(f_i)) for u_i, f_i in zip(U, F)]
        F_flat = [item for items in F for item in items]
        F_in  = [ sum(f_i_T) for f_i_T in list(map(list, zip(*F)))]
        F_out = [ sum(f_i) for f_i in F]

##---- Every 15 minutes as flat list
else:                       
    V = entries_df.sort_values('NLC').iloc[:,3:].values.reshape(-1,).tolist()
    U = exits_df.sort_values('NLC').iloc[:,3:].values.reshape(-1,).tolist()
    F = loads_df.iloc[:,10:].values.reshape(-1,).tolist()
    F_in = (loads_df.iloc[:,10:].join(loads_df['To NLC'])).groupby('To NLC').sum().values.reshape(-1,).tolist()
    F_out = (loads_df.iloc[:,10:].join(loads_df['From NLC'])).groupby('From NLC').sum().values.reshape(-1,).tolist()
    T_in = [sum(el) for el in zip(V, F_in)]
    T_out = [sum(el) for el in zip(U, F_out)]

#%%
##--------------------- FINE TUNING ----------------------##
##--------------------------------------------------------##
"""
Fine tuning of the discard points and the bins. At the moment:
V ---> d_p = 3, n_bins = 100
U ---> d_p = 2, n_bins = 100
F ---> d_p = 32, n_bins = 100
F_in ---> d_p = 5, n_bins = 150
F_out ---> d_p = 9, n_bins = 250
"""

start_d_points = 0
stop_d_points = 10
start_bin = 200
stop_bin = 350
step_bin = 50
tune_matrix = F

if fine_tuning:
    d_points_range = np.arange(start_d_points, stop_d_points+1)
    for n_bin in np.arange(start_bin, stop_bin+1,step_bin):
        R2 = utilities.grid_search(tune_matrix, d_points_range, n_bin)
        plt.plot(d_points_range, R2)
        plt.xticks(d_points_range)
        plt.yticks(np.arange(0.9,1.02,0.01))
        plt.grid()
        plt.title("N bin: {}   R2 max: {:.4}   Index max: {}".format(str(n_bin), max(R2), R2.index(max(R2))+start_d_points))
        plt.show()

#%%
##---------------- FLOW DISTRIBUTION PLOTS ---------------##
##--------------------------------------------------------##

n_of_bins = {'V':100, 'U':100, 'F':100, 'F_in':150, 'F_out':150, 'T_in':150, 'T_out':150}
d_points =  {'V':0, 'U':0, 'F':1, 'F_in':1, 'F_out':1, 'T_in':1, 'T_out':1}

#%%

utilities.flow_histogram(V, zipf_f = True,flow_type='V15', path = abs_path, n_bins = n_of_bins['V'], save= True, discard_points = d_points['V'])
utilities.flow_histogram(U,  zipf_f = True,flow_type='U15', path = abs_path, n_bins = n_of_bins['U'], save= True, discard_points = d_points['U'])
utilities.flow_histogram(F, zipf_f = True, flow_type='F15', path = abs_path, n_bins = n_of_bins['F'], save= True, discard_points = d_points['F'])
utilities.flow_histogram(F_in, zipf_f = True, flow_type='F15_in', path = abs_path, n_bins = n_of_bins['F_in'], save= True, discard_points = d_points['F_in'])
utilities.flow_histogram(F_out, zipf_f = True,flow_type='F15_out', path = abs_path, n_bins = n_of_bins['F_out'], save= True, discard_points = d_points['F_out'])
utilities.flow_histogram(T_in, zipf_f = True, flow_type='T15_in', path = abs_path, n_bins = n_of_bins['T_in'], save= True, discard_points = d_points['T_in'])
utilities.flow_histogram(T_out, zipf_f = True, flow_type='T15_out', path = abs_path, n_bins = n_of_bins['T_out'], save= True, discard_points = d_points['T_out'])

# %%
