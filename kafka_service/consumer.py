from kafka import KafkaConsumer
import json
from Comment_scraper.preproccessing import preprocess, predict


kafka_config = {
        "bootstrap_servers": '172.19.0.4:9092',
        "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
    }

KAFKA_TOPIC_NAME_CONS = "test"



if __name__ == "__main__":
    print("Kafka Consumer Application Started ... ")


    consumer = KafkaConsumer(KAFKA_TOPIC_NAME_CONS,
                             bootstrap_servers=kafka_config["bootstrap_servers"])


    for message in consumer:
    
        message_value = message.value.decode('utf-8')


        message_dict = json.loads(message_value)
       

        preprocessed = preprocess(message_dict['message'], tokenized=True, lowercased=True)

        result = predict(preprocessed)

        print("Received Message:")
        print(preprocessed)   
        print("-----------------------")

        print("-----------------------")