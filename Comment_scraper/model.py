# PhoBERT
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification





model = AutoModelForSequenceClassification.from_pretrained("./Comment_scraper/Model")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base",use_fast=False)

print("Model loaded !!")

# def predict(model, tokenizer, text) : 
#     preprocessed = preprocess(text, tokenized=True, lowercased=True)
#     encoded = tokenizer(preprocessed, truncation=True, padding=True, max_length=100, return_pt = True)
#     print(encoded)

