import geo
import geometry
import math


# Enter coordinates of station center
station_center = geo.Coordinates()
station_center.lat = 55.736098
station_center.lon = 37.595020

# Add relative coordinates of station edge
edge = []
edge.append(geometry.Point(-30, -60))
edge.append(geometry.Point(30, -60))
edge.append(geometry.Point(30, 60))
edge.append(geometry.Point(-30, 60))

# Add azimuth
azimuth = 330


t = geometry.get_absolute_coordinates(edge, station_center, azimuth)

for p in t:
    print "________________"
    print p.lat
    print ','
    print p.lon

# a = geo.compute_form_dir('55.736093',  '37.595041', 100, 90, 4)
# print a.lat
# print a.lon
#
# print geometry.get_direction(edge[1])
# print geometry.get_distance(edge[1])
#
#
# p = geometry.rotate(edge[1], math.pi/2)
# print p.x
# print p.y