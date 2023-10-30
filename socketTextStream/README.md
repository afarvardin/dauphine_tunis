# How to run Spark Streaming - socketTextStream

If you have already downloaded and built Spark, you can run this example as follows. 
You will first need to run Netcat (a small utility found in most Unix-like systems) as a data server by using the 'nc' command line

# For Windows users (Linux commands in following)
In case you do not have _ncat_ on your machine you can download it from the link below:

https://nmap.org/download.html

Extract it then open a terminal in the extracted path. Run the below commands:

### TERMINAL 1 
> ncat -l -p 9999

Then, in a different terminal, you can start the example by using the below command
## TERMINAL 2:
To find the Spark directory on your machine, here is the command the you need to type in _spark-shell_:
> scala> sc.getConf.get("spark.home")

Then from the main directory of Spark, run the command below:
> $ ./bin/spark-submit examples/src/main/python/streaming/network_wordcount.py localhost 9999

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




