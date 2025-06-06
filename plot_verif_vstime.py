###########################################################
### plot score with respect to time for each experiment ###
### multiple centers can be inluded on one plot         ###
###########################################################

import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# adjust parameters in this section
## ---------------------------------------------------------------------------------
centers = ['Met_Office'] # list of centers to include on the plot. Should be named as in the directories containing  the statistics files
plot_levs = ['100hpa'] # list of levels to plot. Each level will be plotted seprately 

plot_scores = ['sd'] # list of scores to plot. Each score will be plotted seprately
# possible options:
# sd: standard deviation, me: mean error, mae: mean absolute error, rmse: root mean square error

plot_expts = ['Control_NewOp', 'AllObs_NewOp', 'My_20k_NewOp', 'Control-C2_NewOp'] # list of experiments to include
# this should be given as the name of the files without the '_stats.txt' (or '_stats_obs.txt') see for example line 51

ref = 'ob' # reference stats are calculated with respect to
# possible options:
# ob: observation, an: analysis, ecmf: ECMWF reanalysis
## ---------------------------------------------------------------------------------

for center in centers:
    files = os.listdir(f'{center}/')
    expts = []
    for f in files:
        name = f.split('.')[0]
        ex = name.split('_')
        if 'stats' not in ex:
            continue
        else:
            if ex[0] == 'OLD':
                continue
            if (ex[-1] == 'an' and ref == 'ob') or (ex[-1] == 'ob' and ref == 'ecmf'):
                continue
            expt = '_'.join(ex[:ex.index('stats')])
            if plot_expts[0] != 'all' and expt not in plot_expts:
                continue
            expts.append(expt)

# ensure control expt is at the front of list
expts.insert(0, expts.pop(expts.index('Control')))

timeSeriesVals = {}
for center in centers:
    for expt in expts:
        if center == 'METEO-FRANCE':
            if ref == 'ob':
                statfile = f'{center}/{expt}_stats_obs.txt'
            else:
                statfile = f'{center}/{expt}_stats_an.txt'
        else:
            statfile = f'{center}/{expt}_stats.txt'
        with open(statfile, 'r', newline='') as file:
            read = csv.reader(file, delimiter=',')
            nrow = 0
            for row in read:
                nrow +=1
                if len(timeSeriesVals.keys()) == 0:
                    head = row
                    timeSeriesVals = dict((key,[]) for key in head)
                    timeSeriesVals['expt'] = []
                    timeSeriesVals['center'] = []
                else:
                    if row[0] == 'centre': # don't save header row to data
                        continue
                    for i, h in enumerate(head):
                        timeSeriesVals[h].append(row[i])
                    timeSeriesVals['expt'].append(expt)
                    timeSeriesVals['center'].append(center)
            file.close()

linestyles = ['-', ':', '--', '-.']
colors = ['r', 'b', 'y', 'darkviolet', 'k', 'sienna']i
numbers = {'Control': 10, 'NoRO': 0, 'AllObs': 35, 'Control-C2': 6, 'My_20k': 20}
scores = {'rmse': 'Root Mean Squared Error', 'me': 'Mean Error', 'mae': 'Mean Absolute Error', 's1': 'S1 Skill Score', 'ccaf': 'Forecast Anomaly Correlation', 'cctf': 'Forecast Tendancy Correlation', 'rmsaf': 'Root Mean Square of Forecast Anomaly', 'rmsav': 'Root Mean Square of Verifying Analysis Anomaly', 'seeps': 'SEEPS', 'sd': 'Standard Deviation'}
var = {'r': 'Relative Humidity', 't': 'Temperature', 'w': 'Wind Speed', 'z': 'Geopotential Height'}
reg = {'nhem': 'Northern Hemisphere', 'shem': 'Southern Hemisphere', 'tropics': 'Tropics'}

all_params = np.unique(np.asarray(timeSeriesVals['par']))
params = []
for param in all_params:
    if param[0] == 'm':
        params.append(param)
    else:
        if param[0] == 'r' or param[0] == 'w':
            lev = param[2:]
        else:
            lev = param[1:]

        if lev not in plot_levs:
            continue
        params.append(param)

for center in centers:
    cid = np.asarray(timeSeriesVals['center']) == center
    ctmp = np.unique(np.asarray(timeSeriesVals['par'])[cid])
    for param in params:
        if param not in ctmp:
            print(f'Parameter {param} not availiable for {center}. Skipping')
            params.remove(param)

    ctmp = np.unique(np.asarray(timeSeriesVals['sc'])[cid])
    for score in plot_scores:
        if score not in ctmp:
            print(f'Score {score} not availiable for {center}. Skipping')
            plot_scores.remove(score)

plotnum = 0
totplot = (len(params) * len(plot_scores) * 2 * 3)
for param in params:
    for score in np.unique(np.asarray(timeSeriesVals['sc'])):
        if score not in plot_scores:
            continue
        for r, region in enumerate(np.unique(np.asarray(timeSeriesVals['dom']))):
            fig, ax = plt.subplots()
            fig2, ax2 = plt.subplots()
            ax_lab = ax.twinx()
            ax_lab.get_yaxis().set_visible(False)
            ax2.axhline(y=0, color='lightgrey', ls=':')
            ax.set_ylabel(scores[score])
            ax2.set_ylabel(scores[score] + ' Reduction (%)')
            ax.set_xlabel('Forecast Hour')
            ax2.set_xlabel('Forecast Hour')
            if param[0] == 'm':
                fig.suptitle('Mean Sea Level Pressure '+ scores[score] + '\n' + reg[region] + ' Reference: ' + ref)
                fig2.suptitle('Mean Sea Level Pressure '+ scores[score] + ' Reduction' + '\n' + reg[region] + ' Reference: ' + ref)
            else:
                if param[0] == 'r' or param[0] == 'w':
                    lev = param[2:]
                else:
                    lev = param[1:]

                if lev not in plot_levs:
                    continue
    
                fig.suptitle(lev + ' ' + var[param[0]] + ' ' + scores[score] + '\n' + reg[region] + ' Reference: ' + ref)
                fig2.suptitle(lev + ' ' + var[param[0]] + ' ' + scores[score] + ' Reduction' + '\n' + reg[region] + ' Reference: ' + ref)
            for c, center in enumerate(centers):
                for e, expt in enumerate(expts):
                    lid = (np.asarray(timeSeriesVals['par']) == param) & (np.asarray(timeSeriesVals['sc']) == score) & (np.asarray(timeSeriesVals['dom']) ==  region) & (np.asarray(timeSeriesVals['expt']) == expt) & (np.asarray(timeSeriesVals['ref']) == ref) & (np.asarray(timeSeriesVals['center']) == center)
                    vals = np.asarray(timeSeriesVals['v'])[lid].astype(float)
                    time = np.asarray(timeSeriesVals['s'])[lid].astype(int)

                    #if not shortest:
                    #        shortest = time[-1]
                    #if time[-1] < shortest:
                    #    shortest = time[-1]

                    if expt == 'Control':
                        base = vals

                    if c == 0:
                        label = expt
                    else:
                        label = ''

                    ind = time <= 140
                    print(linestyles[c],colors[e])
                    ax.plot(time, vals, label=label, ls=linestyles[c], color=colors[e])
                    if expt != 'Control':
                        label = expt + '_' +center
                        ax2.plot(time, (base - vals)/base * 100, label=label, color=colors[e], ls=linestyles[c])
    
                    if len(centers) > 1:
                        if e == 0:
                            label = center
                        else:
                            label = ''
                        ax_lab.plot(np.NaN, np.NaN, color='k', label=label, ls=linestyles[c])
            ax2.legend()
            ax.legend(loc=1)
            ax.set_xlim(0, 140)
            ax2.set_xlim(0, 140)
            if len(centers) > 1:
                ax_lab.legend(loc=2)
                if not os.path.exists(f'Comparison_Plots'):
                    os.makedirs(f'Comparison_Plots')
                cent_names = '-'.join(centers)
                plot_name = f'Comparison_Plots/{cent_names}_{param}_{score}_{ref}_{region}.png'
                plot_name_red = f'Comparison_Plots/{cent_names}_{param}_{score}_{ref}_{region}_reduction.png'
            else:
                if not os.path.exists(f'{centers[0]}_Plots'):
                    os.makedirs(f'{centers[0]}_Plots')
                plot_name = f'{centers[0]}_Plots/{centers[0]}_{param}_{score}_{ref}_{region}.png'
                plot_name_red = f'{centers[0]}_Plots/{centers[0]}_{param}_{score}_{ref}_{region}_reduction.png'

            fig.savefig(plot_name)
            plotnum += 1
            print(f'Saving: {plot_name} {plotnum}/{totplot}')
            fig2.savefig(plot_name_red)
            plotnum += 1
            print(f'Saving: {plot_name_red} {plotnum}/{totplot}')
            plt.close(fig)
            plt.close(fig2)
