import re
import csv
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from tweepy import TweepError

negative_words = set()
with open("../../resources/Hu and Liu (2004)/negative-words.txt") as f:
    for line in f.readlines():
        if line[0] != ';':
            negative_words.add(line.strip())
            
positive_words = set()
with open("../../resources/Hu and Liu (2004)/positive-words.txt") as f:
    for line in f.readlines():
        if line[0] != ';':
            positive_words.add(line.strip())
            
            
def calculate_polarity_score(text):
    polarity_score = 0
    for word in text.split():
        word = word.lower()
        if word in negative_words:
            polarity_score -= 1
        elif word in positive_words:
            polarity_score += 1
        # print word, polarity_score
    # print text.split(), len(negative_words), len(positive_words), polarity_score
    return polarity_score