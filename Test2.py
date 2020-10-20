import re
import math
import bisect
import warnings
import time
from datetime import datetime, timedelta
from inspect import signature, getsourcelines
from collections import namedtuple

import numpy as np
from scipy import integrate
from scipy import linalg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# from .Function import Function

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:04:08 2020

@author: Rosen Yu
"""
from rocketpy import Environment, Rocket, SolidMotor, Flight

Env = Environment(
    railLength=5.2,
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400,
    date=(2020, 9, 26, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

Env.setAtmosphericModel(type='Forecast', file='GFS')

Pro75M1670 = SolidMotor(

    thrustSource="data/motors/Cesaroni_M1670.eng",
    burnOut=3.9,
    grainNumber=5,
    grainSeparation=5/1000,
    grainDensity=1815,
    grainOuterRadius=33/1000,
    grainInitialInnerRadius=15/1000,
    grainInitialHeight=120/1000,
    nozzleRadius=33/1000,
    throatRadius=11/1000,
    interpolationMethod='linear'
)

Calisto = Rocket(
    motor=Pro75M1670,
    radius=127/2000,
    mass=19.197-2.956,
    inertiaI=6.60,
    inertiaZ=0.0351,
    distanceRocketNozzle=-1.255,
    distanceRocketPropellant=-0.85704,
    powerOffDrag="data/calisto/powerOffDragCurve.csv",
    powerOnDrag="data/calisto/powerOnDragCurve.csv"
)


Calisto.setRailButtons([0.2, -0.5])

NoseCone = Calisto.addNose(length=0.55829, kind="vonKarman", distanceToCM=0.71971)

FinSet = Calisto.addFins(4, span=0.100, rootChord=0.120, tipChord=0.040, distanceToCM=-1.04956)

Tail = Calisto.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)

def drogueTrigger(p, y):
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    return True if y[5] < 0 and y[2] < 800 else False

Main = Calisto.addParachute('Main',
                            CdS=10.0,
                            trigger=mainTrigger, 
                            samplingRate=105,
                            lag=1.5,
                            noise=(0, 8.3, 0.5))

Drogue = Calisto.addParachute('Drogue',
                              CdS=1.0,
                              trigger=drogueTrigger, 
                              samplingRate=105,
                              lag=1.5,
                              noise=(0, 8.3, 0.5))

TestFlight = Flight(rocket=Calisto, environment=Env, inclination=85, heading=0, name = "TestFlight")


Dalisto = Rocket(
    motor=Pro75M1670,
    radius=100/2000,
    mass=19.197-2.956,
    inertiaI=6.60,
    inertiaZ=0.0351,
    distanceRocketNozzle=-1.255,
    distanceRocketPropellant=-0.85704,
    powerOffDrag="data/calisto/powerOffDragCurve.csv",
    powerOnDrag="data/calisto/powerOnDragCurve.csv"
)


Dalisto.setRailButtons([0.2, -0.5])

NoseCone = Dalisto.addNose(length=0.5, kind="vonKarman", distanceToCM=0.71971)

FinSet = Dalisto.addFins(4, span=0.50, rootChord=0.10, tipChord=0.040, distanceToCM=-1)

Tail = Dalisto.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)


Main = Dalisto.addParachute('Main',
                            CdS=10.0,
                            trigger=mainTrigger, 
                            samplingRate=105,
                            lag=1.5,
                            noise=(0, 8.3, 0.5))

Drogue = Dalisto.addParachute('Drogue',
                              CdS=1.0,
                              trigger=drogueTrigger, 
                              samplingRate=105,
                              lag=1.5,
                              noise=(0, 8.3, 0.5))


TestFlight2 = Flight(rocket=Dalisto, environment=Env, inclination=85, heading=0, name = "TestFlight2")

############################################################################## 
# Rosen: Codes for Plotting

# Create a figure and an axes.
fig, ax = plt.subplots()  

# Get the altitude from flight 1
z1 = TestFlight.getZ();
t1 = TestFlight.getZtime();
n1 = TestFlight.getName();

# Get the altitude from flight 1
z2 = TestFlight2.getZ();
t2 = TestFlight2.getZtime();
n2 = TestFlight2.getName();

# Plot
ax.plot(t1, z1, label=n1)  # Plot some data on the axes.
ax.plot(t2, z2, label=n2)  # Plot more data on the axes...
ax.set_xlabel('Time (sec)')  # Add an x-label to the axes.
ax.set_ylabel('Altitude (m)')  # Add a y-label to the axes.
ax.set_title("Altitude Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.
plt.show()
############################################################################## 

# TestFlight.info()

# TestFlight.allInfo()