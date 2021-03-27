#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
from ipynb.fs.full.paramters_ import *
from ipynb.fs.full.class_functions import *


# In[4]:


#%% Functions
def get_travel_info(city, fract):         
    def daily_travel(num):
        travel_distribution = np.array([0.01, 0.008, 0.005, 0.003, 0.006, 0.015, 0.035, 
                                    0.06, 0.07, 0.06, 0.06, 0.065, 0.05, 0.057, 
                                    0.06, 0.06, 0.07, 0.08, 0.07, 0.05, 0.045, 0.042,
                                    0.03, 0.02]) 
        return (travel_distribution*num).tolist()

    fraction_of_uber_customers = np.random.uniform(fract[0], fract[1])
    population_per_compartment = np.array([city.num_susceptible, 
                                           city.num_exposed, 
                                           city.num_undocumented, 
                                           city.num_documented, 
                                           city.num_immune])

    num_people_using_uber = population_per_compartment.copy()
    num_people_using_uber[3] = 0
    #Here we are assuming that the documented people are not the uber riders
    num_people_using_uber = fraction_of_uber_customers * num_people_using_uber * num_people_using_uber/num_people_using_uber.sum()
    
    travel_distribution_compartment = np.array(
        list(map(daily_travel, num_people_using_uber)))
    
    return travel_distribution_compartment.astype(int)




def get_uber_per_compartment(uber_vehicles):
    collect = []
    for vehicle in uber_vehicles:
        collect.append(vehicle.driver.compartment)
    
    collect = np.array(collect)
    return np.sum(collect, axis=0)
        
def get_free_uber(uber_vehicles):
    free_vehicles = []
    for vehicle in uber_vehicles:
#         if vehicle.driver.documented = True:
#             vehicle.busy == True
        if vehicle.busy == False:
    
            free_vehicles.append(vehicle)
        
    
    return free_vehicles

def assign_new_ubers(new_ubers_in_service, passenger_compartment, mean_trip_len=0):
    exposed_num = 0
    passenger_exposed = 0
    for idx, vehicle in enumerate(new_ubers_in_service):
        vehicle.assign(np.random.poisson(mean_trip_len))
        if idx+1 <= passenger_compartment[0]:
            if vehicle.infected:
                #exposed_num += 1
                passenger_exposed +=1
        elif idx+1 > passenger_compartment[0] and idx+1 <= passenger_compartment[0] + passenger_compartment[1]:
            pass
        elif idx+1 > passenger_compartment[0] + passenger_compartment[1] and idx+1 <= passenger_compartment[0] + passenger_compartment[1] + passenger_compartment[2]+passenger_compartment[3]:
            vehicle.infect()
            exposed_num += 1
        else:
            pass
    return exposed_num,passenger_exposed


# In[ ]:




