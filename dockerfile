FROM openjdk:11 AS java-builder


WORKDIR /app


# Stage 2: Build Python environment
FROM python:3.8

# Install Java in the Python environment
RUN apt-get update && apt-get install -y wget \
    && wget https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz \
    && tar xvf openjdk-11.0.1_linux-x64_bin.tar.gz -C /usr/local/ \
    && update-alternatives --install /usr/bin/java java /usr/local/jdk-11.0.1/bin/java 100 \
    && update-alternatives --install /usr/bin/javac javac /usr/local/jdk-11.0.1/bin/javac 100 \
    && rm openjdk-11.0.1_linux-x64_bin.tar.gz

# Set the working directory to /app
WORKDIR /app



# Copy your Python application code
COPY . /app/Youtube-kafka-hatespeech


# Create directory structure for VnCoreNLP
RUN mkdir -p vncorenlp/models/wordsegmenter

# Download the necessary files
RUN wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.1.1.jar \
    && wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab \
    && wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr

# Move the downloaded files to the appropriate locations
RUN mv VnCoreNLP-1.1.1.jar vncorenlp/ \
    && mv vi-vocab vncorenlp/models/wordsegmenter/ \
    && mv wordsegmenter.rdr vncorenlp/models/wordsegmenter/

RUN pip install -r ./Youtube-kafka-hatespeech/requirements.txt
CMD ["tail", "-f", "/dev/null"]


