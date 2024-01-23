import findspark
findspark.init()
#Tạo session  để tương tác với spark
from pyspark.sql.functions import month,to_date,col
from pyspark.sql import functions as f
from pyspark.sql.types import *
import re
from pyspark.sql.functions import udf
from pyspark.sql.functions import split
from pyvi import ViTokenizer
from pyspark.sql.functions import lower
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pyspark.ml import Transformer
from pyspark.sql.types import FloatType

from model import model , tokenizer



spark = SparkSession.builder.appName("PySparkSQL").getOrCreate()

from pyspark.sql.types import *
schema = StructType([
  StructField("free_text", StringType(), True),
  StructField("label_id", StringType(), True)
])



def readCSV(path):
  df = spark.read.option("header", "true").option("quote", "\"").option("escape", "\"").csv(path)
  df = df.filter(col("label_id").cast("double").isNotNull())
  return df


STOPWORDS_PATH ="./vietnamese-stopwords.txt"

with open(STOPWORDS_PATH, "r", encoding="utf-8") as file:
    stopwords = set(line.strip() for line in file)


# Define UDF for filtering stop words
@udf(StringType())
def filter_stop_words_udf(train_sentences):
    new_sent = [word for word in train_sentences.split() if word not in stopwords]
    return ' '.join(new_sent)
fill_stop_words=udf(filter_stop_words_udf)



# Define UDF for de-emojifying
@udf(StringType())
def de_emojify_udf(text):
    regrex_pattern = re.compile(pattern="[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)
de_emojify=udf(de_emojify_udf)




@udf(StringType())
def preprocess_udf(text):
    text = ViTokenizer.tokenize(text)
    #text = ' '.join(vncorenlp.tokenize(text)[0])
    # pre_text = ""
    # sentences = vncorenlp.tokenize(text)
    # for sentence in sentences:
    #     pre_text += " ".join(sentence)
    # text = pre_text
    return text
preprocess=udf(preprocess_udf)


def predict_udf(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    return float(logits.argmax(axis=1))

predict_udf_spark = udf(predict_udf, FloatType())





# Define the schema for the DataFrame for training
schema = StructType([
    StructField("input_ids", StringType(), True),
    StructField("attention_mask", StringType(), True),
    StructField("label", StringType(), True)
])


schema_prediction= StructType([
    StructField("input_ids", StringType(), True),
    StructField("attention_mask", StringType(), True)
])


# Define a PyTorchTransformer
class PyTorchTransformer(Transformer):
    def _transform(self, dataset):
        # Apply tokenization and model inference
        def predict_udf(text):
            inputs = tokenizer(text, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
            return float(logits.argmax(axis=1))

        # Register the UDF
        predict_udf_spark = udf(predict_udf, FloatType())

        # Apply the UDF to create a new column with predictions
        return dataset.withColumn("prediction", predict_udf_spark(col("input_ids")))
    

from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[
    PyTorchTransformer()
])




data = [("Nó học cách của thằng anh nó đó, hèn, khốn nạn",)]
df = spark.createDataFrame(data, ["text"])
df_processed = df.withColumn("processed_text",lower(col("text")))
df_processed = df.withColumn("processed_text",filter_stop_words_udf("text"))
df_processed = df.withColumn("processed_text", de_emojify_udf("text"))
df_processed = df.withColumn("processed_text", preprocess_udf("text"))

df_processed=tokenizer(df_processed.toPandas()["processed_text"].tolist(), truncation=True, padding=True, max_length=100)
df_processed=list(zip(df_processed['input_ids'], df_processed['attention_mask']))
df = spark.createDataFrame(df_processed, schema=schema_prediction)




result=df.withColumn("prediction", predict_udf_spark(col("input_ids")))


res=result.toPandas()
if res["prediction"][0]==0:
    print("clean")
elif res["prediction"][0]==1:
    print("offensive")
else:
    print("hate")

# Show the predictions








