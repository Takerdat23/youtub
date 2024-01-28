
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable

os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from pyspark.sql.types import *
import findspark
import re
import torch
from pyvi import ViTokenizer
from Comment_scraper.model import model , tokenizer
findspark.init()
#Tạo session  để tương tác với spark
spark = SparkSession.builder.master("local[*]").appName("PySparkSQL").getOrCreate()

STOPWORDS_PATH ="./Comment_scraper/vietnamese-stopwords.txt"
with open(STOPWORDS_PATH, "r", encoding="utf-8") as file:
    stopwords = set(line.strip() for line in file)
# Define UDF for filtering stop words
@udf(StringType())
def filter_stop_words_udf(train_sentences):
    new_sent = [word for word in train_sentences.split() if word not in stopwords]
    return ' '.join(new_sent)
fill_stop_words=udf(filter_stop_words_udf)

@udf(StringType())
def de_emojify_udf(text):
    regrex_pattern = re.compile(pattern="[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)
de_emojify=udf(de_emojify_udf)
@udf(StringType())
def preprocess_udf(text):
    text = ViTokenizer.tokenize(text)
    return text
preprocess=udf(preprocess_udf)






schema_prediction= StructType([
    StructField("input_ids", StringType(), True),
    StructField("attention_mask", StringType(), True)
])


model_spark= spark.sparkContext.broadcast(model)




def predict_udf_spark(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model_spark.value(**inputs)
    logits = outputs.logits
    return float(logits.argmax(axis=1))




# result=df.withColumn("prediction", predict_udf_spark(col("input_ids")))

# result.show()
    
def predict_label(text): 
    data = [(text,)]
    df = spark.createDataFrame(data, ["text"])
    df_processed = df.withColumn("processed_text",filter_stop_words_udf("text"))
    df_processed = df.withColumn("processed_text", de_emojify_udf("text"))
    df_processed = df.withColumn("processed_text", preprocess_udf("text"))

    df=df_processed
    text_tokenize=df.select("processed_text").tail(1)[0][0]

    res=predict_udf_spark(text_tokenize)

    if res==0:  
        return "clean"
    elif res==1:    
        return "offensive"
    else: 
        return "hate"



