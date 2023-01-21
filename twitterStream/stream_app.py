from pyspark.streaming import StreamingContext
import shutil
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import Row, SQLContext, SparkSession

def aggregate_tags_count(new_values, total_sum):
	return sum(new_values) + (total_sum or 0)


checkpoint_path = r"C:\User\AminFarvardin\Downloads\twitterckpoint"
shutil.rmtree(checkpoint_path, ignore_errors=True)

sc = SparkContext("local[4]", "TwitterStreamApp")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 2)
sqlContext = SQLContext(sc)

ssc.checkpoint(checkpoint_path)

dataStream = ssc.socketTextStream("127.0.0.1", 9009)

words = dataStream.flatMap(lambda line: line.split(" "))
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))

tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
tags_totals.pprint()

ssc.start()
ssc.awaitTermination()
