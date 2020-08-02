# Learning how SPICE "thinks" with kernels -- basic position/velocity in 3D space

import spiceypy
import math

# Errors tell us that we need generic kernel files (from NAIF public repo) -- kernels are added/"furnished" with the SPICE furnsh function
spiceypy.furnsh("kernels/lsk/naif0012.tls.pc")
spiceypy.furnsh("kernels/spk/de432s.bsp")

# ---------------------------------------------------
# Compute position of Earth with respect to (wrt) the Sun when I was born:

# One of the many ways to go from UTC to Ephemeris time (see utc2et docs) -- This is the Ephemeris time when I was born!
ET_BIRTHDAY = spiceypy.utc2et("11 DEC 2002 0:0:0")

# Computing geometric state (position and velocity) of Earth with respects to the Sun
EARTH_STATE_WRT_SUN, EARTH_SUN_LT = spiceypy.spkgeo(
    targ=399, et=ET_BIRTHDAY, ref="ECLIPJ2000", obs=10
)

print(
    "6-dimensional state vector of Earth relative to the Sun is: \n",
    EARTH_STATE_WRT_SUN,
)


# Now to check if results make sense:

# Compute distance from Sun to Earth in km
DIST_EARTH_SUN_km = math.sqrt(
    EARTH_STATE_WRT_SUN[0] ** 2.0
    + EARTH_STATE_WRT_SUN[1] ** 2.0
    + EARTH_STATE_WRT_SUN[2] ** 2.0
)

# Convert to Astronomical Units -- 1AU is the rough distance between the Earth and Sun
DIST_EARTH_SUN_au = spiceypy.convrt(DIST_EARTH_SUN_km, "km", "AU")

percent_error = (DIST_EARTH_SUN_au - 1) * 100

print(
    "The distance between the Sun and Earth in AU is: \n",
    DIST_EARTH_SUN_au,
    "AU \n Which is \n",
    percent_error,
    "% off from the yearly average",
)


# ---------------------------------------------------
# Compute orbital speed of Earth:

EARTH_ORBITALSPEED_WRT_SUN = math.sqrt(
    EARTH_STATE_WRT_SUN[3] ** 2.0
    + EARTH_STATE_WRT_SUN[4] ** 2.0
    + EARTH_STATE_WRT_SUN[5] ** 2.0
)

print(
    "The actual orbital speed of Earth with respects to the Sun is: \n",
    EARTH_ORBITALSPEED_WRT_SUN,
    "km/sec",
)


# Now to check if results make sense using equations from AP Physics 1: v=sqrt(Gm/r) (https://www.youtube.com/watch?v=nxD7koHdQhM)

# Get double precision value of the universal gravitational constant G times the mass of the Sun
spiceypy.furnsh("kernels/pck/gm_de431.tpc")

_, GM_SUN = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)

THEORETICAL_EARTH_ORBITALSPEED_WRT_SUN = math.sqrt(GM_SUN[0] / DIST_EARTH_SUN_km)

print(
    "The theoretical orbital speed of Earth with respects to the Sun is: \n",
    THEORETICAL_EARTH_ORBITALSPEED_WRT_SUN,
    "km/sec",
)
