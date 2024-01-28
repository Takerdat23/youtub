import pandas as pd
from kafka import KafkaProducer
from datetime import datetime
import time
import random
import numpy as np
import json
import pytchat


# pip install kafka-python
YOUTUBE_ID = "N7Ajxe66wcw" #change the id to your youtube id
KAFKA_TOPIC_NAME_CONS = "test" # change the topics name as you like
KAFKA_BOOTSTRAP_SERVERS_CONS = '172.18.0.4:9092' #change the ip address to your docker container ip 
kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS)
if __name__ == "__main__":

    print("Kafka Producer Application Started")
    chat = pytchat.create(video_id = YOUTUBE_ID)
  
            
    while chat.is_alive(): 
        for c in chat.get().sync_items(): 
          
            data_dict = {}
            data_dict['message'] = c.message
            # print(data_dict)
            json_message = json.dumps(data_dict)
            encoded_message = json_message.encode('utf-8')

            print("Message: ", json.loads(encoded_message))

            kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, encoded_message)
            time.sleep(1)
            kafka_producer_obj.flush()
    print("Kafka Producer Application Completed. ")






