# Module Import
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import *
import scipy
import numpy as np
import os

os.chdir("/Users/izayzay/Downloads")

# Data Import
dat2 = pd.read_csv("2017_Fuel_Economy_Data.csv")
y = dat2['Combined Mileage (mpg)']

# Generate a class for bootstrapped samples' CI
#%%
class Boot():
    """
    Initializes class 'Boot'
    """
    
    def __init__(self, data = None, stat = "mean"):
        self.stat = stat
        self.dat = data
        self.boot_stat = []
        self.n_boot = len(self.boot_stat)
        self.conf_level = 0.95 
        self.n = None

    def assign_data(self, data):
        """
        Allows for data assignment to object. This data should be in the form 
        of a Pandas series.  

        Parameters
        ----------
        data : Series of data to be bootstrapped
        """
        self.dat = data
        self.n = len(data)
        
    def clear_stat_list(self):
        """Clears list of summary statistics of bootstrapped samples"""
        self.boot_stat = []
        
    def set_statistic(self, statistic):
        """
        Selection of summary statistic of bootstrapped samples. Clears previous
        summary statistic list. 
        
        Parameters
        ----------
        statistic: Name of summary statistic desired. Options include 'mean', 'std', 
        and 'median'
        """
        self.stat = statistic
        self.clear_stat_list()
        
    def sims_loop(self, boots = 100):
        """
        Bootstraps sample and calculates desired summary statistic and appends to
        list within object

        Parameters
        ----------
        boots : number of bootstraps to perform
        Raises
        ------
        TypeError
            Name of statistic given is invalid. See 'self.set_statistic'.

        """
        
        if type(self.dat) == None :
            print("No data or incorrect data has been supplied")
        else:
            self.n = len(self.dat)

            for i in range(boots):
                boot_sample = self.dat.sample(self.n, replace = True)
                if self.stat == 'median':
                    self.boot_stat.append(float(boot_sample.mean()))
                
                elif self.stat == 'mean':
                    self.boot_stat.append(float(boot_sample.mean()))
                    
                elif self.stat == 'std':
                        self.boot_stat.append(float(boot_sample.std()))
                else:
                    raise TypeError("Invalid Statistic Name")
        self.n_boot = len(self.boot_stat)
        
    def plot_boot(self):
        """
        Plots histogram of summary statistic list made from bootstrapped
        samples
        """
        df = pd.DataFrame({self.stat: self.boot_stat})
        plot = (
        ggplot(data = df, mapping = aes(x = self.stat)) + 
         geom_histogram()
         )
        return(plot)
        
    def CI(self):
        """
        Calculates CI for the mean based on bootstrapped samples
        """
        conf = (100 - self.conf_level*100)/2
        if self.n_boot == 0:
            print("No Boots Performed")
        else: 
            return(np.percentile(self.boot_stat, [conf, 100-conf]))

#%%
boot1 = Boot(data = 100)
boot1.boot_stat
boot1.plot_boot()
boot1.CI()

#%%
boot2 = Boot()
boot2.assign_data(y)
boot2.sims_loop(100)
