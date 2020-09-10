Personal notes for [ThomasAlbin's Space Science Tutorials](https://towardsdatascience.com/@thomas.albin)

*“It has been said that astronomy is a humbling and character-building experience.” - Carl Sagan*

Zain Kamal -- z.kamal2021@gmail.com
Feel free to reach out with literally anything, I'm so bored.

# Background
NASA’s Navigation and Ancillary Information Facility (NAIF) at the Jet Propulsion Laboratory (JPL) built the SPICE (Spacecraft, Planet, Instrument, and C-matrix Events) ancillary information system to help scientists and engineers analyze scientific observations obtained from robotic spacecraft, compute geometric information used in planning missions, and conduct the numerous engineering functions needed to carry out those missions. SPICE has been used on nearly every worldwide planetary science mission since the time of the Magellan mission to Venus.

**I use a python wrapper for the [C-SPICE library](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/) called [SpiceyPy by Andrew Annex](https://github.com/AndrewAnnex/SpiceyPy).**

# Project 0: I Hate My Life
After 3 months of wrestling with VSCode, I gave up and wiped my entire OS. Packages work now!
Exploring the basic functions of SPICE, mainly accessing kernels. Verifying position values by comparing SPICE's 3D velocity vector with the manually calculated orbital velocity of Earth.

# Project 1: Understanding Kepler’s First Law
**In this project, I modeled the trajectory of the solar system barycenter (blue) with respects to the center of the sun (yellow), projected onto the ecliptic plane.**
[](include the image!!)
Kepler's first law of planetary motion: "The orbit of a planet is an ellipse with the Sun at one of the two foci"
(Kepler and Brahe derived this 400 years ago by through pure observation, manual calculations, and the 17th-century-Germany equivalent of caffeine pills. Their work ethic is so intense that it hurts me, sometimes, to read about it.)
Although the Sun contains over 99% of the solar system’s mass, it isn’t the solar system’s center of mass (the point about which all planets and asteroids orbit). In astronomy, that point is defined as the barycenter.

# Project 2: Planetary Dances (or Astronomical Waltzes) -- Building off of Project 1
**This project investigated the causes of the solar system barycenter’s (SSB) movement. The computations and visualisations of various phase angles reveal that the four gas giants (Jupiter, Uranus, Saturn, Neptune) are the main reason of the movement of the Solar System Barycentre as introduced in Project 1. The blue curve (left axis) plots the distance between the SSB and the Sun (in solar radii) vs time (in UTC). The orange curve (right axis) shows the phase angle between the planet and the SSB as seen from the Sun (in degrees).**
The large time interval between the maximum and minimum distances indicate that the inner planets cannot be the main contributors of this gravitational pull -- otherwise we would see more short time spikes and variations that correlate with shorter orbital periods. We can analyse the distance between the Sun and the SSB using the phase angle between the SSB and the gas giants as seen from the Sun. It appears that Jupiter is a major factor (since it is the most massive planet and only 5 AU away). However, the other giants cannot be neglected, considering the minimum distance of 0.5 Solar Radii between the years 2012 and 2016. You can see that the phase angles for Saturn, Uranus and Neptune are way larger and create a “counter gravity pull” to the other direction causing the SSB’s position to stay within the Sun. Between 2020 and 2024 the gas giants are more aligned to the same direction causing a maximum distance of almost 2 Solar Radii! [](include some technical stuff on phase angles)

[](# Project 3: Basic N-Body Simulation
In physics and astronomy, an N-body simulation is a simulation of a dynamical system of particles, usually under the influence of physical forces, such as gravity. 
My system is fairly simple, just the Sun + 8 planets. This was more for fun (and so I can say that I """wrote an N-Body simulation"""").)
I might use vpython for better 3d simulations?