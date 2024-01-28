import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from collections import Counter

# Assuming you have a function that returns the number of hate and non-hate comments
# For example: get_comment_counts() -> {'hate': 10, 'non-hate': 90}
# This function would be where you consume and process your Kafka messages

def get_comment_counts():
    # Kafka consumption logic would go here
    # For demonstration, we'll just return static values
    return {'hate': 10, 'non-hate': 90}

# Function to plot a pie chart
def plot_pie_chart(data):
    labels = data.keys()
    sizes = data.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1

# Use the sidebar for input
st.sidebar.title("Kafka Comment Stream Analysis")
if st.sidebar.button("Refresh Data"):
    comment_counts = get_comment_counts()

    # Plot pie chart
    fig = plot_pie_chart(comment_counts)
    st.sidebar.pyplot(fig)

# Function to generate YouTube embed link from normal URL
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