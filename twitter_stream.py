'''
    Author: Prakhar Mishra
    Date: 9/01/2016
'''

# Importing Packages
from __future__ import print_function
import sys
import json
import re
import urllib2
from collections import Counter

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import nltk
import csv


t0_original = ''
data = {}
data_tweet_geo = {}
removal_list = ['\\','/',',','(',')','!',':','.']


# open output file
outfile_all = open('/home/prakhar/Downloads/spark-1.5.0/SocialCops_Task_SoftwareChallenge/tweet_task.csv', "w" )
# get a csv writer
writer = csv.writer(outfile_all)
writer.writerow(['Original-Tweets','Tweets','Wordcount','Geo-Information','Sentiment-Score'])


# Importing English StopWords
stop = stopwords.words('english')

if __name__ == "__main__":

    sc = SparkContext(appName="PythonStreamingTwitter")
    ssc = StreamingContext(sc,2)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])

    # Extracts the text
    def getText(x):
        global t0_original

        regex01 = "\"id_str\":\"[0-9]+\",\"text\":\s*\"(.+?)\",\"source\""
        t0 = re.findall(regex01,x)
        
        # Cleans Text
        t0 = cleanText(t0)
        
        # Get Intent
        # t0_intent = getIntent(t0)

        t0_original = t0
    
        #Get Sentiment
        senti = getSentiment(t0)
        
        
        # # Removes Stopwords
        t0 = removeStopWords(t0)
        
        # # Counts Word
        to_wc = countWords(t0)


        # # Gets Geo-Location 
        geo = getGeoLocation(x)


        if type(geo) is list:
            if len(geo) != 0:
                geo = geo[0]
            else:
                geo = 0
        else:
            geo = geo

        # Returns Tweet , WordCount , Location
        return [str(t0_original),str(t0),str(to_wc),str(geo),str(senti)]
        # return [str(t0),str(t0_intent)]

    # Cleans the tweet
    def cleanText(x):
        if len(x) != 0:
            try:
                # Remove Links
                regex02 = 'https:.+'
                t1 = re.sub(regex02,'',x[1])                
            except:
                # Remove Links
                regex02 = 'https:.+'
                t1 = re.sub(regex02,'',x[0])
                
            # Remove unicode and punctuations
            tknzr = TweetTokenizer(reduce_len=True)
            a = tknzr.tokenize(t1)
            
            #Unicode remover    
            regex03 = 'u[a-zA-Z0-9]{4}'
            
            # Pnctuations remover
            c = [i for i in a if i not in removal_list]
            c = " ".join(c)
            k = re.sub(regex03,'',str(c))

            return k

    # Remove Stop words
    def removeStopWords(x):
        if x != None:
            x = x.split()
            z = [i for i in x if i not in stop]
            y = " ".join(z)
            return y

    # Gets sentiment score from Sentiment140 API
    def getSentiment(x):
        if x != None:
            x = '{"data": [{"text":'+str(x)+'}]}'
            regex = '\"polarity\":([0-4])'
            response = urllib2.urlopen('http://www.sentiment140.com/api/bulkClassifyJson?appid=pmprakhargenius@gmail.com?text=', x)
            page = response.read()
            t1 = re.findall(regex,page)
            return t1

    # Get Geo-Location
    def getGeoLocation(data):
        if data != None:
            
            # Regular Expression
            # For geo_enabled tag
            # For place tag
            # For name in place tag
            # For timezone tag
            # For location tag
            regex01 = "\"geo_enabled\":\s*(.+?),"
            regex02 = "\"place\":\s*(.+?)\"contributors\""
            regex02_01 = "\"name\":\s*(.+?),\""
            regex03 = "\"time_zone\":\s*(.+?),"
            regex04 = "\"location\":\s*(.+?),"

            # Finds all the occurences of geo_enabled
            t0 = re.findall(regex01, data)
            # return t0
            
            # t0 - list
            # t0[1] - geo_tag of Original text
            if len(t0) > 1:
                t0 = t0[1]
            elif len(t0) == 1:
                t0 = t0[0]
            # try:
            #     # if t[1] - original text exists
            #     t0 = t0[1]
            # except:
            #     # When only t[0] - exists
            #     t0 = t0[0]
            # If geo_enabled tag is 'true'
            if str(t0) == 'true':
                # Search for all the occurence of place tag
                t1 = re.findall(regex02, data)
                # print t1
                if len(t1) > 1:
                    t1 = t1[1]
                elif len(t1) == 1:
                    t1 = t1[0]
                
                # Check for t1 if it's not null
                if t1 != 'null,':
                    # Extract Name tag from there
                    t1_1 = re.findall(regex02_01, t1)
                    return t1_1
                elif t1 == 'null,':
                    # Extract timezone tag
                    t2 = re.findall(regex03, data)
                    # print t2
                    if len(t2) > 1:
                        t2 = t2[1]
                    elif len(t1) == 1:
                        t2 = t2[0]

                    if t2 != 'null':
                        return t2
                    elif t2 == 'null':
                        # Extract Location Tag
                        t3 = re.findall(regex04, data)
                        if len(t3) > 1:
                            t3 = t3[1]
                        elif len(t3) == 1:
                            t3 = t3[0]

                        if t3 != 'null':
                            return t2
                        elif t3 == 'null':
                            return 'Location data not found !!'
            # Geo_tag not found condition
            else:
                # Extract timezone tag
                    t2 = re.findall(regex03, data)
                    # print t2
                    if len(t2) > 1:
                        t2 = t2[1]
                    elif len(t2) == 1:
                        t2 = t2[0]

                    if t2 != 'null':
                        return t2
                    elif t2 == 'null':
                        # Extract Location Tag
                        t3 = re.findall(regex04, data)
                        
                        if len(t3) > 1:
                            t3 = t3[1]
                        elif len(t3) == 1:
                            t3 = t3[0]

                        if t2 != 'null':
                            return t2
                        elif t2 == 'null':
                            return 'Location data not found !!'
            

    # Word Count for tweet
    def countWords(x):
        if x != None:
            x = x.split()
            y = Counter(x)
            y = dict(y)
            # Cleans the dictionary contaaining wordcount
            # u'xyz' -> u' '
            regex01 = "(u'|['])"
            y = re.sub(regex01,"",str(y))
            return y      


    def getIntent(x):
        tknzr = TweetTokenizer(reduce_len=True)
        a = tknzr.tokenize(x)
        # # # print "Twitter tokens: ", a
        tagged = nltk.pos_tag(a)
        # # # print 'Tagged: ', tagged

        y = []
        for x in tagged:
            if x[1] == 'VB':
                return x[0]
            else:
                return 'No Verb Found'

    def saveDataToFile(x):
        x = x.collect()
        for data in x:
            writer.writerow([data[0],data[1],data[2],data[3],data[4]])
            # writer.writerow([data[0],data[1]])

    # Get Geo-Location
    # loc = lines.map(getGeoLocation)
    # loc.pprint()
    
    # Get Tweets
    tweets = lines.map(getText)
    tweets.foreachRDD(saveDataToFile)

    #tweets.pprint()

    
    # Sentiment140 Usage
    # senti = tweets.map(getSentiment)
    # senti.foreachRDD(appendToList)
    # senti.pprint()
    ssc.start()
    ssc.awaitTermination()
