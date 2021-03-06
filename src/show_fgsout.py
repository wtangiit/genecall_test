#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
'''
Sn = TP/P = TP/(TP + FN +WF), 
Sp = TN/F = TN/(TN + FP), 
PPV = TP/(TP + FP +WF), w
here Ntot = TP + TN + FP + FN +WF.
'''

__helpmsg__ = "Usage: show_fgsout.py test1.table.csv test2.table.csv test3.table.csv ...\n"

linestyles1 = ['-v', '-or', '-dk', '->k', '-1m', '-^g', '-', '-', '-', '-']

#FILTERED = ['A1','A2','A3']
FILTERED = ['BA','BP','BS','CJ','CT','EC','HP','PA','PM','WE']
#FILTERED = ['A1','A2','A3','BA','BP','BS','CJ','CT','EC','HP','PA','PM','WE']

def plotline(ax, x, output, linestyles):
    lines = ax.plot(x, output, linestyles, linewidth=PLOTWIDTH, markeredgewidth=1, markersize=8)
    return lines

GRID_LINEWIDTH = 0.6
GRID_ALPHA = 0.3
PLOTWIDTH = 1.4

def parse_table(filename):
#stem TN2 TP N2 FP WF N P total  
#A1-0p2-075  csv 335    3408    553    229    475         564    4436    5000  
    infile = open(filename, "r")
    record_list = []
    training_set = filename.split(".")[0]
    for line in infile:
        record = {}
        line = line.strip()
        columns = line.split()
        sub_columns = columns[0].split("-")
        record['genome'] = sub_columns[0]
        
        if record['genome'] not in FILTERED:
            continue
        
        record['error'] = sub_columns[1]
        record['length'] = sub_columns[2]
        record['TN2'] = columns[2]
        record['TP'] = columns[3]
        record['N2'] = columns[4]
        record['FP'] = columns[5]
        record['WF'] = columns[6]
        record['N'] = columns[7]
        record['P'] = columns[8]
        record['total'] = columns[9]
        record['train'] = training_set

        record_list.append(record)
    return record_list

def get_sensitivity_by_error_train(rec_list, error_rate, train):
    '''return a list of sensitivity of given error_rate and train, ordered by length'''
    length_values = ['075', '100', '150', '200', '300', '400', '600', '1000']
    valid_recs = {}

    for rec in rec_list:
        if rec["error"] == error_rate and rec["train"] == train:
            length = rec["length"]
            if valid_recs.has_key(length):
                valid_recs[length].append(rec)
            else:
                valid_recs[length] = [rec]
     
    sens_list = []    
    for length in length_values:
        recs = valid_recs[length]
        total_tp = 0
        total_p = 0
        for rec in recs:
            total_tp += float(rec["TP"])
            total_p += float(rec["P"])
        sens = total_tp / total_p
        sens_list.append(sens)
    
    return sens_list
        

def plot_sensitivity(rec_list, error_rate):
   
    fig_type = "error"
    legend_type = "train"
    x_type = "length"
    x_values = [075, 100, 150, 200, 300, 400, 600, 1000]
    x_labels = [0, 200, 400, 600, 800, 1000]
    
    train_list = []
    for names in infile_names:
        train = names.split(".")[0]
        train_list.append(train)
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_ylabel('sensitivity')
    ax.set_xlabel("length of reads")
    ax.set_title('error rate %s' % error_rate)
    ax.set_xticklabels(x_labels)
    
    plot_things = []
    plot_labels = []
    legend_labels = []
    i = 0
    for train in train_list:
        sens_list = get_sensitivity_by_error_train(rec_list, error_rate, train)
        plots = plotline(ax, x_values, sens_list, linestyles1[i])
        plot_things.append(plots)
        plot_labels.append(plots[0])
        legend_labels.append(train)
        i += 1
        
    ax.legend(tuple(plot_labels), tuple(legend_labels), loc=0)

    ax.set_ylim(ymin=0, ymax=1)
    ax.set_yticks([0.1 * x for x in range(11)])
    ax.yaxis.grid(True, linestyle='-', which='major', alpha=GRID_ALPHA, linewidth=GRID_LINEWIDTH)
    ax.xaxis.grid(True, linestyle='-', which='major', alpha=GRID_ALPHA, linewidth=GRID_LINEWIDTH)
    plt.savefig("sensitivity-%s" % error_rate)


if __name__ == '__main__':    
    if len(sys.argv) == 1:
        print __helpmsg__
        sys.exit(1)
        
    bins = {}
    infile_names = []
    
    error_lists = ["0p0", "0p2", "0p5", "2p3"]
    
    total_pairs = 0
    
    for i in range(1, len(sys.argv)):
        infile_names.append(sys.argv[i])
        
    print infile_names
    
    rec_list = []
    for filename in infile_names:
        records = parse_table(filename)
        rec_list.extend(records)
  
    for error_rate in error_lists:
        plot_sensitivity(rec_list, error_rate)
 
    
    