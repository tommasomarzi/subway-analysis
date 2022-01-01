# %%
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

#%%
##-------------------- FIT POWER LAW ---------------------##
##--------------------------------------------------------##

def power_law(x, a, b):
    return a*(x**(-b))

def power_law_fit(x, y, discard = None):
    if discard:
        x = x[discard:]
        y = y[discard:]
    pars, cov = curve_fit(f=power_law, xdata=x, ydata=y, p0=[0, 0], bounds=(-np.inf, np.inf))
    return pars

#%%
##--------------------- ZIPF LAW -------------------------##
##--------------------------------------------------------##

def zipf(x, a, b, c):
    return ((b+a*x)**(-c))

def zipf_fit(x, y, discard = None):
    if discard:
        x = x[discard:]
        y = y[discard:]
    pars, cov = curve_fit(f=zipf, xdata=x, ydata=y, p0=[0.1, 10, 2], bounds=(0, np.inf))#, p0=[0, 0, 0],
    return pars

#%%
##--------------------FLOW DISTRIBUTION-------------------##
##--------------------------------------------------------##

def flow_histogram(matrix, zipf_f = False, flow_type = None, path = None, n_bins = None, save = False, discard_points = None, logscale = True):
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
    
    if logscale:
        ax.set_xscale('log')
        ax.set_yscale('log')

        x_high = math.pow(10,np.ceil(math.log10(bins.max())))
        x_high_prev = math.pow(10,np.floor(math.log10(bins.max())))
        y_low = math.pow(10,np.floor(math.log10(n[n>0].min())))
        y_low_aft = math.pow(10,np.ceil(math.log10(n[n>0].min())))

        if (n[n>0].min()-y_low ) < (y_low_aft - y_low)/10.:
            y_low = math.pow(10,np.floor(math.log10(n[n>0].min()))-1)

        #if (x_high-bins.max()) < (x_high - x_high_prev)/10.:
        #    x_high = math.pow(10,np.ceil(math.log10(bins.max()))+1)
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
    elif flow_type == 'T15_in':       
        ax.set_xlabel('$T_{in}$')
        ax.set_ylabel('P($T_{in}$)') 
    elif flow_type == 'T15_out':       
        ax.set_xlabel('$T_{out}$')
        ax.set_ylabel('P($T_{out}$)') 
    
    x_bins = bins[:-1]+ 0.5*(bins[1:] - bins[:-1])

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    if zipf_f:
        pars = zipf_fit(x_bins[n>0], n[n>0],discard_points)
        predicted = zipf(x_bins[n>0.0][discard_points:], *pars)
        R2 = r2_score(n[n>0.0][discard_points:], predicted)

        text = '$\gamma$ = {:.2f}'.format(pars[2]) + '\n' +r'$\alpha$ = {:.3f}'.format(pars[0]) + '\n' + '$R^2$ = {:.3f}'.format(R2)

        ax.grid()

        ax.scatter(x_bins, n, marker='.', c='red', s=40, alpha=0.3)
        ax.plot(x_bins[discard_points:], zipf(x_bins[discard_points:], *pars), linestyle='-', linewidth=1, color='black')
        ax.text(0.2, 0.35, text, transform=ax.transAxes, fontsize=8, verticalalignment='center', bbox=props)
    else:
        pars = power_law_fit(x_bins[n>0], n[n>0],discard_points)
        predicted = power_law(x_bins[n>0.0][discard_points:], *pars)
        R2 = r2_score(n[n>0.0][discard_points:], predicted)

        text = '$\gamma$ = {:.2f}'.format(pars[1]) + '\n' + '$R^2$ = {:.3f}'.format(R2)

        ax.grid()

        ax.scatter(x_bins, n, marker='.', c='red', s=40, alpha=0.3)
        ax.plot(x_bins[discard_points:], power_law(x_bins[discard_points:], *pars), linestyle='-', linewidth=1, color='black')
        ax.text(0.2, 0.35, text, transform=ax.transAxes, fontsize=8, verticalalignment='center', bbox=props)

    ax.minorticks_on()
    fig.tight_layout()
    
    if save:
        fig.savefig(path + '/pics/flow_distribution_'+str(flow_type)+'.png', dpi=1000, facecolor='white', transparent=False)
    plt.show()
    plt.close()

#%%
##---------------------- GRID SEARCH ---------------------##
##--------------------------------------------------------##

def grid_search(matrix, d_points_range, n_bins = None):

    if n_bins:
        n,bins,patches = plt.hist(matrix, density=True, bins = n_bins, alpha=0.6)
    else:
        n,bins,patches = plt.hist(matrix, density=True, alpha=0.6)
    plt.close()

    n = n/sum(n)

    x_bins = bins[:-1]+ 0.5*(bins[1:] - bins[:-1])

    R2_list = []

    for d_points in d_points_range:
        pars = power_law_fit(x_bins[n>0], n[n>0],d_points)
        predicted = power_law(x_bins[n>0.0][d_points:], *pars)
        R2_list.append(r2_score(n[n>0.0][d_points:], predicted))
    
    return R2_list
