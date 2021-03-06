"""
This class takes a dictionary generated by the SkyMap 
class and plots all-sky in Mollweide
projections or deep sky scans about the celestial 
north pole for selected wavelength ranges.

Coloring of the sky pixels corresponds to the 'hits' or 'redundancy',
the number of times a sky pixel was seen in the specified wavelength.
The produced visualizations are called hits maps. 

"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from numpy import pi, cos, sin
import collections as coll
import cPickle as pickle
from collections import Counter


class SkyPlots2(object):
    def __init__(self):
        pass

    def lambda_plot(self, lambda_dict1, modifier, lambda_min=.75, 
                    lambda_max=5, lambda_global_min=.75, 
                    lambda_global_max=5):

        if lambda_dict1.keys()==[]:
            raise ValueError("lambda_dict.keys() empty list")

        lambda_dict={}

        for key in lambda_dict1.keys():
            if ( lambda_max > key > lambda_min):
                lambda_dict[key]= lambda_dict1[key]

        if lambda_dict.keys()==[]:
            raise ValueError("lambda_dict empty after wavelength bounding applied")
        
        theta_list=[]
        phi_list=[]
        lambda_list=[]

        for tupler in sorted(lambda_dict.items()):
            lambda_list += [tupler[0]]*len(tupler[1])
            theta_listi, phi_listi = zip(*tupler[1])
            theta_list += [ sin(thetai) for thetai in theta_listi]
            phi_list += [ phi for phi in phi_listi]

        if len(lambda_list) != len(theta_list) != len(phi_list):
            raise ValueError("Size mismatch len(lambda_list)=%s, \
                       len(theta_list)=%s, len(phi_list)=%s" \
                       %(len(lambda_list), len(theta_list), len(phi_list) ) )             

        fig= plt.figure()
        ax= plt.subplot(111, polar=True)
        s= ax.scatter(phi_list, theta_list,s=50, c=lambda_list,\
                    vmin=lambda_global_min, vmax=lambda_global_max,\
                    cmap=matplotlib.cm.gist_rainbow, edgecolors='none')

        fig.colorbar(s)
        self.plt.title(plot_title)
        plt.savefig("test_fig_%s.png" %(modifier),dpi=100)
        

    def redundancy_plot(self, lambda_dict, lambda_min, lambda_max, plot_title, plot_type, radius_line=5*pi/180):
        """This method makes a polar plot of the redundancy between two input lambda. Input
           lambda dictionary, lambda_min, lambda_max
        
        plot_type=['deep','allsky']
        """
        redu_list=[] 
        key_list = np.array(lambda_dict.keys())
        key_list= key_list[ (lambda_max > key_list) & (key_list>= lambda_min)]
 
        for key in key_list:
            redu_list+= [ ( round(tupler[0],7) , round(tupler[1],7) ) for tupler in lambda_dict[key] ]
            

        redu_dict=coll.Counter(redu_list) # {(theta1,phi1):#, (theta2,phi2):#...}
        redu_mat=np.asarray(redu_dict.keys())
                
        # Define colormap
        cmap = plt.cm.jet

        # Polar Scatter Plot
        self.fig= plt.figure()

        if plot_type=='deep':
            phi_list= redu_mat[:,1]
            rad_list= np.sin(redu_mat[:,0]) 
            self.ax= plt.subplot(111, polar=True)
            self.scat= self.ax.scatter(phi_list, rad_list, s=5, c=redu_dict.values(),\
                    cmap=cmap, edgecolors='none')
            
        elif plot_type=="allsky":
            
            Dec=pi/2-redu_mat[:,0]
            RA = redu_mat[:,1]
            RA[RA>pi]-=2*pi
       
            self.ax=plt.subplot(111, projection="mollweide")
            self.scat= self.ax.scatter(RA, Dec, s=5, c=redu_dict.values(),\
                    cmap=cmap, edgecolors='none')
        else:
            raise ValueError("Invalid version")

        Nhits= sum(redu_dict.values())       
  
        # Plot cap radius
        if plot_type=="deep":
            phi_rad_plot= np.arange(0,2*pi,.01)
            rad_plot = [sin(radius_line)]*len(phi_rad_plot)
            self.rad_plotter = self.ax.plot(phi_rad_plot , rad_plot, color='m', linewidth=1)
            self.ax.annotate('dec=%.2f$^\circ$'%(90-radius_line*180/pi), xy=(-pi/2,sin(radius_line)), xytext=(0.4, 0.2), textcoords='figure fraction', arrowprops=dict(facecolor='green', shrink=.05),bbox=dict(facecolor='blue',alpha=.3) )
            self.ax.set_rgrids(radii=[ sin(theta) for theta in np.linspace(pi/64,pi/16,3)],labels=90-np.linspace(pi/64,pi/16,3)*180/pi, angle=80, color='DarkOrange',size='medium')

        elif plot_type=="allsky":
            plt.grid(True)

        plt.title(plot_title + "; Total Hits %s" %(Nhits), y=1.06, color='b')
        cb=self.fig.colorbar(self.scat) # Add colorbar
        cb.set_label("# of Hits")
        self.fig.set_size_inches(20.0,10.0)
        
        #plt.savefig("map_%.2f_%.2f.png" %(lambda_min, lambda_max),dpi=500)       
        plt.show()

    def show(self):
        plt.show()

    def lambda_radial_histogram(self, lambda_dict1, lambda_min, lambda_max):
        """This function takes as argument a dictionary 
        lambda1:[(theta1,phi1,...)]. It makes a histogram of hits, where
        each bin is in equal-area radial slice.

        :M Area (in steradians) of each radial slice
        :theta_min (on range [0,pi]) initial value of theta
        :theta_max (on range [0,pi]) final value of theta
        """

        print "Doing Keys"
        keys = np.asarray(lambda_dict1.keys())
        keys= keys[(keys<lambda_max) & (keys>=lambda_min)]
        
        print "Making Data"
        for i,key in enumerate(keys):
            print i
            if i==0:
                data= np.asarray(lambda_dict1[key])[:,0]
            else:
                data=np.append( data, np.asarray(lambda_dict1[key])[:,0], axis=0)

        data=np.around(data, decimals=10)
        data1= Counter(data)
        print "data1 created"
    
        thetas, freq = zip( *sorted(data1.items()) )
        thetas=np.asarray(thetas)
        dec= np.around(90-(180/pi)*thetas,2)

        freq=np.asarray(freq)
        num_sum= freq.sum()
        freq=freq/(2*pi*np.sin(thetas))
        thet_dist= num_sum*freq/freq.sum()
        Nhits=thet_dist.sum()
        
        print "Making Plot"
        fig=plt.figure()
        ax=plt.subplot(111)
        bar=ax.bar(thetas, thet_dist , width=.0001)
        
        strt= len(thetas)/40
        incr = len(thetas)/5
        
        plt.xticks([thetas[0],thetas[len(thetas)/4], thetas[len(thetas)/2], thetas[(len(thetas)*3)/4], thetas[-1]], [dec[0],dec[len(dec)/4], dec[len(dec)/2],dec[(len(dec)*3)/4], dec[-1]] )

        fig.suptitle( "Number Density Distribution; lambda [%.2fum,%.2fum); Total Hits %s" %(lambda_min, lambda_max, Nhits) )
        plt.xlabel("Dec")
        plt.ylabel("Number Density")
        fig.set_size_inches(20.0,10.0)
        #plt.savefig("hist_%.2f_%.2f.png" %(lambda_min, lambda_max),dpi=500)
        #plt.show()
        "Done"
