#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
from ipynb.fs.full.paramters_ import *


# In[5]:



#%% Clasess
class Zone:
    def __init__(self, beta, mu, eta, delta, gamma, num_susceptible, 
                 num_exposed, num_undocumented,num_documented, num_immune):
        self.beta = beta
        self.mu = mu
        self.eta = eta
        self.delta = delta
        self.gamma = gamma
        self.num_susceptible = num_susceptible 
        self.num_exposed = num_exposed
        self.num_undocumented = num_undocumented
        self.num_documented = num_documented
        self.num_immune = num_immune
        self.compartments = [self.num_susceptible,
                             self.num_exposed,
                             self.num_undocumented,
                             self.num_documented,
                             self.num_immune]

        
        self.population = num_susceptible + num_exposed + num_undocumented + num_documented + num_immune
        self.dynamic_matrix = self._get_dynamic_matrix()
        self.memory = [[num_susceptible, num_exposed, num_undocumented, 
                        num_documented, num_immune]]
               

    def _get_dynamic_matrix(self):
        susceptible_row = [1, 0, 0, 0, 0]
        exposed_row = [0, 1 - self.eta, (1 - self.delta) * self.eta, 
                       self.delta * self.eta, 0]
        undocumented_row = [- self.mu * self.beta * self.num_susceptible, 
                            self.mu * self.beta * self.num_susceptible,
                            1 - self.gamma, 0, self.gamma]
        documented_row = [- self.beta * self.num_susceptible, 
                          self.beta * self.num_susceptible, 0, 1 - self.gamma, self.gamma]
        immune_row = [0, 0, 0, 0, 1]
      
        dynamic_matrix = np.array([susceptible_row, exposed_row, undocumented_row, documented_row, immune_row])
      
        return dynamic_matrix
             
    def update_infection(self, uber_exposed):
        self.num_susceptible -= uber_exposed
        self.num_susceptible = max(0, self.num_susceptible)
        self.num_exposed += uber_exposed
        current_state = np.array([self.num_susceptible,
                                  self.num_exposed,
                                  self.num_undocumented, 
                                  self.num_documented, 
                                  self.num_immune]).reshape(1,5)
        
        self.dynamic_matrix = self._get_dynamic_matrix()      
        new_state = np.matmul(current_state, self.dynamic_matrix)
        new_state = new_state.reshape(5,)
        
        self.num_susceptible, self.num_exposed, self.num_undocumented, self.num_documented, self.num_immune = new_state
        
        self.dynamic_matrix = self._get_dynamic_matrix()
        self.memory.append([self.num_susceptible, self.num_exposed, 
                            self.num_undocumented,self.num_documented, 
                            self.num_immune])
        
        self.compartments = [self.num_susceptible,
                             self.num_exposed,
                             self.num_undocumented,
                             self.num_documented,
                             self.num_immune]
            

class Uber:
    def __init__(self, num_periods_decay, driver):
        self.num_periods_decay = num_periods_decay
        self.driver = driver
        self.busy = False
        self.infected = False
        self.time_to_destination = -1
        self.time_to_recover = -1
        
    def tic(self):
        if self.busy:
            self.time_to_destination = max(0, self.time_to_destination - 1)
            self.busy = False if self.time_to_destination == 0 else True
        
        if self.infected:
            self.time_to_recover = max(0, self.time_to_recover - 1)
            self.infected = False if self.time_to_recover == 0 else True
            
    def assign(self, time_to_destination):
        self.time_to_destination = time_to_destination
        self.busy = True
                
    def infect(self):
        self.time_to_recover = self.num_periods_decay
        self.infected = True
        self.driver.susceptible, self.driver.exposed, self.driver.undocumented, self.driver.documented, self.driver.inmune = np.array([0,1,0,0,0], dtype = np.bool)
        
class Driver:
    def __init__(self, compartment):
        self.susceptible, self.exposed, self.undocumented, self.documented, self.inmune = np.array(compartment, dtype = np.bool)
        
        self.compartment = np.array(compartment, dtype = np.int)
        self.infected = self.undocumented or self.documented
            


# In[ ]:





# In[ ]:




