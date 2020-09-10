# This project finds the barycenter of the Solar System wrt the Sun over a time interval
# Following along with [ThomasAlbin's Space Science Tutorials](https://towardsdatascience.com/@thomas.albin)

import spiceypy
import datetime
import numpy
import math
from matplotlib import pyplot

# ---------------------------------------------------

# Instead of furnishing kernels individually, you do them all at once with a meta file
spiceypy.furnsh("Project_1/meta_kernel.txt")


# ---------------------------------------------------

# Initial time (my birthday hehe)
INITIAL_TIME_UTC = datetime.datetime(
    year=2002, month=12, day=11, hour=0, minute=0, second=0
)

# Final time after an arbitrary period
DAYS_ELAPSED = 10_000
FINAL_TIME_UTC = INITIAL_TIME_UTC + datetime.timedelta(days=DAYS_ELAPSED)

# Convert to strings in the format SPICE recognizes
INITIAL_TIME_UTC_STR = INITIAL_TIME_UTC.strftime("%Y-%m-%dT%H:%M:%S")
FINAL_TIME_UTC_STR = FINAL_TIME_UTC.strftime("%Y-%m-%dT%H:%M:%S")

print("Initial time (UTC): ", INITIAL_TIME_UTC_STR)
print("Final time (UTC): ", FINAL_TIME_UTC_STR, "\n")

# Convert UTC to Ephemeris Time
INITIAL_TIME_ET = spiceypy.utc2et(INITIAL_TIME_UTC_STR)
FINAL_TIME_ET = spiceypy.utc2et(FINAL_TIME_UTC_STR)

# NOTE that these time calculations have factored in leap seconds. In this case, the difference in 5 sec which may or may not be substantial to your objective
print(
    "The time interval covered is",
    (numpy.round(FINAL_TIME_ET - INITIAL_TIME_ET)),
    "seconds\n",
)


# ---------------------------------------------------

# Create a NumPy array with 10,000 steps (one for each day over the interval)
TIME_INTERVAL_ET = numpy.linspace(
    start=INITIAL_TIME_ET, stop=FINAL_TIME_ET, num=DAYS_ELAPSED
)

# Store position of SSB wrt Sun over 10,000 days in a numpy array and print
SSB_WRT_SUN = []

for time in TIME_INTERVAL_ET:
    position, _ = spiceypy.spkgps(targ=0, et=time, ref="ECLIPJ2000", obs=10)
    SSB_WRT_SUN.append(position)

SSB_WRT_SUN = numpy.array(SSB_WRT_SUN)

""" this is inefficient
print(
    "The initial position of SSB wrt Sun is: \nX:",
    SSB_WRT_SUN[0][0],
    "km\nY:",
    SSB_WRT_SUN[0][1],
    "km\nZ:",
    SSB_WRT_SUN[0][2],
    "km",
)
"""

print(
    "The initial position of SSB wrt Sun is: \nX: %s km \nY: %s km \nZ: %s km \n"
    % tuple(numpy.round(SSB_WRT_SUN[0]))
)

DISTANCE = lambda x, y, z: math.sqrt(x ** 2.0 + y ** 2.0 + z ** 2.0)

print(
    "The initial distance between the SSB and Sun is %s"
    % numpy.round(
        DISTANCE(SSB_WRT_SUN[0][0], SSB_WRT_SUN[0][1], SSB_WRT_SUN[0][2])
    ),  # numpy.linalg.norm(SSB_WRT_SUN_[0]) also somehow works?
    "km\n",
)

# Put this distance in terms of Sun's radius
_, SUN_RADII = spiceypy.bodvcd(bodyid=10, item="RADII", maxn=3)
SUN_RADIUS = SUN_RADII[0]
SSB_WRT_SUN_SUNRADII = SSB_WRT_SUN / SUN_RADII

print(
    "The initial position of SSB wrt Sun is: \nX: %s sun radii \nY: %s sun radii \nZ: %s sun radii \n"
    % tuple(SSB_WRT_SUN_SUNRADII[0])
)

print(
    "The initial distance between the SSB and Sun is %s"
    % DISTANCE(
        SSB_WRT_SUN_SUNRADII[0][0],
        SSB_WRT_SUN_SUNRADII[0][1],
        SSB_WRT_SUN_SUNRADII[0][2],
    ),
    "sun radii",
)

# Now graph it IN 2 DIMENSIONS

SSB_WRT_SUN_SUNRADII_XY = SSB_WRT_SUN_SUNRADII[:, 0:2]

pyplot.style.use("dark_background")

FIG, AX = pyplot.subplots(figsize=(7, 7))

SUN_CIRC = pyplot.Circle(
    (0.0, 0.0), 1.0, color="yellow", alpha=0.8
)  # Radius is 1 bc unit is sun radii
AX.add_artist(SUN_CIRC)

AX.plot(
    SSB_WRT_SUN_SUNRADII_XY[:, 0],
    SSB_WRT_SUN_SUNRADII_XY[:, 1],
    ls="solid",
    color="royalblue",
)

# Set some parameters for the plot, set an equal ratio, set a grid, and set the x and y limits
AX.set_aspect("equal")
AX.grid(True, linestyle="dashed", alpha=0.5)
AX.set_xlim(-2, 2)
AX.set_ylim(-2, 2)

# Labelling
AX.set_xlabel("X [Sun-Radii]")
AX.set_ylabel("Y [Sun-Radii]")
AX.set_title(
    "Trajectory of the Solar System Barycentre (blue) wrt \nthe centre of the Sun (yellow) projected onto the XY (ecliptic) plane\n"
)

pyplot.show()

# To save the figure:
# plt.savefig('wee.png', dpi=300)
