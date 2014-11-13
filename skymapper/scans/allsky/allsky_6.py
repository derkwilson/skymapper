"""
First allsky survey

"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from skymapper.visualize.SkyPlots import SkyPlots2
from skymapper.visualize.plot_points import moll_plot
from skymapper.gen_maps.SkyMap2 import SkyMap2
from skymapper.scans.allsky.read_in import read_in_date
from skymapper.visualize.redundancy_funcs import *

import numpy as np
from numpy import pi
import time

def allsky_survey(pointing_file):
    dir= os.path.dirname(__file__)
    savedir = os.path.join(dir, '../../data/allsky_test/')


    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    skymap = SkyMap2(nside=2**8,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=pi) 

    pointings1 = read_in_date(pointing_file)
    days = np.unique(pointings1[:,0])
    
    # Initializations
    fig_sub, ax_sub= plt.subplots(1, 4, subplot_kw=dict(projection="mollweide"))        
    sum_plot_days=[2,8,10,31, 45, 92,183,184,274]
    least_plot_days=[92,93,183,184,274,275]
    
    for day in days:
        points_in=map(tuple, pointings1[ pointings1[:,0]==day, 1:4] )

        for i, tupler in enumerate(points_in):
            print "day:%s, step:%s" %(day, i)
            skymap.make_dicts(day, tupler )
            
            if (day in least_plot_days) & (i==0):
                least_hits_arr=skymap.least_hits()

                theta_in=least_hits_arr[:, 0]
                phi_in=least_hits_arr[:, 1]
                hits_in=least_hits_arr[:, 2]
                moll_plot(theta_in, phi_in, hits_in , "least_allsky: Day %s"%(day-1), "least_allsky_6_day_%s" %(day-1))
                
            #if (day in sum_plot_days) & (i==0):
            #    sum_hits_arr=skymap.sum_hits()

            #    theta_in=sum_hits_arr[:, 0]
            #    phi_in=sum_hits_arr[:, 1]
            #    hits_in=sum_hits_arr[:, 2]

            #   moll_plot(theta_in, phi_in, hits_in , "sum_allsky: Day %s"%(day-1), "sum_allsky_4_day_%s" %(day-1))

    least_hits_arr=skymap.least_hits()
    theta_in=least_hits_arr[:, 0]
    phi_in=least_hits_arr[:, 1]
    hits_in=least_hits_arr[:, 2]
    moll_plot(theta_in, phi_in, hits_in , "least_allsky: Day %s"%("FINAL"), "least_allsky_6_day_%s" %("FINAL"))

    #sum_hits_arr=skymap.sum_hits()
    #theta_in=sum_hits_arr[:, 0]
    #phi_in=sum_hits_arr[:, 1]
    #hits_in=sum_hits_arr[:, 2]
    #moll_plot(theta_in, phi_in, hits_in , "sum_allsky: Day %s"%("FINAL"), "sum_allsky_4_day_%s" %("FINAL"))

 
if __name__=='__main__':
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/all_sky_days.txt', 'test_out')
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/test_2000', 'test_out')
    dir= os.path.dirname(__file__)    
    pointfile = os.path.join(dir, '../../data/all_sky_days_v2.txt')

    time1=time.time()
    allsky_survey( pointfile)
    time2=time.time()
    print "Time Elapsed: %s" %(time2-time1)
