# -*- coding: utf-8 -*-
"""
Created on 10/13/2020
@author: Dyllon Preston
Make sure you update the file directories to match your files!
"""

from rocketpy import Environment, Rocket, SolidMotor, Flight
import math

# Parameters for environment for rocket stage 1
Env1 = Environment(
    railLength=10,
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400, #the elevation for stage 1 would be the distance above sea level
    date=(2020, 9, 21, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

# Parameters for first stage motor
motor1 = SolidMotor(
    thrustSource="./RocketPy-master/data/motors/booster.eng",
    burnOut=7.85705280,
    grainNumber=7,
    grainSeparation=5/1000,
    grainDensity=1000,
    grainOuterRadius=0.127,
    grainInitialInnerRadius=0.060396,
    grainInitialHeight=0.168206,
    nozzleRadius=0.086106,
    throatRadius=.019306,
    interpolationMethod='linear'
)

# Parameters for first stage rocket
rocket_stage1 = Rocket(
    motor=motor1,
    radius=.156718,
    mass=106.0998,
    inertiaI=218.85,
    inertiaZ=0.0351,
    distanceRocketNozzle=-5.626619,
    distanceRocketPropellant=-5.13081,
    powerOffDrag="./RocketPy-master/data/GTXR/Stage1PowerOffDrag.csv",
    powerOnDrag="./RocketPy-master/data/GTXR/Stage1PowerOnDrag.csv"
)

rocket_stage1.setRailButtons([0.2, -0.5])

# Parameters for first stage nose cone
NoseCone = rocket_stage1.addNose(length=0.78359, kind="vonKarman", distanceToCM=0.98075)

# Parameters for first stage fins
FinSet = rocket_stage1.addFins(4, span=0.1651, rootChord=0.381, tipChord=0.127, distanceToCM=-.33675)

# Parameters for first stage tail
# Tail = rocket_stage1.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)

# Defining triggers for parachutes
def drogueTrigger(p, y):
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    return True if y[5] < 0 and y[2] < 800 else False

# Parameters for first stage main parachute
Main = rocket_stage1.addParachute('Main',
                            CdS=10.0,
                            trigger=mainTrigger, 
                            samplingRate=105,
                            lag=1.5,
                            noise=(0, 8.3, 0.5))

# Parameters for first stage drogue
Drogue = rocket_stage1.addParachute('Drogue',
                              CdS=1.0,
                              trigger=drogueTrigger, 
                              samplingRate=105,
                              lag=1.5,
                              noise=(0, 8.3, 0.5))

# Parameters for first stage rocket flight
Flight_stage1 = Flight(rocket=rocket_stage1, environment=Env1, inclination=85, heading=0 ,verbose=True)

# Post processing of first stage
Flight_stage1.postProcess()

"""
#//////////////////////////////////////////////             Rocket  Stage 2             //////////////////////////////////////////////////////////////////////////////////////#
"""

# Ignition delay between stage 1 and stage 2
ignition_delay = 4
tsecond_stage = motor1.burnOutTime + ignition_delay

# Parameters for second stage environment
Env2 = Environment(
    railLength=0,
    latitude= Env1.lat + (Flight_stage1.y(tsecond_stage) / 6378000) * (180 / math.pi),
    longitude= Env1.lat + (Flight_stage1.x(tsecond_stage) / 6378000) * (180 / math.pi) / (math.cos(Env1.lat * math.pi / 180)),
    elevation=Flight_stage1.z(tsecond_stage), # elevation must be updated to avoid a discontinuity
    date=(2020, 9, 21, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

# Parameters for second stage motor
motor2 = SolidMotor(
    thrustSource="./RocketPy-master/data/motors/sustainer.eng",
    burnOut=7.75332780,
    grainNumber=5,
    grainSeparation=5/1000,
    grainDensity=1000,
    grainOuterRadius=0.127,
    grainInitialInnerRadius=.059157,
    grainInitialHeight=.281405,
    nozzleRadius=.056642,
    throatRadius=.047699,
    interpolationMethod='linear'
) 

# Parameters for the second stage rocket
rocket_stage2 = Rocket(
    motor=motor2,
    radius=.156718,
    mass=57.81406,
    inertiaI=202.64,
    inertiaZ=0.0351,
    distanceRocketNozzle=-4.13335,
    distanceRocketPropellant=-3.276607,
    powerOffDrag="./RocketPy-master/data/GTXR/PowerOffDrag.csv",
    powerOnDrag="./RocketPy-master/data/GTXR/PowerOnDrag.csv"
)

rocket_stage2.setRailButtons([0.2, -0.5])

# Parameters for second stage nose cone
NoseCone = rocket_stage2.addNose(length=0.55829, kind="vonKarman", distanceToCM=0.49054)

# Parameters for second stage sins
FinSet = rocket_stage2.addFins(4, span=0.1651, rootChord=0.381, tipChord=0.127, distanceToCM=-.2034)

# Parameters for second stage main parachute
Main = rocket_stage2.addParachute('Main',
                            CdS=10.0,
                            trigger=mainTrigger, 
                            samplingRate=105,
                            lag=1.5,
                            noise=(0, 8.3, 0.5))

# Parameters for the second stage drogue
Drogue = rocket_stage2.addParachute('Drogue',
                              CdS=1.0,
                              trigger=drogueTrigger, 
                              samplingRate=105,
                              lag=1.5,
                              noise=(0, 8.3, 0.5))

# Parameters for the second stage flight
Flight_stage2 = Flight(rocket=rocket_stage2, environment=Env2, inclination=Flight_stage1.w1(tsecond_stage), heading=0, initialSolution=[0, Flight_stage1.x(tsecond_stage), 0, Flight_stage1.z(tsecond_stage), Flight_stage1.vx(tsecond_stage), Flight_stage1.vy(tsecond_stage), 0, Flight_stage1.e0(tsecond_stage), Flight_stage1.e1(tsecond_stage), Flight_stage1.e2(tsecond_stage), Flight_stage1.e3(tsecond_stage), Flight_stage1.w1(tsecond_stage), Flight_stage1.w2(tsecond_stage), Flight_stage1.w3(tsecond_stage)])

# Post processing of the second stage
Flight_stage2.postProcess()

"""
#//////////////////////////////////////////////             Print Data             //////////////////////////////////////////////////////////////////////////////////////#
"""

# Prints all graphs for stage 1
# Flight_stage1.allInfo()

#Prints all graphs for stage 2
Flight_stage2.allInfo()