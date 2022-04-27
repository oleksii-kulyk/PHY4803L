# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 21:38:33 2022

@author: Oleksiy
"""
from to_distribution import *
from fit_Curve import *
from stats import *
import csv

Output_Data = [["Data Set Name" ,"HI - LO mean: V", "HI - LO uncertainty: V", "LOW mean: V", "LOW uncertainty: V", "HIGH mean: V", "HIGH uncertainty: V"]]

# process up to dataset 72
for i in range (73):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    filename = "../final data/ALL{0:04d}/A{0:04d}CH1.CSV".format(i)
    print(filename)
    distrib, Xmean = delta_sweep(filename, 0.001)
    plot_sweep(distrib, ax, i)
    distrib_nozero = remove_zeros(distrib)
    
    idxHI_Max = HI_max(distrib_nozero, Xmean, ax)
    idxIsoSig = plotIsolatedSignal(distrib_nozero, idxHI_Max, ax, 'red', "HIGH", 10)
    HImean, HIerror = plotStdErr(distrib_nozero, idxIsoSig, idxHI_Max, ax, "HIGH:")
    HI = mes.Measurement(HImean, HIerror)
    
    idxLO_Max = LO_max(distrib_nozero, Xmean, ax)
    idxIsoSig = plotIsolatedSignal(distrib_nozero, idxLO_Max, ax, 'blue', "LOW", 11)
    LOmean, LOerror = plotStdErr(distrib_nozero, idxIsoSig, idxLO_Max, ax, "LOW:")
    LO = mes.Measurement(LOmean, LOerror)
    
    delta = plotDelta(LO, HI, distrib, ax)
    
    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    plt.savefig("PlotsFinal/A{0:04d}CH1.pdf".format(i), bbox_extra_artists=(lgd,), bbox_inches='tight', format="pdf")
    datasetname = "A{0:04d}CH1".format(i)
    Output_Data.append([datasetname, delta.val, delta.unc, LO.val, LO.unc, HI.val, HI.unc])
    plt.show()
    plt.clf()

        
# process datasets 73 and 74 separately

#Dataset 73:
fig = plt.figure()
ax = fig.add_subplot(111)
filename = "../final data/ALL0073/A0073CH1.CSV"
print(filename)
distrib, Xmean = delta_sweep(filename, 0.001)
plot_sweep(distrib, ax, 73)
distrib_nozero = remove_zeros(distrib)

idxHI_Max = HI_max(distrib_nozero, Xmean, ax)
idxIsoSig = plotIsolatedSignal(distrib_nozero, idxHI_Max, ax, 'red', "HIGH", 10)
HImean, HIerror = plotStdErr(distrib_nozero, idxIsoSig, idxHI_Max, ax, "HIGH:")
HI = mes.Measurement(HImean, HIerror)

idxLO_Max = LO_max(distrib_nozero, Xmean, ax)

#idxIsoSig = plotIsolatedSignal(distrib_nozero, idxLO_Max, ax, 'blue', "LOW", 11) is replaced by
idxsIsoSig = np.array((1,2,3,4,5,6,7,8,9,10))
ax.scatter(distrib_nozero[idxsIsoSig,0], distrib_nozero[idxsIsoSig,1], s=80, c='blue', label="LOW", marker=11)

LOmean, LOerror = plotStdErr(distrib_nozero, idxIsoSig, idxLO_Max, ax, "LOW:")
LO = mes.Measurement(LOmean, LOerror)

delta = plotDelta(LO, HI, distrib, ax)

lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
plt.savefig("PlotsFinal/A0073CH1.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight', format="pdf")
datasetname = "A0073CH1"
Output_Data.append([datasetname, delta.val, delta.unc, LO.val, LO.unc, HI.val, HI.unc])
plt.show()
plt.clf()


#Dataset 74:
fig = plt.figure()
ax = fig.add_subplot(111)
filename = "../final data/ALL0074/A0074CH1.CSV"
print(filename)
distrib, Xmean = delta_sweep(filename, 0.001)
plot_sweep(distrib, ax, 74)
distrib_nozero = remove_zeros(distrib)

idxHI_Max = HI_max(distrib_nozero, Xmean, ax)
idxIsoSig = plotIsolatedSignal(distrib_nozero, idxHI_Max, ax, 'red', "HIGH", 10)
HImean, HIerror = plotStdErr(distrib_nozero, idxIsoSig, idxHI_Max, ax, "HIGH:")
HI = mes.Measurement(HImean, HIerror)

idxLO_Max = LO_max(distrib_nozero, Xmean, ax)

#idxIsoSig = plotIsolatedSignal(distrib_nozero, idxLO_Max, ax, 'blue', "LOW", 11) is replaced by
idxsIsoSig = np.array((1,2,3,4,5,6,7,8,9,10))
ax.scatter(distrib_nozero[idxsIsoSig,0], distrib_nozero[idxsIsoSig,1], s=80, c='blue', label="LOW", marker=11)

LOmean, LOerror = plotStdErr(distrib_nozero, idxIsoSig, idxLO_Max, ax, "LOW:")
LO = mes.Measurement(LOmean, LOerror)

delta = plotDelta(LO, HI, distrib, ax)

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
plt.savefig("PlotsFinal/A0074CH1.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight', format="pdf")
datasetname = "A0074CH1"
Output_Data.append([datasetname, delta.val, delta.unc, LO.val, LO.unc, HI.val, HI.unc])
plt.show()
plt.clf()

# write results to a file
with open('Analyzed Data.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')
    for i in range(len(Output_Data)) :
        datawriter.writerow(Output_Data[i])
    
    
'''
#fit_PolyL(distrib, Xmean + 0.001, ax, deg=5)
#fit_PolyH(distrib, Xmean - 0.001, ax, deg=5)
#fit_GaussL(distrib, Xmean + 0.001, ax)
#fit_GaussH(distrib, Xmean - 0.001, ax)
"A{0:04d}CH1".format(i)
ax.set(xlim=(0.02, xmax), ylim=(ymin, ymax))

f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
f.close()

TODO
increase the size pf graphs so they are not cut off when saved.
Submit the new graphs to webcources.
'''