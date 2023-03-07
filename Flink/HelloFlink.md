# Steps to structure a typical Apache Flink streaming application:
1. Set up the execution environment.
1. Read one or more streams from data sources.
1. Apply streaming transformations to implement the application logic.
1. Optionally output the result to one or more data sinks.
1. Execute the program.

The program below converts the temperatures from Fahrenheit to
Celsius and computes the average temperature every 5 seconds for each sensor.
We explain the "Steps to structure a typical Apache Flink streaming application"
helping this application.

```scala
// Scala object that defines the DataStream program in the main() method.
object AverageSensorReadings {
    // main() defines and executes the DataStream program
    def main(args: Array[String]) {
        // set up the streaming execution environment
        val env = StreamExecutionEnvironment.getExecutionEnvironment
        // use event time for the application
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
        // create a DataStream[SensorReading] from a stream source
        val sensorData: DataStream[SensorReading] = env
        // ingest sensor readings with a SensorSource SourceFunction
        .addSource(new SensorSource)
        // assign timestamps and watermarks (required for event time)
        .assignTimestampsAndWatermarks(new SensorTimeAssigner)
        val avgTemp: DataStream[SensorReading] = sensorData
        // convert Fahrenheit to Celsius with an inline lambda function
        .map( r => {
        val celsius = (r.temperature - 32) * (5.0 / 9.0)
        SensorReading(r.id, r.timestamp, celsius)
        } )
        // organize readings by sensor id
        .keyBy(_.id)
        // group readings in 5 second tumbling windows
        .timeWindow(Time.seconds(5))
        // compute average temperature using a user-defined function
        .apply(new TemperatureAverager)
        // print result stream to standard out
        avgTemp.print()
        // execute application
        env.execute("Compute average sensor temperature")
    }
}
```


## Set Up the Execution Environment
The execution environment determines whether the program is
running on a local machine or on a cluster. In the DataStream API, the execution
environment of an application is represented by the _StreamExecutionEnvironment_.
In our example, we retrieve the execution environment by calling the
static _getExecutionEnvironment()_ `method'. This method returns a local or remote
environment, depending on the context in which the method is invoked. If the
method is invoked from a submission client with a connection to a remote
cluster, a remote execution environment is returned. Otherwise, it returns a
local environment.
It is also possible to explicitly create local or remote execution environments as
follows:

```scala
// create a local stream execution environment
val localEnv: StreamExecutionEnvironment.createLocalEnvironment()
// create a remote stream execution environment
val remoteEnv = StreamExecutionEnvironment.createRemoteEnvironment(
"host", // hostname of JobManager
1234, // port of JobManager process
"path/to/jarFile.jar") // JAR file to ship to the JobManager
```

Next, we use _env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)_ to
instruct our program to interpret time semantics using event time. The
execution environment offers more configuration options, such as setting the
program parallelism and enabling fault tolerance.

# Read an Input Stream
Once the execution environment has been configured, it is time to do some
actual work and start processing streams.
The StreamExecutionEnvironment provides methods to create stream sources that
ingest data streams into the application. Data streams can be ingested from
sources such as message queues or files, or also be generated on the fly.

In our example, we use the below code to connect to the source of the sensor measurements and create an
initial _DataStream_ of type _SensorReading_.

```scala
val sensorData: DataStream[SensorReading] =
    env.addSource(new SensorSource)
```

## Apply Transformations
Once we have a DataStream, we can apply a transformation on it. There are
different types of transformations. Some transformations can produce a
new DataStream, possibly of a different type, while other transformations do not
modify the records of the DataStream but reorganize it by partitioning or
grouping. The logic of an application is defined by chaining transformations.

In our example, we first apply a map() transformation that converts the
temperature of each sensor reading to Celsius. Then, we use
the keyBy() transformation to partition the sensor readings by their sensor ID.
Next, we define a timeWindow() transformation, which groups the sensor
readings of each sensor ID partition into tumbling windows of 5 seconds:

```scala
val avgTemp: DataStream[SensorReading] = sensorData
    .map( r => {
        val celsius = (r.temperature - 32) * (5.0 / 9.0)
        SensorReading(r.id, r.timestamp, celsius)
    } )
    .keyBy(_.id)
    .timeWindow(Time.seconds(5))
    .apply(new TemperatureAverager)
```

## Output the Result
Streaming applications usually emit their results to some external system, such
as Apache Kafka, a filesystem, or a database. Flink provides a well-maintained
collection of stream sinks that can be used to write data to different systems.
There are also applications that do not emit results but keep them internally to serve them via
Flink’s queryable state feature.

In our example, the result is a _DataStream[SensorReading]_ record. Every record
contains an average temperature of a sensor over a period of 5 seconds. The
result stream is written to the standard output by calling print():
```scala
avgTemp.print()
```

## Execute
When the application has been completely defined, it can be executed by
calling _StreamExecutionEnvironment.execute()_. This is the last call in our example:

```scala
env.execute("Compute average sensor temperature")
```

Flink programs are executed lazily. That is, the API calls that create stream
sources and transformations do not immediately trigger any data processing.
Instead, the API calls construct an execution plan in the execution environment,
which consists of the stream sources created from the environment and all
transformations that were transitively applied to these sources. Only
when _execute()_ is called does the system trigger the execution of the program.