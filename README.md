# Twitter Spark Streaming using PySpark
![Twitter Spark Streaming](https://github.com/prakhar21/spark-streaming/blob/master/twitter_spark.png)

##### * Testing Environment *   ( On Virtual Machine )
* Ubuntu - 12.04   ( 32 bit )
* 8GB Ram
* i7 - QuadCore
##### Contents in folder:
  
  - tweepy_kafka_producer.py ( Publishes tweets to kafka topic )
  - twitter_stream.py ( Process the tweets )
  - tweet_task.csv ( Sample output file )
  - get_intent.py ( classifies into topics )
  - generate_Map.py ( Visualizes geo points on map )
  - draw_Pies.py ( draws pie charts )
  - generate_cloud.py ( draws word cloud )
  - my_map.html ( locations plotted map )
  - figure_1.png ( Word cloud )
  - figure_2.png ( pie plot for top 17 locations )
  - tweet_task_intent.csv ( Contains tweet , intent , topic )

### Pipeline Structure
> Data is ingested in realtime using tweepy ( Twitter API ) and is sent to the producer which publishes it to some user defined topic in kafka. 

> We then create a consumer, which subscribes to the topic and eventually gets the data.


### Technologies Used

This application uses a number of open source technologies to work properly:

* Apache Spark 1.5.0 - Big Data Processing Engine
* Tweepy - Twitter Application Programming Interface
* Kafka - Messaging System
* Sublime Text Editor - Text Editor
* Python 2.7 - Programming Language
* Sentiment140 - API

### Python Packages Used
*    matplotlib , wordcloud ,scipy ,geocoder
*   re , pylab , webbrowser , pygmaps 
*   json , nltk , collections , urllib2
*   gensim , monkeylearn , random, csv



# Kafka Commands
#### Starts Zookeeper Server:
```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```
#### Starts Kafka Server:
```sh
$ nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > ~/kafka/kafka.log 2>&1 &
```
#### Create Topic ( t ):
```sh
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic socialcops
```
#### Start Producer:
```sh
$ python tweepy_kafka_producer.py
```
#### Start Consumer ( another terminal ):
From inside Spark directory -
```sh
$ bin/spark-submit --master local[3] --jars external/kafka-assembly/target/scala-2.10/spark-streaming-kafka-assembly-1.5.0.jar SocialCops_Task_SoftwareChallenge/twitter_stream.py localhost:2181 socialcops

```
#### Analyse Intent and Topic ( saves to tweet_task_intent.csv )
```sh
$ python get_intent.py tweet_task.csv
```
#### Draw Pie Charts:
```sh
$ python draw_pies.py tweet_task.csv
```
#### Plot on map
```sh
$ python generate_Map.py tweet_task.csv
```

#### Draw WordCloud
```sh
$ python generate_cloud.py tweet_task.csv
```
License
----
Prakhar Mishra
