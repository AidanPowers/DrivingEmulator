# -*- coding: utf-8 -*-
"""
Attempted Simulation of this battlebot https://robogames.fandom.com/wiki/Original_Sin
@author: power105
"""
import pychrono as chrono
import pygame

# Initialize Pygame for joystick support
pygame.init()
joystick_count = pygame.joystick.get_count()
## Removed for debugging
# if joystick_count == 0:
#     # No joysticks
#     print("Error, I didn't find any joysticks.")
#     exit()
# else:
#     # Use the first joystick
#     my_joystick = pygame.joystick.Joystick(0)
#     my_joystick.init()
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()


# Create the system
system = chrono.ChSystemNSC()

# Create the ground
ground = chrono.ChBodyEasyBox(1000, 1000, 2, 1000, True, True)
ground.SetPos(chrono.ChVectorD(0, 0, -1))
system.Add(ground)

# Create the vehicle body
body = chrono.ChBodyEasyBox(2.0, 1.0, 0.5, 1000, True, True)
body.SetPos(chrono.ChVectorD(0, 0, 0))
system.Add(body)

# Create the wheels
wheel_FL = chrono.ChBodyEasyCylinder(0.5, 0.2, 1000, True, True)
wheel_FR = chrono.ChBodyEasyCylinder(0.5, 0.2, 1000, True, True)
wheel_RL = chrono.ChBodyEasyCylinder(0.5, 0.2, 1000, True, True)
wheel_RR = chrono.ChBodyEasyCylinder(0.5, 0.2, 1000, True, True)

# Position the wheels
wheel_FL.SetPos(chrono.ChVectorD(1, 0.75, 0))
wheel_FR.SetPos(chrono.ChVectorD(1, -0.75, 0))
wheel_RL.SetPos(chrono.ChVectorD(-1, 0.75, 0))
wheel_RR.SetPos(chrono.ChVectorD(-1, -0.75, 0))

# Add the wheels to the system
system.Add(wheel_FL)
system.Add(wheel_FR)
system.Add(wheel_RL)
system.Add(wheel_RR)

# Create the motors
motor_FL = chrono.ChLinkMotorRotationAngle()
motor_FR = chrono.ChLinkMotorRotationAngle()
motor_RL = chrono.ChLinkMotorRotationAngle()
motor_RR = chrono.ChLinkMotorRotationAngle()

# Attach the motors to the wheels
motor_FL.Initialize(wheel_FL, ground, chrono.ChFrameD(wheel_FL.GetPos()))
motor_FR.Initialize(wheel_FR, ground, chrono.ChFrameD(wheel_FR.GetPos()))
motor_RL.Initialize(wheel_RL, ground, chrono.ChFrameD(wheel_RL.GetPos()))
motor_RR.Initialize(wheel_RR, ground, chrono.ChFrameD(wheel_RR.GetPos()))

# Add the motors to the system
system.Add(motor_FL)
system.Add(motor_FR)
system.Add(motor_RL)
system.Add(motor_RR)

# Main simulation loop
while True:
    pygame.event.pump()

    # Get joystick inputs
    left_y = my_joystick.get_axis(1)
    right_y = my_joystick.get_axis(3)

    # Control the motors based on joystick inputs
    motor_FL.SetDesiredRotation(chrono.ChQuaternionD(left_y, 0, 0, 1))
    motor_FR.SetDesiredRotation(chrono.ChQuaternionD(right_y, 0, 0, 1))
    motor_RL.SetDesiredRotation(chrono.ChQuaternionD(left_y, 0, 0, 1))
    motor_RR.SetDesiredRotation(chrono.ChQuaternionD(right_y, 0, 0, 1))

    # Perform a step of the simulation
    system.DoStepDynamics(0.01)
