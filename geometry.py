import math
import geo

class Point:
    def __init__(self, x=None, y=None, z=None):
        self.x = x  # or whatever
        self.y = y
        self.z = z
def rotate(point, angle):
    rotated_point = Point()
    rotated_point.x = point.x * math.cos(angle) - point.y * math.sin(angle);
    rotated_point.y = point.x * math.sin(angle) + point.y * math.cos(angle);
    return rotated_point;

def get_absolute_coordinates (points, center, direction):
    rdir = direction * math.pi/180
    npoints = []
    for point in points:
        npoints.append(rotate(point, -rdir))
    gpoints = []
    for npoint in npoints:
        gpoints.append(geo.compute_form_dir(center.lat, center.lon, get_distance(npoint),get_direction(npoint), 4))
    return gpoints

def get_distance (point):
    return math.sqrt((point.x ** 2 + point.y ** 2))


def get_direction (point):
    direct = math.atan2(point.y, point.x) - math.pi/2
    return to_degrees(direct)

def to_radians(angle):
    return angle * math.pi/180
def to_degrees(angle):
    return angle * 180/math.pi
