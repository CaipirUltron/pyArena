#!/usr/bin/env python
# coding: utf-8

# # Trajectory tracking control for unicyle robot
# TODO: Document here

# In[ ]:


# Do this once
import sys
sys.path.append('..')

## Necessary imports
import pyArena.core as pyacore
import pyArena.control.trajectorytracking as pyacontrol
import pyArena.vehicles.underactuatedvehicle as pyavehicle
import matplotlib.pyplot as plt
import numpy as np

## Simulation parameters
nx = 3
nu = 2
Tsim = 100
dt = 0.1
K = np.array([[1, 0.0],[0.0, 0.1]])
eps = np.array([1, 0])
x_init = np.array([10.0, 0.0, np.pi/2])

## Specify desired trajectory
radius = 30

# TODO: Learn Symbolic operations in Python
a = 0.05
pd = lambda t: radius*np.array([np.cos(a*t), np.sin(a*t)])
pdDot = lambda t: radius*np.array([-a*np.sin(a*t), a*np.cos(a*t)])

## Specify the controller
kwargsController = {'pd': pd, 'pdDot': pdDot, 'gain': K, 'eps': eps}

ttController = pyacontrol.TrajectoryTracking(**kwargsController)

kwargsSystem = {'initialCondition': x_init, 'controller': ttController}

system = pyavehicle.UnicycleKinematics(**kwargsSystem)

## Create pyArena simulation object and simulate
kwargsSimulation = {'system': system, 'simTime': Tsim, 'dt': dt}
pyA = pyacore.simulator.pyArena(**kwargsSimulation)
dataLog = pyA.run()

## Plot results
pdVec = pd(dataLog.time).T
plt.plot(pdVec[:,0], pdVec[:,1], 'k--')
plt.plot(dataLog.stateTrajectory[:,0], dataLog.stateTrajectory[:,1], 'r')
plt.show()
