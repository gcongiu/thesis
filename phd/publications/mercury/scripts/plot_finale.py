
"""
Created on Sun May  4 12:18:00 2014

@author: Federico
"""

"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json

#no sliding window


def read_mean_runtime(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        mean_runtime = findings["mean_runtime"]
        return mean_runtime


def read_std_runtime(path_file):
    with open(path_file, 'r') as f:
        findings = json.load(f)
        std = findings["standard_dev"]
        return std


if __name__ == "__main__":

    print("please provide the 6+3+6=15 files with the results to plot in the given order!!!")
    print(" ############## TEST CLUSTER  #####################################")
    print("Test cluster results: local_fs_noAM, local_fs_AM_target_conf, local_fs_willneedAll")
    print("Test cluster results: lustre_fs_noAM, lustre_fs_AM_target_conf, lustre_fs_willneedAll")
    print("Test cluster results: gpfs_fs_noAM, gpfs_fs_AM_target_conf, gpfs_fs_willneedAll")
    print(" ############## MOGON CLUSTER  #####################################")
    print("Mogon cluster results: local_fs_noAM, local_fs_AM_target_conf, local_fs_willneedAll")
    print("Mogon cluster results: gpfs_fs_noAM, gpfs_fs_AM_target_conf, gpfs_fs_willneedAll")

    parser = argparse.ArgumentParser(description='This script generates the final plot of runtime. Please provide the list of 15 files to process as input!', version='0.0')
    parser.add_argument('-i', '--input', action='append', dest='collection', default=[], help='Add repeated values to a list of input files to be processed', required=True)
    parser.add_argument('-o', '--outputfile', help='output pdf (or other image format) file with plot of the execution times', required=True)
    args = parser.parse_args()

    all_runtimes = []
    all_runtimes_std = []

    for name in args.collection:
        mean_run = read_mean_runtime(name)
        all_runtimes.append(mean_run)

    for name in args.collection:
        mean_std = read_std_runtime(name)
        all_runtimes_std.append(mean_std)

    n_groups = 3


    #### local, Lustre, GPFS

    ##### Test cluster

    # single client, no AM
    means_noAM = (all_runtimes[0], all_runtimes[3], all_runtimes[6])
    std_noAM = (all_runtimes_std[0], all_runtimes_std[3], all_runtimes_std[6])

    #############################

    # single client, no sliding window, target config

    means_goodconf = (all_runtimes[1], all_runtimes[4], all_runtimes[7])
    std_goodconf = (all_runtimes_std[1], all_runtimes_std[4], all_runtimes_std[7])

    #############################


    # single client, sliding window

    means_slw = (all_runtimes[2], all_runtimes[5], all_runtimes[8])
    std_slw = (all_runtimes_std[2], all_runtimes_std[5], all_runtimes_std[8])

    #############################

    ##### Mogon

    # single client, no AM

    mogon_means_noAM = (all_runtimes[9], 0, all_runtimes[12])
    mogon_std_noAM = (all_runtimes_std[9], 0, all_runtimes_std[12])

    #############################

    # manca mogon local no sliding window

    # single client, no sliding window, target config

    mogon_means_goodconf = (all_runtimes[10], 0, all_runtimes[13])
    mogon_std_goodconf = (all_runtimes_std[10], 0, all_runtimes_std[13])

    #############################

    # single client, sliding window

    mogon_means_slw = (all_runtimes[11], 0, all_runtimes[14])
    mogon_std_slw = (all_runtimes_std[11], 0, all_runtimes_std[14])

    #############################


    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.12

    error_config = {'ecolor': '0'}

    rects1 = plt.bar(index - 3*bar_width, means_noAM, bar_width,
                     #alpha=opacity,
                     color='0',
                     yerr=std_noAM,
                     error_kw=error_config,
                     label='w/o AM - Test'
                     )

    rects2 = plt.bar(index - 2*bar_width, means_slw, bar_width,
                     #alpha=opacity,
                     color='0.2',
                     yerr=std_slw,
                     error_kw=error_config,
                     label='w/ AM, WillNeed all file - Test')#,
                     #hatch='xx')


    rects3 = plt.bar(index - 1*bar_width, means_goodconf, bar_width,
     #                #alpha=opacity,
                     color='0.4',
                     yerr=std_goodconf,
                     error_kw=error_config,
                     label='w/ AM, Tailored config file - Test'
                     )

    rects4 = plt.bar(index + 0.5*bar_width, mogon_means_noAM, bar_width,
                     #alpha=opacity,
                     color='0.6',
                     yerr=mogon_std_noAM,
                     error_kw=error_config,
                     label='w/o AM - Mogon'
                     )

    rects5 = plt.bar(index + 1.5*bar_width, mogon_means_slw, bar_width,
                     #alpha=opacity,
                     color='0.8',
                     yerr=mogon_std_slw,
                     error_kw=error_config,
                     label='w/ AM, WillNeed all file - Mogon')#,
                     #hatch='xx')

    rects6 = plt.bar(index + 2.5*bar_width, mogon_means_goodconf, bar_width,
     #                #alpha=opacity,
                     color='1',
                     yerr=mogon_std_goodconf,
                     error_kw=error_config,
                     label='w/ AM, Tailored config file - Mogon'
                     )



    ax.set_ylim([0, 270])
    #plt.grid()
    #plt.xlabel('File systems', fontsize=15, verticalalignment='bottom')
    #plt.xlabel('File systems')
    plt.ylabel('Execution time [sec]', fontsize=15)
    plt.yticks(fontsize=12)
    #plt.title('Execution time')
    start, end = ax.get_ylim()
    #ax.yaxis.set_ticks(np.arange(start, end, 10))
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)
    plt.xticks(index, ('ext4', 'Lustre', 'GPFS'), fontsize=15)
    #plt.legend(loc='upper center', fontsize=10)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5,1.3), ncol=2, fontsize=10)
    #plt.tight_layout()
    plt.subplots_adjust(top=.77)
    #plt.show()
    plt.savefig(args.outputfile)