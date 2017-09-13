
import os, sys, glob
import optparse
import numpy as np

import matplotlib
#matplotlib.rc('text', usetex=True)
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 16})
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()
 
    parser.add_option("-p","--plotDir",default="../plots")
    parser.add_option("-s","--spectraDir",default="../spectra")

    parser.add_option("--name",default="16abc")
    parser.add_option("--doSpec",  action="store_true", default=False)

    opts, args = parser.parse_args()

    return opts

def read_files_spec(files):

    names = []
    specs = {}
    for filename in files:
        name = filename.replace(".ascii","").split("/")[-1]
        data_out = np.loadtxt(filename)
        lambda_d, spec_d = data_out[:,0], data_out[:,1]

        specs[name] = {}
        specs[name]["lambda"] = lambda_d
        specs[name]["data"] = spec_d

        names.append(name)

    return specs, names

# Parse command line
opts = parse_commandline()

spectraDir = opts.spectraDir

baseplotDir = opts.plotDir
plotDir = os.path.join(baseplotDir,"spectra",opts.name)
if not os.path.isdir(plotDir):
    os.mkdir(plotDir)

if opts.doSpec:

    filenames_all = glob.glob('%s/*.ascii'%(spectraDir))

    filenames = []
    legend_names = []
    for filename in filenames_all:
        filenameSplit = filename.replace(".ascii","").split("/")[-1].split("_")

        if len(filenameSplit) == 6:
            objectname, objecttype, mag, date, telescope = filenameSplit[0], filenameSplit[1], filenameSplit[2], filenameSplit[3], filenameSplit[4]
        elif len(filenameSplit) == 5:
            objectname, mag, date, telescope = filenameSplit[0], filenameSplit[1], filenameSplit[2], filenameSplit[3]

        if not objectname == opts.name: continue
        filenames.append(filename)
        legend_name = "%s: %s"%(telescope, date)
        legend_names.append(legend_name)
    specs, names = read_files_spec(filenames)

    maxhist = -1e10
    colors = ["g","r","c","y","m"]
    plotName = "%s/spec.pdf"%(plotDir)
    plt.figure(figsize=(12,10))
    for ii,name in enumerate(names):
        spec_d = specs[name]
        linestyle = "%s-"%colors[ii]
        plt.semilogy(spec_d["lambda"],spec_d["data"],linestyle,label=legend_names[ii],linewidth=2)
        maxhist = np.max([maxhist,np.max(spec_d["data"])])
 
    plt.xlim([3000,11000])
    #plt.ylim([10.0**39,10.0**43])
    plt.xlabel(r'$\lambda [\AA]$',fontsize=24)
    plt.ylabel('Fluence [erg/s/cm2/A]',fontsize=24)
    plt.legend(loc="best")
    plt.grid()
    plt.savefig(plotName)
    plt.close()

