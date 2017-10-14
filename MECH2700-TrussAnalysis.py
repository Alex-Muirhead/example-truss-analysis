# -*- coding: utf-8 -*-
"""
Example code for MECH2700
A linear algebra calculator to determine the stresses on a truss. 

@author:  Alex Muirhead
@date:    Wed Oct 11 19:51:13 2017
@title:   LinearSolver
@version: 1.1.2
@python:  3.6.1
"""

import numpy as np

MEMBERS = {
    'Rax': 0,  'Ray': 1,  'Rbx': 2,  # Rby not included
    'Tab': 3,  'Tac': 4,
    'Tbc': 5,  'Tbd': 6,
    'Tcd': 7,  'Tce': 8,
    'Tde': 9,  'Tdf': 10,
    'Tef': 11, 'Teg': 12,
    'Tfg': 13, 'Tfh': 14,
    'Tgh': 15
}

# ===== INPUT VARIABLES =====

a = 1.8  # [m]
b = 1.8  # [m]
joint = 'c'
strainGaugeMember = 'Tcd'   # PICK FROM DICTIONARY ABOVE
maxMemberForce = 31977.567  # [N]

"""
Calculate the maximum member force by getting the cross-sectional area of
your brace / chord segment, and using the calculation:

    Force = stress / area = (strain * modulus) / area

"""

# ===========================

assert strainGaugeMember in MEMBERS, \
    "Invalid member name, choose from the defined dictionary"

L = pow(a**2 + b**2, 0.5)
cos = a / L
sin = b / L

geometry = np.zeros([16, 16])

# Ax : Rax + Tac = 0
geometry[0, [0, 4]] = [1, 1]
# Ay : Ray - Tab = 0
geometry[1, [1, 3]] = [1, -1]

# Bx : Rbx + Tbd + Tbc*cos(t) = 0
geometry[2, [2, 6, 5]] = [1, 1, cos]
# By : Tab + Tbc*sin(t) = 0
geometry[3, [3, 5]] = [1, sin]

# Cx : -Tac - Tbc*cos(t) + Tcd*cos(t) + Tce = 0
geometry[4, [4, 5, 7, 8]] = [-1, -cos, cos, 1]
# Cy : -Tbc*sin(t) - Tcd*sin(t) = 0
geometry[5, [5, 7]] = [-sin, -sin]

# Dx : -Tbd - Tcd*cos(t) + Tde*cos(t) + Tdf = 0
geometry[6, [6, 7, 9, 10]] = [-1, -cos, cos, 1]
# Dy : Tcd*sin(t) + Tde*sin(t) = 0
geometry[7, [7, 9]] = [sin, sin]

# Ex : -Tce - Tde*cos(t) + Tef*cos(t) + Teg = 0
geometry[8, [8, 9, 11, 12]] = [-1, -cos, cos, 1]
# Ey : -Tde*sin(t) - Tef*sin(t) = 0
geometry[9, [9, 11]] = [-sin, -sin]

# Fx : -Tdf - Tef*cos(t) + Tfg*cos(t) + Tfh = 0
geometry[10, [10, 11, 13, 14]] = [-1, -cos, cos, 1]
# Fy : Tef*sin(t) + Tfg*sin(t) = 0
geometry[11, [11, 13]] = [sin, sin]

# Gx : -Teg - Tfg*cos(t) = 0
geometry[12, [12, 13]] = [-1, -cos]
# Gy : -Tfg*sin(t) - Tgh = 0
geometry[13, [13, 15]] = [-sin, -1]

# Hx : -Tfh = 0
geometry[14, [14]] = [-1]
# Hy : Tgh = F
geometry[15, [15]] = [1]

externalForces = np.zeros([16])
externalForces[15] = 0.5  # Only half of external load applied to each side

internalForces = np.linalg.solve(geometry, externalForces)

appliedForce = maxMemberForce / internalForces[MEMBERS[strainGaugeMember]]
print(">>> APPLIED LOAD <<<")
print("The applied load is {:.3e} N".format(-appliedForce))

internalForces *= appliedForce
paired = list(zip(MEMBERS, internalForces))

formatStr = "The interal force on {} is {:>10.3e} N"

print("\n>>> CHORD FORCES <<<")
for i in range(4, 16, 4):
    print(formatStr.format(*paired[i]))
for i in range(6, 18, 4):
    print(formatStr.format(*paired[i]))

print("\n>>> BRACE FORCES <<<")
for i in range(3, 17, 2):
    print(formatStr.format(*paired[i]))

print("\n>>> REACTION FORCES <<<")
for i in range(3):
    print("The reaction force {} is {:>10.3e} N".format(*paired[i]))
print("The reaction force {} is {:>10.3e} N".format("Rby", 0))

print("\n>>> STRESSES NEAR {} <<<".format(joint.upper()))
for i, member in enumerate(MEMBERS):
    if joint in member:
        print(formatStr.format(*paired[i]))
