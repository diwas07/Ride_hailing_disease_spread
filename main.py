#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from ipynb.fs.full.paramters_ import *
from ipynb.fs.full.class_functions import *
from ipynb.fs.full.functions_ import *
import matplotlib.pyplot as plt


# In[2]:


def simulate_disease_spread():
    counter = []        

    #%% Objects
    city = Zone(beta, mu, eta, delta, gamma, num_susceptible, num_exposed, 
                num_undocumented, num_documented, num_immune)

    population_per_compartment = np.array([city.num_susceptible, 
                                           city.num_exposed, 
                                           city.num_undocumented, 
                                           city.num_documented, 
                                           city.num_immune])

    uber_divers_compartment = population_per_compartment/city.population*num_uber_divers
    uber_divers_compartment = uber_divers_compartment.astype(int)
    driver_compartment = uber_divers_compartment[0]*[[1,0,0,0,0]]+     
                         uber_divers_compartment[1]*[[0,1,0,0,0]]+                         
                         uber_divers_compartment[2]*[[0,0,1,0,0]]+                         
                         uber_divers_compartment[3]*[[0,0,0,1,0]]+                         
                         uber_divers_compartment[4]*[[0,0,0,0,1]]

    uber_drivers = [Driver(driver_compartment[i]) for i in range(len(driver_compartment))]
    uber_vehicles = [Uber(num_periods_decay, uber_driver) 
                     for uber_driver in uber_drivers]

    #%% Main loop

    for day in range(simulation_time):
#         print('day:', day)
        fract=[1, 1]
        uber_divers_compartment = get_uber_per_compartment(uber_vehicles)
        travel_distribution_compartment =             get_travel_info(city, fract)
        num_travels_per_hour = travel_distribution_compartment.sum(axis=0)
        pass_exposed = 0
        for period in range(num_time_periods):
            free_uber = get_free_uber(uber_vehicles)
            num_free_uber = len(free_uber)
            if num_free_uber > num_travels_per_hour[period]:
                new_ubers_in_service = np.random.choice(
                    free_uber, num_travels_per_hour[period])
                new_exposed,passenger_exposed = assign_new_ubers(new_ubers_in_service, 
                                 travel_distribution_compartment[:,period])
                pass_exposed += passenger_exposed

            else:
                new_exposed,passenger_exposed = assign_new_ubers(new_ubers_in_service, 
                                 travel_distribution_compartment[:,period])
                pass_exposed +=passenger_exposed

            [vehicle.tic() for vehicle in uber_vehicles]
        counter.append(pass_exposed)    
        city.update_infection(pass_exposed)
        #city.update_infection(new_exposed)
    zonewise_data = np.array(city.memory)
    return(zonewise_data)


# In[3]:


def disease_spread_graph(zone_data):
    plt.plot(zone_data[:,0],label = 'Susceptible')
    plt.plot(zone_data[:,1],label = 'Exposed')
    plt.plot(zone_data[:,2],label = 'Undocumented')
    plt.plot(zone_data[:,3],label = 'Documented')
    plt.plot(zone_data[:,4],label = 'Immune/Recovered')
    plt.xlabel('Day')
    plt.ylabel('Number of people')
    plt.title('Disease progression')
    plt.legend()
    plt.ylim((0,5000000))
    plt.show()


# In[ ]:




