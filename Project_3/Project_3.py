# Basic N-Body simulation, mainly just playing with vectors and vpython -- can we simulate the Sun's "wobble" ?

import spiceypy

# import numpy
# import datetime
# import vpython

spiceypy.furnsh("Project_3/meta_kernel.txt")

# ---------------------------------------------------

et = spiceypy.utc2et("01 JAN 2010 0:0:0")
G = 0.000000000066743

# Bodies: sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
bodyid_dictionary = {
    "SUN": 10,
    "MERCURY": 199,
    "VENUS": 299,
    "EARTH": 399,
    "MARS": 499,
    "JUPITER": 599,
    "SATURN": 699,
    "URANUS": 799,
    "NEPTUNE": 899,
}

BODIES = []

for body in bodyid_dictionary:

    # Array: body name | naif id code | mass | position wrt SSB [3d array] | velocity wrt SSB [3d array]
    info = []

    info.append(body)
    info.append(bodyid_dictionary[body])
    info.append(spiceypy.bodvcd(bodyid=info[1], item="GM", maxn=1)[1][0] / G)
    info.append(spiceypy.spkgeo(targ=info[1], et=et, ref="ECLIPJ2000", obs=0)[0][:3])
    info.append(spiceypy.spkgeo(targ=info[1], et=et, ref="ECLIPJ2000", obs=0)[0][3:])

    BODIES.append(info)


print(BODIES)
