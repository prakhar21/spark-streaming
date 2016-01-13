'''
    Author: Prakhar Mishra
    Date: 12/1/2016
'''

# Importing packages
from collections import Counter
import csv
import matplotlib.pyplot as plt
import random
import re
from pylab import *
import sys

# Opens tweets file and get marker
data = open(str(sys.argv[1]), 'r')
data_reader = csv.reader(data)


###############################################################################
########################### GEO INFORMATION ###################################
###############################################################################

# Grabs only the geo information columns
# 4th columns has data for geo information
geo = []
for line in data_reader:
	geo.append(line[3])


# Counts each occurence except header
# and stores as dictionary
geo = geo[1:]
x = Counter(geo)
total_count = dict(x)


# Plotting the geo count per region
# Setting figure size and other parameters
fig = plt.figure(figsize=(13, 11), facecolor='white', edgecolor='white')

top_loc = []
labels = []
fractions = []

# Display top count only
max_20 = Counter(total_count)
for c in max_20.most_common(20):
	if c[0] == 'null' or c[0] == '0' or c[0] == 'Location data not found !!':
		pass
	else:
		top_loc.append(c)

# Appends locations in labels list
# 0th index - label
# 1st index - count - TUPLE CASE
for i in top_loc:
	labels.append(i[0])

# Appends count on fractions list
for i in top_loc:
	fractions.append(i[1])

# Cleans the labels
regex = "(\")"
labels = [re.sub(regex,'',i) for i in labels]

#Plot the pie chart
plt.pie(fractions,labels = labels,shadow = False)
title('Top 17 Locations', bbox={'facecolor':'0.8', 'pad':10})


###############################################################################
################################# SENTIMENT ###################################
###############################################################################

'''
data_readr = csv.reader(data)
# Grabs only the sentiment score
senti = []
for l in data_readr:
	senti.append(l[4])

senti = senti[1:]
x = Counter(senti)
total_count = dict(x)


two_senti_score = total_count["['2']"]
four_senti_score = total_count["['4']"]
zero_senti_score = total_count["['0']"]

labels = ['2','4','0']
fractions = [two_senti_score, four_senti_score, zero_senti_score]
plt.pie(fractions,labels = labels,shadow = False)
title('Sentiment Score Count', bbox={'facecolor':'0.8', 'pad':10})
'''
plt.show()

