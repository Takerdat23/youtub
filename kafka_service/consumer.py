from kafka import KafkaConsumer
import json
from Comment_scraper.Spark_Preprocessing import predict_label


kafka_config = {
        "bootstrap_servers": '172.18.0.4:9092',
        "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
    }

KAFKA_TOPIC_NAME_CONS = "test"



if __name__ == "__main__":
    


    consumer = KafkaConsumer(KAFKA_TOPIC_NAME_CONS,
                             bootstrap_servers=kafka_config["bootstrap_servers"])
    
    print("Kafka Consumer Application Started ... ")


    for message in consumer:
    
        message_value = message.value.decode('utf-8')


        message_dict = json.loads(message_value)
    
        result = predict_label(message_dict['message'])

        print("Received Message result:")
        print("Messages:", message_dict['message'])
        print("result: ", result)   
        print("-----------------------")

        print("-----------------------")