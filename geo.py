import math
import helpers


class Coordinates:
    def __init__(self):
        self.lat = None  # or whatever
        self.lon = None
        self.crs = None


# MEASURES
# 0. Nautical mile
# 1. km
# 2. sm
# 3. feet
# 4. meters
# Direction:
# 0/360 NORTH
def compute_form_dir(lat1, lon1, distance, direction, measure):
    #  Input and validate data

    # signlat1 = helpers.signlatlon(ns1)
    # signlon1 = helpers.signlatlon(ew1)
    # lat1 = (math.pi / 180) * signlat1 * helpers.check_field(lat1)
    # lon1 = (math.pi / 180) * signlon1 * helpers.check_field(lon1)
    lat1 = (math.pi / 180) * helpers.check_field(lat1)
    lon1 = (math.pi / 180) * helpers.check_field(lon1)
    d12 = distance

    # /* get distance conversion factor */
    dc = helpers.dconv(measure)
    d12 /= dc
    # print ("dc=" + str(dc) + "      dis=" + str(d12))

    crs12 = direction * math.pi / 180.  # radians
    # print ("lat1=" + str(lat1) + " lon1=" + str(lon1) + " d12=" + str(d12) + " crs12=" + str(crs12))

    # get ellipse
    ellipse = helpers.getEllipsoid(2)  # can use constantly wgs84 ellipsoid for our needs (number 2)

    if (ellipse.name == "Sphere"):
        # spherical code
        d12 /= (180 * 60 / math.pi)  # in radians
        cd = direct(lat1, lon1, crs12, d12)
        lat2 = cd.lat * (180 / math.pi)
        lon2 = cd.lon * (180 / math.pi)
    else:
        # elliptic code
        cde = direct_ell(lat1, -lon1, crs12, d12, ellipse)  # ellipse uses East negative
        lat2 = cde.lat * (180 / math.pi)
        lon2 = -cde.lon * (180 / math.pi)  # ellipse uses East negative
    print ("crs12=" + str(crs12))

    if (lat2 >= 0):
        ns2 = "N"
    else:
        ns2 = "S"

    if (lon2 > 0):
        ew2 = "W"
    else:
        ew2 = "E"

    out = Coordinates()
    out.lat = math.fabs(lat2)
    out.lon = math.fabs(lon2)
    out.ns = ns2
    out.ew = ew2
    return out


#     out.lat = degtodm(Math.abs(lat2),decpl)
# lat2s=degtodm(Math.abs(lat2),decpl)
# document.OutputFormDir.lat2.value=lat2s
# lon2s=degtodm(Math.abs(lon2),decpl)
# document.OutputFormDir.lon2.value=lon2s



def direct(lat1, lon1, crs12, d12):
    EPS = 0.00000000005

    if (math.fabs(math.cos(lat1)) < EPS) or not (math.fabs(math.sin(crs12)) < EPS):
        print ("Only N-S courses are meaningful, starting at a pole!")

    lat = math.asin(math.sin(lat1) * math.cos(d12) +
                    math.cos(lat1) * math.sin(d12) * math.cos(crs12))
    if (math.fabs(math.cos(lat)) < EPS):
        lon = 0.  # endpoint a pole
    else:
        dlon = math.atan2(math.sin(crs12) * math.sin(d12) * math.cos(lat1),
                          math.cos(d12) - math.sin(lat1) * math.sin(lat))
        lon = math.fmod(lon1 - dlon + math.pi, 2 * math.pi) - math.pi

    # print(
    # "lat1=" + lat1 + " lon1=" + lon1 + " crs12=" + crs12 + " d12=" + d12 + " lat=" + str(lat) + " lon=" + str(lon))

    out = Coordinates()  # temp object for return
    out.lat = lat
    out.lon = lon
    return out


def direct_ell(glat1, glon1, faz, s, ellipse):
    # glat1 initial geodetic latitude in radians N positive
    # glon1 initial geodetic longitude in radians E positive
    # faz forward azimuth in radians
    # s distance in units of a (=nm)

    EPS = 0.00000000005

    if ((math.fabs(math.cos(glat1)) < EPS) and not (math.fabs(math.sin(faz)) < EPS)):
        print("Only N-S courses are meaningful, starting at a pole!")

    a = ellipse.a
    f = 1 / ellipse.invf
    r = 1 - f
    tu = r * math.tan(glat1)
    sf = math.sin(faz)
    cf = math.cos(faz)
    if (cf == 0):
        b = 0.
    else:
        b = 2. * math.atan2(tu, cf)  # check if atan2 works correctly!!!

    cu = 1. / math.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1. + math.sqrt(1. + c2a * (1. / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1. - x
    c = (x * x / 4. + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1
    assert math.fabs(y - c) > EPS
    while (math.fabs(y - c) > EPS):
        sy = math.sin(y)
        cy = math.cos(y)
        cz = math.cos(b + y)
        e = 2. * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4. - 3.) * y * cz * d / 6. + x) *
             d / 4. - cz) * sy * d + tu

    b = cu * cy * cf - su * sy
    c = r * math.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = modlat(math.atan2(d, c))
    c = cu * cy - su * sy * cf
    x = math.atan2(sy * sf, c)
    c = ((-3. * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = modlon(glon1 + x - (1. - c) * d * f)  # fix date line problems
    baz = modcrs(math.atan2(sa, b) + math.pi)

    out = Coordinates()  # temp out array
    out.lat = glat2
    out.lon = glon2
    out.crs = baz
    return out


def mod(x, y):
    return x - y * math.floor(x / y)


def modlon(x):
    return mod(x + math.pi, 2 * math.pi) - math.pi


def modcrs(x):
    return mod(x, 2 * math.pi)


def modlat(x):
    return mod(x + math.pi / 2, 2 * math.pi) - math.pi / 2
