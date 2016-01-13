'''
	Author: Prakhar Mishra
	Date: 11/01/2016
'''

# Importing packages
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread
import csv

# Opening and getting marker for input file
data = open(str(sys.argv[1]), 'r')
data_reader = csv.reader(data)

# Reads only the tweets and appends it into 
# places list
places = []
for line in data_reader:
	if line[1] != 'None':
		places.append(line[1])
	else:
		pass

# Joins all the tweets sepeated with space
words = ' '.join(places)

# Background Image
twitter_mask = imread('twitter_mask.png', flatten=True)

# Cleans
final_tweets = " ".join([word for word in words.split()
                            if not word.startswith('@') and word != 'ude' and word != 'n' and word != 'udc'
                            ])

wc = WordCloud(
					  font_path = 'CabinSketch-Regular.ttf',
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1050,
                      height=850,
                      mask=twitter_mask
            ).generate(final_tweets)


plt.imshow(wc)
plt.axis("off")
plt.show()

