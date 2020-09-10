# This project investigated the causes of the solar system barycenter’s (SSB) movement. The computations and visualisations of miscellaneous angular parameters reveal that these planets are the main reason of the movement of the Solar System Barycentre as introduced in Project 1.
# Following along with [ThomasAlbin's Space Science Tutorials](https://towardsdatascience.com/@thomas.albin)

import spiceypy
import pandas
import datetime
import numpy
from matplotlib import (
    pyplot,
)  # You can't just import all of matplotlib, you must specifically invoke pyplot to use it

# 0: KERNELS ---------------------------------------------------

spiceypy.furnsh("Project_2/meta_kernel.txt")

# ---------------------------------------------------
# (1.0): Compute the trajectory of the barycentre with respect to the Sun
# ---------------------------------------------------

# 1.1: TIME ---------------------------------------------------

# Create a time interval starting at Jan 1 2000, with a delta t of 10,000 days. Convert to Ephemeris time.
TIME_INITIAL_UTC = datetime.datetime(
    year=1990, month=1, day=1, hour=0, minute=0, second=0
)
TIME_DELTA_days = 15000
TIME_FINAL_UTC = TIME_INITIAL_UTC + datetime.timedelta(days=TIME_DELTA_days)

TIME_INITIAL_UTC_STR = TIME_INITIAL_UTC.strftime("%Y-%m-%dT%H:%M:%S")
TIME_FINAL_UTC_STR = TIME_FINAL_UTC.strftime("%Y-%m-%dT%H:%M:%S")

print("Initial time (UTC): ", TIME_INITIAL_UTC_STR)
print("Final time (UTC): ", TIME_FINAL_UTC_STR, "\n")

TIME_INITIAL_ET = spiceypy.utc2et(TIME_INITIAL_UTC_STR)
TIME_FINAL_ET = spiceypy.utc2et(TIME_FINAL_UTC_STR)


# 1.2: TRAJECTORY OF SSB WRT SUN---------------------------------------------------

# Create a NumPy array with 10,000 steps (one for each day over the interval)
TIME_INTERVAL_ET = numpy.linspace(
    start=TIME_INITIAL_ET, stop=TIME_FINAL_ET, num=TIME_DELTA_days
)

# using sun radii bc km too small, AU too big
_, SUN_RADIUS_km = spiceypy.bodvcd(10, "RADII", 3)
SUN_RADIUS_km = SUN_RADIUS_km[0]

# Create empty data frame (watch corey schafer vid part 2)
SS_DF = pandas.DataFrame()

# NOTE The ET column is set to values over the time interval -- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
SS_DF.loc[:, "ET"] = TIME_INTERVAL_ET

# NOTE Create a converted UTC column
SS_DF.loc[:, "UTC"] = SS_DF["ET"].apply(lambda t: spiceypy.et2datetime(et=t).date())

# ---------------------------------------------------

# NOTE Create a column for ssb wrt sun position and distance
SS_DF.loc[:, "SSB_wrt_SUN_pos_km"] = SS_DF["ET"].apply(
    lambda et: spiceypy.spkgps(targ=0, et=et, ref="ECLIPJ2000", obs=10)[
        0
    ]  # NOTE 0 is here bc spkgps outputs a tuple with "pos" (position) and "lt" (light time), and we only want pos (spkgps[0]). Formatting is atrocious though.
)

SS_DF.loc[:, "SSB_wrt_SUN_pos_sunradii"] = SS_DF["SSB_wrt_SUN_pos_km"].apply(
    lambda vector: vector / SUN_RADIUS_km
)

SS_DF.loc[:, "SSB_wrt_SUN_dist_sunradii"] = SS_DF["SSB_wrt_SUN_pos_sunradii"].apply(
    lambda vector: spiceypy.vnorm(vector)
)

# ---------------------------------------------------
# Visualizing this data in matplotlib

"""# Set figure
FIG, AX = pyplot.subplots(figsize=(6, 4))

# Plot ssb wrt sun dist
AX.plot(SS_DF["UTC"], SS_DF["SSB_wrt_SUN_dist_sunradii"], color="blue")

# Labels and colors
AX.set_xlabel("Date (UTC)")
AX.set_ylabel("Distance between SSB and Sun (Sun radii)", color="tab:blue")
AX.tick_params(axis="y", labelcolor="tab:blue")

# Limits for x and y axes
AX.set_xlim(TIME_INITIAL_UTC, TIME_FINAL_UTC)
AX.set_ylim(0, 2)

# Set grid
AX.grid(axis="x", linestyle="dashed", alpha=0.5)

# pyplot.show()
"""

# ---------------------------------------------------
# (2.0): Phase angles
# ---------------------------------------------------

# 2.1: COMPUTE PHASE ANGLES FOR GAS GIANTS ---------------------------------------------------

# Create dictionary data structure w abbreviated planet names and naif id codes
PLANET_DICTIONARY = {"JUP": 5, "SAT": 6, "URA": 7, "NEP": 8}

# Iterate through dict & compute pos vector for each planet wrt Sun
for planet in PLANET_DICTIONARY:

    planet_id = PLANET_DICTIONARY[planet]

    # Compute the planet's position as seen from the Sun
    planet_pos_col = "%s_wrt_SUN_pos_km" % planet
    SS_DF.loc[:, planet_pos_col] = SS_DF["ET"].apply(
        lambda t: spiceypy.spkgps(targ=planet_id, et=t, ref="ECLIPJ2000", obs=10)[0]
    )

    # Compute the phase ∠planet/sun/ssb (sun is at intersection)
    planet_angle_col = "PHASE_ANGLE_%s_SUN_SSB" % planet
    SS_DF.loc[:, planet_angle_col] = SS_DF.apply(
        lambda x: numpy.degrees(
            spiceypy.vsep(v1=x[planet_pos_col], v2=x["SSB_wrt_SUN_pos_km"])
        ),
        axis=1,  # NOTE that since we need 2 columns for this computation, `.apply` is applied on axis=1 to avoid an error (idk why it just does)
    )


# ---------------------------------------------------
# Final SS_DF columns:
# UTC | ET | SSB_wrt_SUN_pos_km | SSB_wrt_SUN_pos_sunradii | [<GasGiant>_wrt_SUN_pos_km, PHASE_ANGLE_<GasGiant>_SUN_SSB][4]
# ---------------------------------------------------


# 2.2: PLAYING WITH THE MATH OF PHASE ANGLES TO VERIFY VSEP ---------------------------------------------------
# Verify spiceypy.vsep by manually computing phase ∠jup/sun/ssb

# Define a lambda function the computes the angle between two vectors
manual_phase_angle_comp = lambda vector1, vector2: numpy.arccos(
    numpy.dot(vector1, vector2)
    / (numpy.linalg.norm(vector1) * numpy.linalg.norm(vector2))
)
print(
    "Phase angle between the SSB and Jupiter as seen from the Sun (first array entry, lambda function): %s"
    % numpy.degrees(
        manual_phase_angle_comp(
            SS_DF["SSB_wrt_SUN_pos_km"].iloc[0], SS_DF["JUP_wrt_SUN_pos_km"].iloc[0]
        )
    )
)
print(
    "Phase angle between the SSB and Jupiter as seen from the Sun (first array entry, SPICE vsep function): %s"
    % numpy.degrees(
        spiceypy.vsep(
            SS_DF["SSB_wrt_SUN_pos_km"].iloc[0], SS_DF["JUP_wrt_SUN_pos_km"].iloc[0]
        )
    )
)

# ---------------------------------------------------
# (3.0): Calculating gravitational pull of gas giants
# ---------------------------------------------------

# 3.1: Plotting gas giants: time v phase angle ---------------------------------------------------

# 4 axes plot, vertically aligned, share x axis (utc)
FIG, (AX1, AX3, AX3, AX4) = pyplot.subplots(4, 1, sharex=True, figsize=(8, 20))

# Iterate through matplotlib axes & planet data, plot phase angle in each axis
for ax, planet_name_abrev, planet_name in zip(
    [AX1, AX2, AX3, AX4],
    ["JUP", "SAT", "URA", "NEP"],
    ["Jupetier", "Saturn", "Uranus", "Neptune"],
):

    # Title
    ax.set_title(planet_name, color="tab:orange")

    # Plot dist from part 1
    ax.plot(SS_DF["UTC"], SS_DF["SSB_wrt_SUN_dist_sunradii"], color="tab:blue")

    # y label/color/ticks
    ax.set_ylabel("Distance between Sun and SSB [Sun Radii]", color="tab:blue")
    ax.tick_params(axis="y", labelcolor="tab:blue")

    # lims
    ax.set_xlim(TIME_INITIAL_UTC, TIME_FINAL_UTC)
    ax.set_ylim(0, 2)

    # Create twin plot in same matplotlib axis, copying the x axis

