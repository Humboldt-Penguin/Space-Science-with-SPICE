Personal notes for [ThomasAlbin's Space Science Tutorials](https://towardsdatascience.com/@thomas.albin)

*“It has been said that astronomy is a humbling and character-building experience.” - Carl Sagan*

Zain Kamal -- z.kamal2021@gmail.com

# Background
NASA’s Navigation and Ancillary Information Facility (NAIF) built the SPICE (Spacecraft, Planet, Instrument, and C-matrix Events) ancillary information system to help scientists and engineers analyze scientific observations obtained from robotic spacecraft, compute geometric information used in planning missions, and conduct the numerous engineering functions needed to carry out those missions. SPICE has been used on nearly every worldwide planetary science mission since the time of the Magellan mission to Venus.

**I use a python wrapper for the [C-SPICE library](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/) called [SpiceyPy by Andrew Annex](https://github.com/AndrewAnnex/SpiceyPy).**

Project_0 is for testing packages and verifying computations with physics: SPICE, MatPlotLib, NumPy, and VPython.

# Project 1: Wobbly Sun
**In this project, I modeled the trajectory of the solar system barycenter (blue) with respects to the center of the sun (yellow), projected onto the ecliptic plane.**

![Figure_1](https://i.imgur.com/s6zapjb.png)


# Project 2: Astronomical Waltzes [Unfinished]
**This project builds off of project 1 by investigating the causes of the solar system barycenter’s (SSB) movement. The computations and visualisations of phase angles reveal that the four gas giants (Jupiter, Uranus, Saturn, Neptune) are the main reason of the movement of the Sun relative to the Solar System barycenter. The blue curve (left axis) plots the distance between the SSB and the Sun (in solar radii) vs time (in UTC). The orange curve (right axis) shows the phase angle between the planet and the SSB as seen from the Sun (in degrees).**

![Figure 2](https://i.imgur.com/0QcmeC1.png)

The large time interval between the maximum and minimum distances indicate that the inner planets cannot be the main contributors of this gravitational pull -- otherwise we would see more short time spikes and variations that correlate with shorter orbital periods. We can analyse the distance between the Sun and the SSB using the phase angle between the SSB and the gas giants as seen from the Sun. It appears that Jupiter is a major factor (since it is the most massive planet and only 5 AU away). However, the other giants cannot be neglected, considering the minimum distance of 0.5 Solar Radii between the years 2012 and 2016. You can see that the phase angles for Saturn, Uranus and Neptune are way larger and create a “counter gravity pull” to the other direction causing the SSB’s position to stay within the Sun. Between 2020 and 2024 the gas giants are more aligned to the same direction causing a maximum distance of almost 2 Solar Radii! [](include some technical stuff on phase angles)

# Project 3: Basic N-Body Simulation [Unfinished]
An N-body simulation is a simulation of a dynamical system of particles, usually under the influence of physical forces, such as gravity. This project simulates the movement of the Sun and 8 planets by calculating the net force they exert on each other. VPython is used for 3D simulations.