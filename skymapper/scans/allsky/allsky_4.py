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

def allsky_survey(pointing_file, save_suffix):
    dir= os.path.dirname(__file__)
    savedir = os.path.join(dir, '../../data/allsky_test/')


    # FOV Dimensions
    FOV_Dim=(2048*6.2/3600)*(pi/180) # Base Dimension
    FOV_phi=FOV_Dim*2
    FOV_theta=FOV_Dim
    Nstrip=21 # Number of strips on each band of FOV 
    skymap = SkyMap2(nside=2**8,LVF_theta=FOV_theta, LVF_phi=FOV_phi, cap_theta=pi) 

    pointings1 = read_in_date(pointing_file)
    

    days = np.unique(pointings1[:,0])
    

    # Initializations
    skyplot1=SkyPlots2()
    fig_sub, ax_sub= plt.subplots(1, 4, subplot_kw=dict(projection="mollweide"))        
    sub_ind=0
    sum_plot_days=[2,91,182,273,365]
    least_plot_days=[91,181,273,365]
    
    plot_lambda_ranges=[(.75,2.34),(.75,.76),(1.30,1.33),(2.26,2.34)]

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

                moll_plot(theta_in, phi_in, hits_in , "least_allsky: Day %s"%(day), "least_allsky_4_day_%s" %(day))

            if (day in sum_plot_days) & (i==0):
                sum_hits_arr=skymap.sum_hits()

                theta_in=sum_hits_arr[:, 0]
                phi_in=sum_hits_arr[:, 1]
                hits_in=sum_hits_arr[:, 2]

                moll_plot(theta_in, phi_in, hits_in , "sum_allsky: Day %s"%(day), "sum_allsky_4_day_%s" %(day))

    least_hits_arr=skymap.least_hits()
    theta_in=least_hits_arr[:, 0]
    phi_in=least_hits_arr[:, 1]
    hits_in=least_hits_arr[:, 2]
    moll_plot(theta_in, phi_in, hits_in , "least_allsky: Day %s"%("FINAL"), "least_allsky_4_day_%s" %("FINAL"))

    sum_hits_arr=skymap.sum_hits()
    theta_in=sum_hits_arr[:, 0]
    phi_in=sum_hits_arr[:, 1]
    hits_in=sum_hits_arr[:, 2]
    moll_plot(theta_in, phi_in, hits_in , "sum_allsky: Day %s"%("FINAL"), "sum_allsky_4_day_%s" %("FINAL"))

 
if __name__=='__main__':
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/all_sky_days.txt', 'test_out')
#    allsky_survey('/home/rmkatti/skymapper/skymapper/data/test_2000', 'test_out')
    dir= os.path.dirname(__file__)    
    pointfile = os.path.join(dir, '../../data/all_sky_days.txt')

    time1=time.time()
    allsky_survey( pointfile, 'test_data3_2_9')
    time2=time.time()
    print "Time Elapsed: %s" %(time2-time1)
