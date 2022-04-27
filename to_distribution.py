'''This class is for counting the number of data points in CH1 that fall in range of y0+-delta
   as y0 is sweeps from the min to the max values in the dataset.
   This creates two Gaussian dustributions for LOW and HiGH signals of the square wave.
   The Gaussian distributions are then used for statistical analysis in other classes.'''

import numpy as np
import matplotlib.pyplot as plt
   
sweep = 0
    
def delta_sweep(filein, delta):
    
    signal = np.genfromtxt(filein, delimiter=',', skip_header=16, usecols=(0,1), missing_values=("Null"), filling_values=("NaN"), usemask=True)
    numsweeps = np.ceil( ( max(signal[:,1]) - min(signal[:,1]) ) / delta )
    distrib = np.zeros((int(numsweeps), 2))
    sweep = min(signal[:,1])
    for i in range(0, int(numsweeps)) :
        distrib[i,0] = sweep + delta
        for j in range(0, len(signal[:,0])) :
            if (sweep <= signal[j,1]) and (signal[j,1] < (sweep + delta)) :
                distrib[i,1] += 1
        sweep += delta
        Xmean = np.mean(distrib[:,0])
    return distrib, Xmean
  
    
# remove the zero # of data points rows from distrib
def remove_zeros(distrib):
    
    distrib_nozero = np.copy(distrib)
    ENDdistrib = len(distrib[:,0])
    for rep in range(10) : # dark magic don't touch
        i=0
        while i < ENDdistrib :
            if distrib_nozero[i,1] == 0.0 :
                distrib_nozero = np.delete(distrib_nozero, i, axis=0)
                ENDdistrib = len(distrib_nozero[:,0])
            i += 1
    return distrib_nozero

    
def plot_sweep(distrib, ax, i):
    
    #fig, ax = plt.subplots()
    title="A{0:04d}CH1".format(i)
    ax.set(xlabel='V', ylabel='Number of data points', title=title)
    distrib_nozero = remove_zeros(distrib)
    #xidxticks = list(range(len(distrib_nozero[:,0])))
    #plt.xticks(xidxticks, distrib_nozero[:,0])
    ax.plot(distrib_nozero[:,0], distrib_nozero[:,1], '--', color='grey', alpha=0.6)
    ax.scatter(distrib_nozero[:,0], distrib_nozero[:,1], c='black', marker='.')
    ax.vlines(np.mean(distrib[:,0]), -50, 700, linestyles='dotted', label="Xmean")
    #ax.legend()
    
'''
import numpy as np
from to_distribution import *
distrib = delta_sweep("../final data/ALL0000/A0000CH1.CSV")
distrib
distrib = remove_zeros(distrib)
distrib
plot_sweep(distrib)
ax = fig.add_subplot(111)
'''