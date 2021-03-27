#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np


# In[4]:



#%% Parameters
beta = 0.0000003125 # Transmission rate due to documented infected
mu = 0.1 #The factor by which  the transmission rate of undocumented people reduces
eta = 0.4 #The fraction of people who  become documented infected from exposed

delta = 0.2
gamma = 0.01 # Recovery rate
num_susceptible = 3_200_000
num_exposed = 10_000
num_undocumented = 500
num_documented = 200
num_immune = 0
simulation_time = 100
#fraction_uber = 1 #Fraction of the total population that uses uber to move
#INIITIAL WAS 0.5
population_size = num_susceptible + num_exposed + num_undocumented + num_documented + num_immune

num_time_periods = 24# Time periods per day
time_period_lenght = 60# Minutes in a time period
average_trip_length = 15#Minutes
num_uber_divers = 50_000
#DOES NUMBER OF UBER DRIVER EQUAL TO THE NUMBER OF UBERS?
num_periods_decay = 4 # Number of time periods that the virus survives in the vehicle


# In[ ]:




