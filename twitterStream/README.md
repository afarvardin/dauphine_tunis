# Apache Spark Streaming - Get Trending Twitter Hashtags 

## Creating Your Own Credentials for Twitter APIs
- In order to get tweets from Twitter, you need to register on [TwitterApps](https://apps.twitter.com/) by clicking on “Create new app” and then fill the below form click on “Create your Twitter app.”
- Then, go to your newly created app and keep the *bearer_token*.
- Download ```Hadoop.dll``` and ```winutils.exe``` from this [GitHub](https://github.com/cdarlint/winutils) and put them into the ```bin``` folder of Spark.

## Run the Twitter HTTP Client
Open a terminal and run the ```twitter_app.py``` by this command 
``` python twitter_app.py ```

Then open another terminal and run 
```spark-submit stream_app.py```

## OR

To see more intuitive spark code execution, you can run ```stream_app.ipynb``` from a Jupyter notebook


## Stop the application
Using Ctrl+C on the terminal that is running the ```stream_app.py```
Or click ```ssc.stop()``` cell from the ```stream_app.ipynb```.
