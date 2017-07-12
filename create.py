"""
Data processing script for binary data files.

Call in the directory of LBM input file and *.b_dat files.

Usage:
>>python create.py

Will produce *.h5 storage files as well as *.xmf files to 
be read by Paraview.
"""

from mpi4py import MPI
import math
import os
import numpy as np
from hdf5Helper import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import sys
sys.path.insert(1,'.')

# Read data from params.lbm
input_file_name = 'params.lbm'
input_data = open(input_file_name,'r')

latticeType = int(input_data.readline())
Num_ts = int(input_data.readline())
ts_rep_freq = int(input_data.readline())
Warmup_ts = int(input_data.readline())
plot_freq = int(input_data.readline())
Cs = float(input_data.readline())
rho_lbm = float(input_data.readline())
u_lbm = float(input_data.readline())
omega = float(input_data.readline())

Nx = int(input_data.readline())
Ny = int(input_data.readline())
Nz = int(input_data.readline())

Restart_flag = int(input_data.readline())

Lx_p = float(input_data.readline())
Ly_p = float(input_data.readline())
Lz_p = float(input_data.readline())

t_conv_fact = float(input_data.readline())
l_conv_fact = float(input_data.readline())
p_conv_fact = float(input_data.readline())

input_data.close()

#u_conv_fact = l_conv_fact/t_conv_fact;
u_conv_fact = t_conv_fact/l_conv_fact;
print("u_conv_fact = %8.3e \n"%u_conv_fact)
nnodes = Nx*Ny*Nz

# compute geometric data only once
x = np.linspace(0.,Lx_p,Nx).astype(np.float64);
y = np.linspace(0.,Ly_p,Ny).astype(np.float64);
z = np.linspace(0.,Lz_p,Nz).astype(np.float64);
numEl = Nx*Ny*Nz
Y,Z,X = np.meshgrid(y,z,x);

XX = np.reshape(X,numEl)
YY = np.reshape(Y,numEl)
ZZ = np.reshape(Z,numEl)

# compute the number of data dumps I expect to process
nDumps = (Num_ts-Warmup_ts)/plot_freq + 1 # initial data plus Num_ts/plot_freq updates

for i in range(rank,nDumps,size):
  rho_fn = 'density'+str(i)+'.b_dat'
  ux_fn = 'ux'+str(i)+'.b_dat'
  uy_fn = 'uy'+str(i)+'.b_dat'
  uz_fn = 'uz'+str(i)+'.b_dat'

  ux = np.fromfile(ux_fn,dtype=np.float32)
  uy = np.fromfile(uy_fn,dtype=np.float32)
  uz = np.fromfile(uz_fn,dtype=np.float32)
  pressure = np.fromfile(rho_fn,dtype=np.float32)

  # convert velocity to physical units
  ux /= u_conv_fact
  uy /= u_conv_fact
  uz /= u_conv_fact
  pressure /= p_conv_fact # please check this...
  h5_file = 'out'+str(i)+'.h5'
  xmf_file = 'data'+str(i)+'.xmf'
  dims = (Nz,Ny,Nx)

  writeH5(pressure,ux,uy,uz,h5_file)
  writeXdmf(dims,xmf_file,i)
