# Steps to structure a typical Apache Flink streaming application:
1. Set up the execution environment.
1. Read one or more streams from data sources.
1. Apply streaming transformations to implement the application logic.
1. Optionally output the result to one or more data sinks.
1. Execute the program.

## Set Up the Execution Environment
The execution environment determines whether the program is
running on a local machine or on a cluster. In the DataStream API, the execution
environment of an application is represented by the _StreamExecutionEnvironment_.
In our example, we retrieve the execution environment by calling the
static _getExecutionEnvironment()_ method. This method returns a local or remote
environment, depending on the context in which the method is invoked. If the
method is invoked from a submission client with a connection to a remote
cluster, a remote execution environment is returned. Otherwise, it returns a
local environment.
It is also possible to explicitly create local or remote execution environments as
follows:

```
// create a local stream execution environment
val localEnv: StreamExecutionEnvironment.createLocalEnvironment()
// create a remote stream execution environment
val remoteEnv = StreamExecutionEnvironment.createRemoteEnvironment(
"host", // hostname of JobManager
1234, // port of JobManager process
"path/to/jarFile.jar") // JAR file to ship to the JobManager
```

