import sys
import struct
import numpy
import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib import cm

"""
#To read from command line
i = sys.argv[1]
a = sys.argv[2]

i = int(i)
a = int(a)

print "argument 1:", i
print "argument 2:", a
"""

#****************************************************************************************************
#***** Reading data *****
#****************************************************************************************************
#/home/dvalencia/Processed_data_from_CIC/Snap150/NGrid512/CIC/DenCon_Poten_PotDots.dat
print "Reading data"
SliceSize = 10.0
NCells = 256.0

#----- Height and width of figures -----
height = 10
width = 12.9


#pos_x_us, pos_y_us, pos_z_us, DenCon_us = numpy.loadtxt("./../../../../../Data/Sn150/DenCon_Potential_PotDot_fields_k_full.dat", usecols=(1,2,3,7), unpack=True) #_us is unsorted data! 


with open("./../../../../../../Processed_data/NGrid256/DenCon_Pot_PotDot_fields_256.bin", 'rb') as bdata:
    header_size = 40 # in bytes
    bheader = bdata.read(40)
    print header_size
    header_data = struct.unpack('ddddd', bheader)
    BoxSize = header_data[0]
    Omega_L0 = header_data[1]
    Omega_M0 = header_data[2]
    z_RS = header_data[3]
    H0 = header_data[4]
    """
    For each particle I need 68 bytes: an int (4-bytes) for ID, 3 doubles (8-bytes each one) for 
    position, 1 double for DenCon, 1 double for Phi, 1 Double for PhiDot, 1 double for PhiDot_1
    and 1 double for PhiDot_2
    """
    print struct.calcsize('=idddddddd')
    print struct.calcsize('<idddddddd')
    print struct.calcsize('i')
    print struct.calcsize('d')
    bytes_per_part = 68 
    body_size = int( (NCells**3) * bytes_per_part )
    bsize = int( (NCells**3) )
    body_data_read = bdata.read(body_size)
    #body_data = struct.unpack_from('idddddddd', bdata, offset=40)
    #body_data = struct.unpack('=i d d d d d d d d', body_data_read)
    #body_data = struct.unpack('=i 8d', body_data_read)
    #body_data = struct.unpack('<i 8d', body_data_read)
    #body_data = struct.unpack('='+(bsize)*'i 8d', body_data_read)
    body_data = struct.unpack_from('='+(bsize)*'i 8d', body_data_read)
    
    #+++++ Unpacking positions ++++++
    ID_us = body_data[0]
    pos_x_bin = body_data[1::9]
    pos_y_bin = body_data[2::9]
    pos_z_bin = body_data[3::9]
    DenCon_bin = body_data[4::9]
    

    

print BoxSize, Omega_L0, Omega_M0, z_RS, H0
print len(pos_x_bin)
print type(pos_x_bin)

#+++++ Transforming returned tuples into numpy arrays +++++
#pos_x_us = list(pos_x_bin)
pos_x_us = numpy.asarray(pos_x_bin)
pos_y_us = numpy.asarray(pos_y_bin)
pos_z_us = numpy.asarray(pos_z_bin)
DenCon_us = numpy.asarray(DenCon_bin)

del pos_x_bin
del pos_y_bin
del pos_z_bin
del DenCon_bin


print len(pos_x_us)
print type(pos_x_us)
print pos_x_us



#****************************************************************************************************
#***** Unsorted data *****
#****************************************************************************************************


for i in range(40,400,int(SliceSize)):
    k = int(i + SliceSize)
    #+++++ Filtering data by its position in z +++++
    z_filter = numpy.logical_and( numpy.greater_equal(pos_z_us, i), numpy.less(pos_z_us, k ) )
    pos_x_filter = pos_x_us[z_filter]
    pos_y_filter = pos_y_us[z_filter]
    pos_z_filter = pos_z_us[z_filter]
    DenCon_filter = DenCon_us[z_filter]

    #+++++ Sorting by index +++++
    """                                                                                      
    ***** Sorting by index *****                                                                       
    Here we sort by index the data from PotDot_us and create the array sort_index with the                 
    values of the indices. Then, using the array sort_index as argument of pos_x_us we can      
    create an array x_s with the values of positions in x that correspond with the sorted          
    index according to the values of PotDot!                                      
    """

    print "Sorting data"
    sort_index = numpy.argsort(DenCon_filter)
    print "Data sorted!"
    
    x_s = pos_x_filter[sort_index]
    y_s = pos_y_filter[sort_index]
    z_s = pos_z_filter[sort_index]
    DenCon_s_raw = DenCon_filter[sort_index]
    DenCon_s = DenCon_s_raw + numpy.abs(DenCon_s_raw.min()) + 1.0e-8
    print "Data rescaled"

    print DenCon_s.min()
    print DenCon_s.max()

    print "Freeing up memory"
    del DenCon_s_raw
    del DenCon_filter
    del pos_x_filter
    del pos_y_filter
    del pos_z_filter
    del z_filter
    
    #****************************************************************************************************
    #***** Plotting with scatter *****
    #****************************************************************************************************
    
    print "Plotting"
    
    #norm = matplotlib.colors.Normalize(vmin=DenCon_s.min(),vmax=(DenCon_s.max()) )
    
    pyplot.close('all')
    pyplot.figure(figsize=(width,height))
    #pyplot.scatter(x_s, y_s, s=7, c=DenCon_s, cmap=pyplot.cm.jet , edgecolors='none', marker='s') #This works!
    pyplot.scatter(x_s, y_s, s=7, c=DenCon_s, cmap=pyplot.cm.jet , edgecolors='none', norm=matplotlib.colors.LogNorm(vmin=DenCon_s.min(), vmax=DenCon_s.max()), marker='s') #This works!
    pyplot.xlim(0.0,BoxSize)
    pyplot.ylim(0.0,BoxSize)
    pyplot.xlabel(r"Comoving distance $x$ [$h^{-1}$Mpc]")
    pyplot.ylabel(r"Comoving distance $y$ [$h^{-1}$Mpc]")
    pyplot.title(r"$\Delta(\vec{r})$ for $%d \leq z < %d$"%(i,k) )
    pyplot.colorbar()
    pyplot.savefig("DenCon_full_z_from_%dto%d.png"%(i,k) )
    #pyplot.show()
