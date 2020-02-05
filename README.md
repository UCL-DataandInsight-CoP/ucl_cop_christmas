## UCL Community of Practice: Christmas Songs

### Outline

Source christmas songs and lyrics data from the Spotify and Genius APIs using Python. Create an
interesting visualisation. 

### Data Collection

<img src="tree.png?raw=true"/>

```python
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("kafka_twitter_stream_json", data.encode('utf-8'))
        #print (data)
        return True
    def on_error(self, status):
        print (status)
    def on_limit(self,status):
        print ("Twitter API Rate Limit")
        print("Waiting...")
        time.sleep(15 * 60) # wait 15 minutes and try again
        print("Resuming")
        return True
```
On each data event ‘on_data’ I am using the Kafka-Python library to create a producer and send the
tweet data as a message to the required Kafka topic:

