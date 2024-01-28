import sys
sys.path.append('./youtube-kafka/Comment_scraper')
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from collections import Counter
from kafka import KafkaConsumer
import json
from Comment_scraper.Spark_Preprocessing import predict_label




def generate_embed_link(url):
    if 'watch?v=' in url:
        embed_url = url.replace('watch?v=', 'embed/')
        return f"{embed_url}?autoplay=1&mute=1"
    return url


user_input = st.text_input("Enter YouTube Live Stream Link", "https://www.youtube.com/watch?v=XXXX")

# Convert normal YouTube URL to embed URL
embed_url = generate_embed_link(user_input)
padding = 10 

# Embed YouTube live stream
components.html(
    f"""
    <div style="padding: {padding}px; background-color: #000;"> <!-- You can change the background color as needed -->
        <iframe width="100%" height="315" 
                src="{embed_url}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen></iframe>
    </div>
    """,
    height=340,  # Adjusted height to account for padding
)

data_dict = {"clean": 0, "offensive": 0, "hate": 0}


def plot_pie_chart(data, placeholder):
    labels = data.keys()
    sizes = data.values()
    total = sum(sizes)  # Calculate the total count

    # If there are no data, avoid division by zero
    if total == 0:
        percentages = [0 for _ in sizes]
    else:
        percentages = [(size / total) * 100 for size in sizes]  # Calculate percentages

    fig, ax = plt.subplots()
    ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    placeholder.pyplot(fig)

# Kafka consumer setup
kafka_config = {
    "bootstrap_servers": '172.18.0.4:9092',
    "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
}
KAFKA_TOPIC_NAME_CONS = "test"

if __name__ == "__main__":
    st.sidebar.title("Kafka Comment Stream Analysis")
    pie_chart_placeholder = st.sidebar.empty()  # Placeholder for the pie chart

    consumer = KafkaConsumer(KAFKA_TOPIC_NAME_CONS,
                             bootstrap_servers=kafka_config["bootstrap_servers"])

    

    for message in consumer:
        message_value = message.value.decode('utf-8')
        message_dict = json.loads(message_value)
        result = predict_label(message_dict['message'])
        data_dict[result] += 1

        plot_pie_chart(data_dict, pie_chart_placeholder)

        
