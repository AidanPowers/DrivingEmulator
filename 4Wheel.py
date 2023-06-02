# -*- coding: utf-8 -*-
"""
Attempted Simulation of this battlebot https://robogames.fandom.com/wiki/Original_Sin
@author: power105
"""
import pychrono as chrono

# Create the physical system
system = chrono.ChSystemNSC()

# Create the ground
ground = chrono.ChBodyEasyBox(1000, 1000, 2, 1000, True, True)
ground.SetPos(chrono.ChVectorD(0, 0, -1))
system.Add(ground)

# Create the vehicle body
body = chrono.ChBodyEasyBox(2, 1, 0.5, 1000, True, True)
body.SetPos(chrono.ChVectorD(0, 0, 0))
system.Add(body)

# Create the wheels
wheel_radius = 0.5
wheel_width = 0.2
material = chrono.ChMaterialSurfaceNSC()  # Create a default material
for i in range(4):
    x = 1 if i < 2 else -1
    y = 1 if i % 2 == 0 else -1
    wheel_position = chrono.ChVectorD(x, y, -wheel_radius)
    wheel = chrono.ChBody()
    wheel.SetPos(wheel_position)
    wheel.SetMass(1000)
    wheel.SetInertiaXX(chrono.ChVectorD(1, 1, 1)) # You may need to adjust this based on your specific setup
    wheel.GetCollisionModel().ClearModel()
    wheel.GetCollisionModel().AddCylinder(material, wheel_radius, wheel_width, wheel_position)
    wheel.GetCollisionModel().BuildModel()
    wheel.SetCollide(True)
    system.Add(wheel)
    # Create a motor between the body and the wheel
    motor = chrono.ChLinkMotorRotationSpeed()
    motor.Initialize(wheel, body, chrono.ChFrameD(chrono.ChVectorD(x, y, 0)))
    system.AddLink(motor)
    # Set a constant rotation speed for the motor
    motor.SetSpeedFunction(chrono.ChFunction_Const(10 if y > 0 else -10))

# Create the solver
solver = chrono.ChSolverBB()
system.SetSolver(solver)

# Create the integrator
integrator = chrono.ChTimestepperHHT(system)
system.SetTimestepper(integrator)

# Simulate for 10 seconds
while system.GetChTime() < 10:
    system.DoStepDynamics(0.01)

