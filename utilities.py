# %%
import matplotlib.pyplot as plt
import math
import numpy as np

#%%
##--------------------FLOW DISTRIBUTION-------------------##
##--------------------------------------------------------##

def flow_histogram(matrix, flow_type = None, path = None, n_bins = None, save = False):
    """
    Build the histogram and plot it through a scatter plot.
    """

    if n_bins:
        n,bins,patches = plt.hist(matrix, density=True, bins = n_bins, alpha=0.6)
    else:
        n,bins,patches = plt.hist(matrix, density=True, alpha=0.6)
    plt.close()

    n = n/sum(n)
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_yscale('log')

    x_high = math.pow(10,np.ceil(math.log10(bins.max())))
    x_high_prev = math.pow(10,np.floor(math.log10(bins.max())))
    y_low = math.pow(10,np.floor(math.log10(n[n>0].min())))
    y_low_aft = math.pow(10,np.ceil(math.log10(n[n>0].min())))

    if (n[n>0].min()-y_low ) < (y_low_aft - y_low)/10.:
        y_low = math.pow(10,np.floor(math.log10(n[n>0].min()))-1)

    if (x_high-bins.max()) < (x_high - x_high_prev)/10.:
        x_high = math.pow(10,np.ceil(math.log10(bins.max()))+1)

    ax.set_xlim((1, x_high))
    ax.set_ylim((y_low, 1))
    
    if flow_type == 'U':
        ax.set_xlabel('$u_{i->0}$')
        ax.set_ylabel('P($u_{i->0}$)')
    elif flow_type == 'V':       
        ax.set_xlabel('$v_{0->i}$')
        ax.set_ylabel('P($v_{0->i}$)') 
    elif flow_type == 'F':       
        ax.set_xlabel('$f_{i->j}$')
        ax.set_ylabel('P($f_{i->j}$)') 
    elif flow_type == 'F_in':       
        ax.set_xlabel('$f_{.->i}$')
        ax.set_ylabel('P($f_{.->i}$)') 
    elif flow_type == 'F_out':       
        ax.set_xlabel('$f_{i->.}$')
        ax.set_ylabel('P($f_{i->.}$)') 
    elif flow_type == 'F15':       
        ax.set_xlabel('$f_{i->j}$')
        ax.set_ylabel('P($f_{i->j}$)') 
    elif flow_type == 'U15':
        ax.set_xlabel('$u_{i->0}$')
        ax.set_ylabel('P($u_{i->0}$)')
    elif flow_type == 'V15':
        ax.set_xlabel('$v_{0->i}$')
        ax.set_ylabel('P($v_{0->i}$)')
    elif flow_type == 'F15_in':       
        ax.set_xlabel('$f_{.->i}$')
        ax.set_ylabel('P($f_{.->i}$)') 
    elif flow_type == 'F15_out':       
        ax.set_xlabel('$f_{i->.}$')
        ax.set_ylabel('P($f_{i->.}$)') 
    
    ax.scatter(bins[:-1]+ 0.5*(bins[1:] - bins[:-1]), n, marker='.', c='red', s=40, alpha=0.3)
    ax.grid()
    fig.tight_layout()

    if save:
        fig.savefig(path + '/flow_distribution_'+str(flow_type)+'.png', dpi=1200, transparent=False)
    plt.show()
    plt.close()

