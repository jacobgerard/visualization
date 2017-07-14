This visualization repository is used in the post-processing of binary data files from Numeric Fluid Channel calculations.
It creates HDF5 and XDMF files that allow Paraview to use multiple processes while visualizing the data.

The code is in Python and takes advantage of features in the numpy and h5py packages. In order to run the script ensure that both
are installed.

If h5py is not available in the python modules (as is the case on Shepard) you should run an Anaconda version of python 2.7. Setup
for this is in the steps below.

1. Install Anaconda to your home directory. 
2. Put Anaconda's bin directory on the front of your path.
3. Ensure that numpy and h5py are installed in Anaconda. If they are not or you would like to check, run the commands "conda install
numpy" and "conda install h5py".

When the time comes to run the post-processing script, place both processNFC.py and hdf5Helper.py in the same directory as the 
binary data files. Ensure that Anaconda's python is running (if the bin directory is on your path in the ~/.bashrc file then just 
run "source ~/.bashrc"). Then run the script with the command "python processNFC.py". This will take a little while but eventually
output a number of *.h5 and *.xmf files. 

You can open all of the output datasets at once in Paraview by selecting the *xmf files. It should run on any number of nodes and 
processes. You can see the way Paraview split the data by viewing a slice of vtkProcessID. If there are any issues just let me know.
