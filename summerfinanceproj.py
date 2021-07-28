#! usr/bin/env python3
import praw
import pandas as pd
import csv
import string
import nltk
import numpy as np
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

reddit = praw.Reddit(client_id='O67toc3E7bFYnIxnq3qPUA',
                     client_secret='lhCYhrYRHS7fjERsyuPiTkcu4IlOmA',
                     user_agent='News Scraper',
                     username='javonito',
                     password='Redboy123')

sub_finance = reddit.subreddit('finance')
sub_wsb = reddit.subreddit('wallstreetbets')
sub_investing = reddit.subreddit('investing')

subreddits = [sub_finance, sub_wsb, sub_investing]

titles = []
body_texts = []
stock_name = []
tokens = []
with open('bats_symbols.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for column in reader:
        stock_name.append(column['Name'])
with open('nasdaq-listed_csv.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for column in reader:
        stock_name.append(column['Symbol'])

for sub in subreddits:
    hot_posts = sub.hot()
    for post in hot_posts:
        titles.append(post.title)
        body_texts.append(post.selftext)

tokens = [nltk.word_tokenize(body) for body in body_texts]

for title in titles:
    tokens.append(nltk.word_tokenize(title))

updated_tokens = []
for t_group in tokens:
    for token in t_group:
        updated_tokens.append(token)

filtered_reddit = []
for token in updated_tokens:
    filtered_reddit.append(re.findall(r"(\b(?:[A-Z]+[a-z]?[A-Z]*|[A-Z]*[a-z]?[A-Z]+)\b(?:\s+(?:[A-Z]+[a-z]?[A-Z]*|["
                                      r"A-Z]*["r"a-z]?[A-Z]+)\b)*)", token))

filtered_reddit = list(filter(None, filtered_reddit))
unique_filter = []
for x in filtered_reddit:
    for entry in x:
        if entry not in unique_filter:
            if len(entry) > 2:
                unique_filter.append(entry)
print(unique_filter)
