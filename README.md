Python scripts to produce plots of ROMEX verification scores for different centers

**Scripts:**
plot_verif_vsCount.py: produces plots of score reduction with respect to a control experiment
plot_verif_vstime.py: produces plots of scores with respect to forecast time

**Directories:**
The names of the directories refer to the centers. Files inside are named by experiment and have been renamed for inter-center consistancy. Some files have been slightly modified for formatting consistancy

Plots for a single center will be written to _centerName_ _plots/ directories. Plots with multiple centers plotted together will be written to comparison_plots/ . If these directories do not exist, they will be created

**To run:**
Adjust parameters at the top of the script as required. A description of each parameter and how to set them is provided in the comments within each script. The scripts should be run within the typical skylab python virtual environment to ensure access to all the necessary packages. (This may not be necessary, but I haven't tested it). No extra arguments are required on the command line, so the scripts are run as python plot_verif_vsCount.py
# romex_verification
