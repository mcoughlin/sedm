
import os, sys
import glob

spectraDir = '../spectra'
filenames_all = glob.glob('%s/*.ascii'%(spectraDir))
names = []

for filename in filenames_all:
    filenameSplit = filename.replace(".ascii","").split("/")[-1].split("_")

    if len(filenameSplit) == 6:
        objectname, objecttype, mag, date, telescope = filenameSplit[0], filenameSplit[1], filenameSplit[2], filenameSplit[3], filenameSplit[4]
    elif len(filenameSplit) == 5:
        objectname, mag, date, telescope = filenameSplit[0], filenameSplit[1], filenameSplit[2], filenameSplit[3]
    names.append(objectname)

names = list(set(names))

for name in names:
    system_command = "python plot_spectra.py --doSpec --name %s"%name
    os.system(system_command)


