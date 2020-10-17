# Basic N-Body simulation, mainly just playing with vectors and vpython -- can we animate the Sun's "wobble" ?

import spiceypy
import vpython
import datetime

# import numpy


spiceypy.furnsh("Project_3/meta_kernel.txt")

# ---------------------------------------------------

et = spiceypy.utc2et("01 JAN 1950 0:0:0")
G = 0.000000000066743


# ---------------------------------------------------
# Create a dictionary with initial values of 8 bodies

# Bodies: sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
given = (
    "SUN",
    (10, 10),
    "MERCURY",
    (199, 199),
    "VENUS",
    (299, 299),
    "EARTH",
    (399, 399),
    "MARS",
    (499, 4),
    "JUPITER",
    (599, 5),
    "SATURN",
    (699, 6),
    "URANUS",
    (799, 7),
    "NEPTUNE",
    (899, 8),
)

BODIES = {}

for i in range(0, 18, 2):
    BODIES[given[i]] = {
        "ID_body": given[i + 1][0],
        "ID_barycenter": given[i + 1][1],
    }


# fmt: off
for body in BODIES:
    update = {
        "MASS_kg": (spiceypy.bodvcd(bodyid=BODIES[body]["ID_body"], item="GM", maxn=1)[1][0] / G * 1000000000),
        "POSwrtSSB_km": spiceypy.spkgeo(targ=BODIES[body]["ID_barycenter"], et=et, ref="ECLIPJ2000", obs=0)[0][:3],
        "VELwrtSSB_km/s": spiceypy.spkgeo(targ=BODIES[body]["ID_barycenter"], et=et, ref="ECLIPJ2000", obs=0)[0][3:],
        "RADIUS_km": spiceypy.bodvcd(bodyid=BODIES[body]["ID_body"], item="RADII", maxn=3)[1][0]
    }
    # print("pos %s " % spiceypy.spkgeo(targ=BODIES[body]["ID_barycenter"], et=et, ref="ECLIPJ2000", obs=0)[0][:3])
    # print("vel %s " % spiceypy.spkgeo(targ=BODIES[body]["ID_barycenter"], et=et, ref="ECLIPJ2000", obs=0)[0][3:])
    BODIES[body].update(update)


# ---------------------------------------------------
# Create body objects in vpython

colors = (vpython.color.yellow, vpython.vec(206/255, 204/255, 209/255), vpython.vec(234/255, 191/255, 159/255), vpython.vec(0/255, 161/255, 255/255), vpython.vec(255/255, 81/255, 0/255), vpython.vec(255/255, 193/255, 166/255), vpython.vec(255/255, 240/255, 217/255), vpython.vec(179/255, 255/255, 198/255), vpython.vec(0/255, 0/255, 230/255))
color = 0

for body in BODIES:

    body_radius = BODIES[body]["RADIUS_km"]
    if body == "SUN":
        body_radius /= 20


    BODIES[body]["object"] = vpython.simple_sphere(
        pos=vpython.vector(BODIES[body]["POSwrtSSB_km"][0], BODIES[body]["POSwrtSSB_km"][1], BODIES[body]["POSwrtSSB_km"][2]),
        radius= body_radius * 500,  # 7_000_000, 
        # color=colors[color],
        # NOTE: make sure to comment out mr auyeung's face before pushing
        texture = "https://media-exp1.licdn.com/dms/image/C4E03AQEDA7rEZl0UaQ/profile-displayphoto-shrink_200_200/0?e=1602720000&v=beta&t=BGu8tJH0jLE3RwdyhZCbAyl80rVZ8yffmPT_UrhMMwM",
        # texture = "https://i.imgur.com/cxog7Tk.png",
        shininess = 0,
        make_trail=True,
        retain=50,
        trail_type="points",
        interval=2
    )
    color += 1

    BODIES[body]["object"].m = BODIES[body]["MASS_kg"]
    # print("%s: %f" % (body, BODIES[body]["object"].m))
    BODIES[body]["object"].p = BODIES[body]["MASS_kg"] * vpython.vector(BODIES[body]["VELwrtSSB_km/s"][0], BODIES[body]["VELwrtSSB_km/s"][1], BODIES[body]["VELwrtSSB_km/s"][2])


# print(BODIES["MERCURY"]["object"].pos)
# print(BODIES["MERCURY"]["object"].p)
# print(BODIES["MERCURY"]["object"].m)
# print(BODIES["MERCURY"]["object"].p / BODIES["MERCURY"]["object"].m)
# print(BODIES["MERCURY"]["VELwrtSSB_km/s"])


# ---------------------------------------------------
# METHOD 1: Runge Kutta/Euler's Method - Update momentum vectors
# ---------------------------------------------------

dt = 60 * 60

while True:

    vpython.rate(24)
    break

    for body_focus in BODIES: # on each body
        F_net = [0, 0, 0]

        for body_other in BODIES: # that is not the body in question

            if body_focus != body_other:

                distance_m = (BODIES[body_other]["object"].pos.x - BODIES[body_focus]["object"].pos.x) * 1000 # calculate the distance
                if distance_m > 0:
                    F_net[0] = F_net[0] + ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0)) # and add/subtract net force based on relative positions
                else:
                    F_net[0] = F_net[0] - ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0))


                distance_m = (BODIES[body_other]["object"].pos.y - BODIES[body_focus]["object"].pos.y) * 1000
                if distance_m > 0:
                    F_net[1] = F_net[1] + ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0))
                else:
                    F_net[1] = F_net[1] - ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0))


                distance_m = (BODIES[body_other]["object"].pos.z - BODIES[body_focus]["object"].pos.z) * 1000
                if distance_m > 0:
                    F_net[2] = F_net[2] + ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0))
                else:
                    F_net[2] = F_net[2] - ((spiceypy.bodvcd(bodyid=BODIES[body_focus]["ID_body"], item="GM", maxn=1)[1][0] * BODIES[body_other]["object"].m) / ((distance_m) ** 2.0))

        F_net = vpython.vector(F_net[0], F_net[1], F_net[2])

        BODIES[body_focus]["object"].p = BODIES[body_focus]["object"].p + (F_net / 1000) * dt


    for body_focus in BODIES:

        BODIES[body_focus]["object"].pos = BODIES[body_focus]["object"].pos + BODIES[body_focus]["object"].p * dt / BODIES[body_focus]["object"].m


# ---------------------------------------------------
# METHOD 2: Runge Kutta/Euler's Method - Update velocity components
# ---------------------------------------------------

dt = 1000


while True:

    vpython.rate(3600*24*100/1000)
    break

    for body_focus in BODIES:

        # update velocity
        for i in range(3):

            F_net = 0

            for body_other in BODIES: # calc net force on one axis

                if body_other != body_focus: # Calc net force

                    distance_km = (BODIES[body_other]["POSwrtSSB_km"][i] - BODIES[body_focus]["POSwrtSSB_km"][i])

                    if distance_km > 0:
                        F_net += (G * BODIES[body_focus]["MASS_kg"] * BODIES[body_other]["MASS_kg"]) / ((distance_km * 1000) ** 2.0)
                    else:
                        F_net -= (G * BODIES[body_focus]["MASS_kg"] * BODIES[body_other]["MASS_kg"]) / ((distance_km * 1000) ** 2.0)

            BODIES[body_focus]["VELwrtSSB_km/s"][i] = BODIES[body_focus]["VELwrtSSB_km/s"][i] + (((F_net / BODIES[body_focus]["MASS_kg"]) / 1000 ) * dt)
            # BODIES[body_focus]["VELwrtSSB_km/s"][i] += ((F_net / BODIES[body_focus]["MASS_kg"]) / 1000 ) * dt


    for body_focus in BODIES:

        for i in range(3):
            BODIES[body_focus]["POSwrtSSB_km"][i] += BODIES[body_focus]["VELwrtSSB_km/s"][i] * dt # Update position

        # update sphere pos
        BODIES[body_focus]["object"].pos.x = BODIES[body_focus]["POSwrtSSB_km"][0]
        BODIES[body_focus]["object"].pos.y = BODIES[body_focus]["POSwrtSSB_km"][1]
        BODIES[body_focus]["object"].pos.z = BODIES[body_focus]["POSwrtSSB_km"][2]


# possible fixes:
# make everything a sphere attribute: body.pos.x, body.v
# Introduce momentum

# ---------------------------------------------------
# METHOD 3: Brute force
# ---------------------------------------------------

t_utc = datetime.datetime(year=1950, month=1, day=1, hour=0, minute=0, second=0)
dt = 1
while True:
    vpython.rate(20)
    for body in BODIES:
        t_utc_str = t_utc.strftime("%Y-%m-%dT%H:%M:%S")
        t_et = spiceypy.utc2et(t_utc_str)
        pos = spiceypy.spkgeo(targ=BODIES[body]["ID_barycenter"], et=t_et, ref="ECLIPJ2000", obs=0)[0][:3]
        BODIES[body]["object"].pos = vpython.vector(pos[0], pos[1], pos[2])
        t_utc += datetime.timedelta(days=dt)
