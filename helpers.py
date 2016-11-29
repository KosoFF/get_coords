import math


def dconv(measure):
    dc = []
    #nm
    dc.insert(0, 1.)
    #  km
    dc.insert(1, 1.852)
    # sm
    dc.insert(2, 185200.0 / 160934.40)
    #  ft
    dc.insert(3, 185200.0 / 30.48)

    dc.insert(4, 1852.)

    return dc[measure]


# def signlatlon(cond):
#     if cond == 'n' or cond == 'w':
#         sign = 1
#     elif cond == 's' or cond == 'e':
#         sign = -1
#     else:
#         raise NameError('singlatlon arguments are n, s, w or e')
#     return sign


def check_field(field):
    str=field
    latlon=parselatlon(field)
    # if (str.substring(0,3)=="lat"):
    #    if (latlon > 90.):
    #       print("Latitudes cannot exceed 90 degrees")
    #       return 0
    #
    #
    # if (str.substring(0,3)=="lon"):
    #    if (latlon > 180.):
    #       print("Longitudes cannot exceed 180 degrees")
    #       return 0
    return latlon

def parselatlon(instr):
    try:
        str=float(instr)
    except ValueError:
        print "cannot parse lat or lon"
        return 0.
    # if str < 0:
    #     return 0.
    # else:
    #     return float(str)
    return str


def ellipsoid(name, a, invf):
    # /* constructor */
    class Ellipsoid:
        def __init__(self):
            self.name = None  # or whatever
            self.a = None
            self.invf = None
    ell = Ellipsoid()
    ell.name = name
    ell.a = a
    ell.invf = invf
    return ell

def getEllipsoid(ell):
    ells = [{} for i in range(10)]
    ells[1]= ellipsoid("Sphere", 180*60/ math.pi,"Infinite") # first one
    ells[2]= ellipsoid("WGS84",6378.137/1.852,298.257223563)
    ells[3]= ellipsoid("NAD27",6378.2064/1.852,294.9786982138)
    ells[4]= ellipsoid("International",6378.388/1.852,297.0)
    ells[5]= ellipsoid("Krasovsky",6378.245/1.852,298.3)
    ells[6]= ellipsoid("Bessel",6377.397155/1.852,299.1528)
    ells[7]= ellipsoid("WGS72",6378.135/1.852,298.26)
    ells[8]= ellipsoid("WGS66",6378.145/1.852,298.25)
    ells[9]= ellipsoid("FAI sphere",6371.0/1.852,1000000000.)
    return ells[ell]

def degtodm(deg,decplaces):
 # returns a rounded string DD:MM.MMMM
    deg1=math.floor(deg)
    min=60.*(deg-math.floor(deg))
    mins=format(min,decplaces)
    print ("deg1="+str(deg1)+" mins="+mins)
  # rounding may have rounded mins to 60.00-- sigh
    if (mins.substring(0,1)=="6" and mins >59.0):
        deg1 +=1
        mins=format(0,decplaces)

    return str(deg1)+":"+str(mins)
