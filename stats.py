# -*- coding: utf-8 -*-

'''This module looks for the peaks in the signal. Then splits the signal into a HIGH and a LOW based on the peaks. After which standard statistical analysis is preformed.'''

import numpy as np
import matplotlib.pyplot as plt
import measure as mes
from to_distribution import *

def LO_max(distrib, Xmean, ax): #remember to move Xmean+0.001
    iMean=0
    while (distrib[iMean,0] < Xmean) :
         iMean += 1
    LO_Max = np.max(distrib[:iMean,1])
    idxLO_Max = np.where(distrib[:,1] == LO_Max)
    xval = distrib[idxLO_Max[0],0]
    #ax.scatter(xval[0], LO_Max, marker="X",c='violet')
    #ax.legend()
    return idxLO_Max[0][0]
         
def HI_max(distrib, Xmean, ax): #remember to move Xmean-0.001
    iMean=len(distrib[:,0]) - 1
    while (distrib[iMean,0] > Xmean) :
        iMean -= 1
    HI_Max = np.max(distrib[iMean:,1])
    idxHI_Max = np.where(distrib[:,1] == HI_Max)
    xval = distrib[idxHI_Max[0],0]
    #ax.scatter(xval[-1], HI_Max, marker="X",c='black')
    #ax.legend()
    return idxHI_Max[0][-1]

def plotIsolatedSignal(distrib, idxMax, ax, color, label, marker):
    idxsIsoSig = np.array([idxMax])
    #isolating left
    i = idxMax
    while True :
        if not(i > 0) :
            break
        elif (distrib[i-1,1] < distrib[i,1]) :
            idxsIsoSig = np.append(idxsIsoSig, i-1)
            i -= 1
        else : break
    #isolating right
    i = idxMax
    while True :
        if not(i < len(distrib[:,1]) - 1) :
            break
        elif (distrib[i+1,1] < distrib[i,1]) :
            idxsIsoSig = np.append(idxsIsoSig, i+1)
            i += 1
        else : break
    idxsIsoSig = np.sort(idxsIsoSig)
    #plot isolated signal    
    ax.scatter(distrib[idxsIsoSig,0], distrib[idxsIsoSig,1], s=80, c=color, label=label, marker=marker)
    #ax.legend()
    return idxsIsoSig

def plotDelta(LO, HI, distrib, ax):
    #measure.py is used here
    delta = HI - LO
    text = "{0:.3g}±{1:.3g} mV".format(delta.val*1000, delta.unc*1000)
    ax.text(np.mean(distrib[:,0]), np.mean(distrib[:,1]) + 50, text)
    return delta

def plotStdErr(distrib, idxIsoSig, idxMax, ax, peakname):
    mean = meanDistrib(distrib, idxIsoSig)
    error = stdErrDistrib(distrib, idxIsoSig)
    text = ("{2:} {0:.3g}±{1:.3g} mV").format(mean*1000, error*1000, peakname)
    ax.text(distrib[idxMax,0], distrib[idxMax,1] + 50, text)
    return mean, error

def stdErrDistrib(distrib, idxIsoSig):
    totalnum = 0
    for i in idxIsoSig :
        totalnum += distrib[i,1]
    stdErr = stddevDistrib(distrib, idxIsoSig) / np.sqrt(totalnum)
    return stdErr
    
def stddevDistrib(distrib, idxIsoSig):
    totalnum = 0
    for i in idxIsoSig :
        totalnum += distrib[i,1]
    mean = meanDistrib(distrib, idxIsoSig)
    # a sample is assumed
    stddev = np.sum( distrib[idxIsoSig,1] * ( distrib[idxIsoSig,0] - mean )**2 ) / (totalnum - 1)
    return stddev
    
def meanDistrib(distrib, idxIsoSig):
    totalnum = 0
    for i in idxIsoSig :
        totalnum += distrib[i,1]
    mean = np.sum(distrib[idxIsoSig,0]*distrib[idxIsoSig,1]) / totalnum
    return mean