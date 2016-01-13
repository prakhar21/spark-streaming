'''
  Author: Prakhar Mishra
'''

from monkeylearn import MonkeyLearn
from nltk.tokenize import TweetTokenizer
import csv
import sys
import nltk
from gensim.models import Word2Vec
from nltk.corpus import brown
from nltk.corpus import stopwords
import re


# open output file
outfile_all = open('/home/prakhar/Downloads/spark-1.5.0/SocialCops_Task_SoftwareChallenge/tweet_task_intent_test.csv', "w" )
# get a csv writer
writer = csv.writer(outfile_all)
writer.writerow(['Tweets','Similar Words','Topic'])

# Importing English StopWords
stop = stopwords.words('english')

# train model on brown corpus
model = Word2Vec(brown.sents())
print 'Model Trained'

# Opens tweets file
data = open(str(sys.argv[1]), 'r')
data_reader = csv.reader(data)

tweets = []
helping_verbs = ['am', 'are', 'is', 'was', 'were', 'be', 'being', 'been' , 'it\'s',
					'have', 'has', 'had' ,'shall', 'will' ,'do', 'does', 'did' ,
					'may', 'must', 'might' ,'can', 'could', 'would', 'should' ]

removal_list = ['"','\'','-','udd','ude','ss','n','e']
# Reads and extract original_tweets column only
for line in data_reader:
	tweets.append(line[0])


# print tweets[1:3]
# Token for Monkeylearn
token = 'fe0f50a0bd4cfc710010309992cf97a49cc18af9'
ml = MonkeyLearn(token)
module_id = 'cl_5icAVzKR'

tknzr = TweetTokenizer(reduce_len=True)
# Extracts just the verbs from all POS tags


# Return topic for tweet
def getTopicForTweet(x):
	text_list = [str(i)]
	try:
		res = ml.classifiers.classify(module_id, text_list)
		return res.result
	except Exception as e:
		return e

	
# Iterates for all the tweets and performs operations
for i in tweets[1:]:

	# Tokenization and cleaning tweets
	tweet_toknized = tknzr.tokenize(i)
	tweet_toknized = [re.sub('@.+','',str(i)) for i in tweet_toknized]
	tweet_toknized = [re.sub('\.+','',str(i)) for i in tweet_toknized]
	tweet_toknized = [re.sub('RT+','',str(i)) for i in tweet_toknized]
	tweet_toknized = [i for i in tweet_toknized if i not in removal_list]
	tweet_toknized = [i for i in tweet_toknized if i != '']
	tweet = " ".join(tweet_toknized)
	print 'TWEET: ' , tweet
	
	# Part of speech tagging
	tagged = nltk.pos_tag(tweet_toknized)

	verbs = []
	# Gets all the verbs from tweets
	for x in tagged:
	    if x[1] == 'VB':
	        verbs.append(x[0])

	# Helping verbs removed
	verbs_main = list(set(verbs)-set(helping_verbs))
	# Check for if there is something to iterate or not
	if len(verbs_main) != 0:
		for y in verbs_main:
		 	print 'Verb: ' , y
			try:
				# Result with word2vec
				result_model = model.most_similar(str(y), topn=3)
				print 'SIMILAR: ' , result_model
				# get topic
				tpic1 = getTopicForTweet(str(i))
	 			print "TOPIC: " , tpic1
	 		except:
	 			tpic1 = getTopicForTweet(str(i))
	 			print tpic1
	else:
		# when no verbs then get topic
		tpic1 = getTopicForTweet(str(i))
		print "TOPIC: " , tpic1

	print '-'*120

	writer.writerow([str(tweet) , str(result_model) , str(tpic1)])

