# How to run Spark Streaming - socketTextStream

If you have already downloaded and built Spark, you can run this example as follows. 
You will first need to run Netcat (a small utility found in most Unix-like systems) as a data server by using 'nc' command line

# For Windows users (Linux commands in following)
Download the _ncat_ from the link below:

https://schilleriu-my.sharepoint.com/:u:/g/personal/amin_farvardin_faculty_schiller_edu/EapqQ5yhNn1GneqZucpxk3sBsyybwZ9zCwumqRtxXHeOag?e=K7sdkN
Extract it then open a terminal in the extracted path. Run the below commands:

### TERMINAL 1 
> ncat -l -p 9999

Then, in a different terminal, you can start the example by using the below command
## TERMINAL 2:
$ ./bin/spark-submit examples/src/main/python/streaming/network_wordcount.py localhost 9999

### TERMINAL 3 - Type some text in 
> echo Hello | ncat localhost 9999

-------------------------------------

# For Linux users
## TERMINAL 1
$ nc -lk 9999


Then, in a different terminal, you can start the example by using the below command
## TERMINAL 2:
$ ./bin/spark-submit examples/src/main/python/streaming/network_wordcount.py localhost 9999

## TERMINAL 1 - Type some text in 
for example: _hello world_




