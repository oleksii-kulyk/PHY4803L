# -*- coding: utf-8 -*-

'''This module takes the data in `distrib` and fits two Gaussian distributions to the data.
   Then it overlays them on the existing plots'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from to_distribution import *

#Define the Gaussian function   
def Gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def fit_GaussL(distrib, Xmean, ax): #remember to move Xmean+-0.001
    #fit is preformed after distrib is stripper of zeroes
    distrib_nozero = remove_zeros(distrib)
    iMean=0
    while (distrib_nozero[iMean,0] < Xmean) :
         iMean += 1
    #interpolate data for smoother fit
    interp3 = interp1d(distrib_nozero[:iMean,0], distrib_nozero[:iMean,1], kind = "cubic")
    xfit = np.linspace(distrib_nozero[0,0], distrib_nozero[iMean-1,0], 100, endpoint=False)
    popt, pcov = curve_fit(Gauss, distrib[:iMean,0], distrib[:iMean, 1])
    y_fitGauss = Gauss(xfit, popt[0],popt[1],popt[2],popt[3])
    ax.plot(xfit, y_fitGauss, 'b-', label="LOGauss")
    plt.legend()
    
def fit_GaussH(distrib, Xmean, ax): #remember to move Xmean+-0.001
    #fit is preformed after distrib is stripper of zeroes
    distrib_nozero = remove_zeros(distrib)
    iMean=len(distrib_nozero[:,0]) - 1
    while (distrib_nozero[iMean,0] > Xmean) :
        iMean -= 1
    #interpolate data for smoother fit
    interp3 = interp1d(distrib_nozero[iMean:,0], distrib_nozero[iMean:,1], kind = "cubic")
    xfit = np.linspace(distrib_nozero[iMean,0], distrib_nozero[-1,0], 100, endpoint=False)
    popt, pcov = curve_fit(Gauss, distrib[iMean:,0], distrib[iMean:, 1])
    y_fitGauss = Gauss(xfit, popt[0],popt[1],popt[2],popt[3])
    ax.plot(xfit, y_fitGauss, 'r-', label="HIGauss")
    plt.legend()
    
def fit_PolyL(distrib, Xmean, ax, deg=3): #remember to move Xmean+-0.001
    #fit is preformed after distrib is stripper of zeroes
    distrib_nozero = remove_zeros(distrib)
    iMean=0
    while (distrib_nozero[iMean,0] < Xmean) :
        iMean += 1
    #interpolate data for smoother fit
    interp3 = interp1d(distrib_nozero[:iMean,0], distrib_nozero[:iMean,1], kind = "cubic")
    xfit = np.linspace(distrib_nozero[0,0], distrib_nozero[iMean-1,0], 100, endpoint=False)
    pfit=np.poly1d(np.polyfit(xfit, interp3(xfit), deg))
    ax.plot(distrib_nozero[:iMean,0], pfit(distrib_nozero[:iMean,0]), 'b-', label="LOpoly")
    plt.legend()

def fit_PolyH(distrib, Xmean, ax, deg=3): #remember to move Xmean+-0.001
    #fit is preformed after distrib is stripper of zeroes
    distrib_nozero = remove_zeros(distrib)
    iMean=len(distrib_nozero[:,0]) - 1
    while (distrib_nozero[iMean,0] > Xmean) :
        iMean -= 1
    #interpolate data for smoother fit
    interp3 = interp1d(distrib_nozero[iMean:,0], distrib_nozero[iMean:,1], kind = "cubic")
    xfit = np.linspace(distrib_nozero[iMean,0], distrib_nozero[-1,0], 100, endpoint=False)
    pfit=np.poly1d(np.polyfit(xfit, interp3(xfit), deg))
    ax.plot(distrib_nozero[iMean:,0], pfit(distrib_nozero[iMean:,0]), 'r-', label="HIpoly")
    plt.legend()
       
    '''
    pfit=np.poly1d(np.polyfit(distrib[:iMean,0], distrib[:iMean,1], 5))
    ax.plot(distrib[:iMean,0], pfit(distrib[:iMean,0]))
    plot_sweep(distrib, ax, 0)
    '''