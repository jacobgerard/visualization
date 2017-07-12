import os
import numpy as np
from hdf5Helper import *

rho = 'pressure.bin'
x = 'ux.bin'
y = 'uy.bin'
z = 'uz.bin'
 
pressure = np.fromfile(rho,dtype=np.float32)
unp = np.fromfile(x,dtype=np.float32)
vnp = np.fromfile(y,dtype=np.float32)
wnp = np.fromfile(z,dtype=np.float32)

print "Length of pressure is",len(pressure)
print "Length of pressure is",len(unp)
print "Length of pressure is",len(vnp)
print "Length of pressure is",len(wnp)

xmf_file = raw_input('XDMF Filename: ')
dims = (91,19,19)

writeH5(pressure,unp,vnp,wnp)
writeXdmf(dims,xmf_file)
