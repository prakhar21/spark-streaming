'''
    Author: Prakhar Mishra
    Date: 13/01/2016
'''

# Importing Packages
import pygmaps
import webbrowser
import csv
import geocoder
import random
import re
import sys

# Opening and getting marker for the input file
data = open(str(sys.argv[1]), 'r')
data_reader = csv.reader(data)

# Reads only the geo information and appends it into 
# places list
places = []
for line in data_reader:
	places.append(line[3])

# Cleans the text
regex = "(\")"
s = [re.sub(regex,'',i) for i in places]

# From 1 because to skip the header
# s[0] - Header of csv
# Gets the latitite and longitute from names
count = 0
data_latlng = []
for i in s[1:]:
	if i != 'Location data not found !!':
		g = geocoder.google(str(i))
	 	dta = g.latlng
	 	if len(dta) != 0:
	 		data_latlng.append(g.latlng)
	 	else:
	 		pass
	else:
	 	pass


points = data_latlng

# # # Defining Center of map ( Portugal )
mymap = pygmaps.maps(37.933426, -7.496694, 3)

# For points in points, plots the data in maps
for i in points:
	mymap.addpoint(float(i[0]),float(i[1]),'#FF00FF')
 	mymap.draw('mymap.html')
 	print 'Drawn'
 	
# Opens the browser when plotting is complete
webbrowser.open_new_tab('mymap.html')



