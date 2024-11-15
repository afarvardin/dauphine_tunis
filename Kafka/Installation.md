To run Kafka, you need to first install all the dependencies.

> sudo apt update
> sudo apt install default-jre
> sudo apt install openjdk-8-jre-headless

# Download Kafka
Head over to Apache [Kafka Downloads](https://kafka.apache.org/downloads) to check for the latest release. Right-click on the Binary downloads like and copy the link.

Or directly use the __wget__ command in WSL2 and provide it with the latest Kafka version
for example:
> wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.12-3.6.0.tgz

Then extract it.

> tar -xvzf kafka_2.12-3.6.0.tgz
**Note**: You can move the extracted file to any preferred location.

Configure your source file
At this point, you have everything that you need to use Kafka. However, to make the experience easier later, it’s recommended to pre-configure your source file (.bashrc / .zshrc) so that each time you load the console, all paths are pre-set.

Add these lines to your .bashrc or .zshrc file.

> export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
> 
> export KAFKA_HOME=~/kafka_2.12-3.6.0/

To load the source file again without doing a re-opening of your WSL, just type:

> source ~/.bashrc

# Testing Kafka
You need 4 tabs for this running the following (single lines)

## Start zookeeper
> $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

## Start Kafka
> $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

## Use a Producer to publish events
> $KAFKA_HOME/bin/kafka-console-producer.sh --topic sample-topic --broker-list localhost:9092

## Use a Consumer to receive events
> $KAFKA_HOME/bin/kafka-console-consumer.sh --topic sample-topic --from-beginning --bootstrap-server localhost:9092

- Go back to the producer tab and publish some events.
- Then go back to the consumer tab and you can see that the events are consumed.
- You can also run them side by side to see them in action.
