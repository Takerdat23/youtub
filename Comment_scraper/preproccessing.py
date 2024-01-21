from vncorenlp import VnCoreNLP
import re
import numpy as np
import json
from Comment_scraper.model import model , tokenizer

vncorenlp = VnCoreNLP("/app/vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

#pre-process


STOPWORDS = './Comment_scraper/vietnamese-stopwords.txt'

labels = ["clean","offensive","hate"] 


with open(STOPWORDS, "r") as ins:
    stopwords = []
    for line in ins:
        dd = line.strip('\n')
        stopwords.append(dd)
    stopwords = set(stopwords)

def filter_stop_words(train_sentences, stop_words):
    new_sent = [word for word in train_sentences.split() if word not in stop_words]
    train_sentences = ' '.join(new_sent)

    return train_sentences

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def preprocess(text, tokenized=True, lowercased=True):
    # text = ViTokenizer.tokenize(text)
    # text = ' '.join(vncorenlp.tokenize(text)[0])
    text = filter_stop_words(text, stopwords)
    text = deEmojify(text)
    text = text.lower() if lowercased else text
    if tokenized:
        pre_text = ""
        sentences = vncorenlp.tokenize(text)
        for sentence in sentences:
            pre_text += " ".join(sentence)
        text = pre_text
    return text


def predict( text): 
     encoded = tokenizer(text, truncation=True, padding=True, max_length=100, return_tensors="pt")
     input_ids = encoded['input_ids']
     attention_mask = encoded['attention_mask']
     outputs = model(input_ids, attention_mask)
     index = np.argmax( outputs.logits.detach().numpy()) 

     print(labels[index])


