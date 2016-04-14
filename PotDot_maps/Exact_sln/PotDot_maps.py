import sys
import numpy
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib import cm

i = sys.argv[1]
a = sys.argv[2]

i = int(i)
a = int(a)

print "argument 1:", i
print "argument 2:", a


#****************************************************************************************************
#***** Reading data *****
#****************************************************************************************************
#/home/dvalencia/Processed_data_from_CIC/Snap150/NGrid512/CIC/DenCon_Poten_PotDots.dat
print "Reading data"
BoxSize = 400.0
SliceSize = 10.0
NCells = 512.0

#----- Height and width of figures -----
height = 10
width = 12.9

pos_x_us, pos_y_us, pos_z_us, PotDot_us = numpy.loadtxt("unsorted_slice_z_%dto%s.dat"%(i,a), usecols=(0,1,2,3), unpack=True) #_us is unsorted data!



#****************************************************************************************************
#***** Unsorted data *****
#****************************************************************************************************

#+++++ Sorting by index +++++
"""                                                                                                         
***** Sorting by index *****                                                                                
Here we sort by index the data from PotDot_us and create the array sort_index with the                      
values of the indices. Then, using the array sort_index as argument of pos_x_us we can                      
create an array x_s with the values of positions in x that correspond with the sorted                       
index according to the values of PotDot!                                                                    
"""

print "Sorting data"
sort_index = numpy.argsort(PotDot_us)
print "Data sorted!"

x_s = pos_x_us[sort_index]
y_s = pos_y_us[sort_index]
z_s = pos_z_us[sort_index]
#PotDot_s_raw = PotDot_us[sort_index]
PotDot_s = PotDot_us[sort_index]

#PotDot_s = PotDot_s_raw + numpy.abs(PotDot_s_raw.min()) + 1.0e-8
print "Data rescaled"

print PotDot_s.min()
print PotDot_s.max()

print "Freeing up memory"
del pos_x_us
del pos_y_us
del pos_z_us
del PotDot_us
#del PotDot_s_raw


#****************************************************************************************************
#***** Plotting with scatter *****
#****************************************************************************************************

print "Plotting"
pyplot.close()
pyplot.figure(figsize=(width,height))

cmap = 'RdBu_r'
#norm = matplotlib.colors.Normalize(vmin=1.0e7,vmax=1.5e9)
norm = matplotlib.colors.LogNorm(vmin=1.0e7,vmax=1.5e9)

pyplot.scatter(x_s, y_s, s=5, c=numpy.abs(PotDot_s), cmap=cmap , edgecolors='none', marker='s', norm=norm)
#pyplot.scatter(x_s, y_s, s=5, c=numpy.abs(PotDot_s), cmap=pyplot.cm.jet , edgecolors='none', norm=matplotlib.colors.LogNorm(vmin=PotDot_s.min(), vmax=0.5*PotDot_s.max()), marker='s') #This works!
pyplot.xlim(0.0,BoxSize)
pyplot.ylim(0.0,BoxSize)
pyplot.xlabel(r"Comoving distance $x$ [$h^{-1}$Mpc]")
pyplot.ylabel(r"Comoving distance $y$ [$h^{-1}$Mpc]")
pyplot.title(r"$\dot{\Phi}(\vec{r})$ for $%d \leq z < %d$"%(i,a))
pyplot.colorbar()

pyplot.savefig("PotDot_full_z_from_%dto%d.png"%(i,a))
#pyplot.show()
