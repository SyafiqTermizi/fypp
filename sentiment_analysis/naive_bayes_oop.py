import os
from datetime import datetime, date, time

import nltk
from tqdm import tqdm

from fyp.settings import BASE_DIR
from .text_preprocess import text_preprocess

train_dataset_text = os.path.join(BASE_DIR, 'train_dataset_text.txt')
train_dataset_sentiment = os.path.join(BASE_DIR, 'train_dataset_sentiment.txt')


class naive_bayes_c():

	def __init__(self):

		masa = datetime.now()
		print('Initialising Naive Bayes classifier at: ')
		print(masa)
		#read the sentiment text and value
		print('\nReading source text file')
		train_text = [word.rstrip() for word in open(train_dataset_text)]
		train_sentiment = [word.rstrip() for word in open(train_dataset_sentiment)]

		pos_index=[]
		neg_index=[]

		counter = 0
		while counter < len(train_sentiment):
			if train_sentiment[counter] == '4':
				pos_index.append(counter)
			elif train_sentiment[counter] == '0':
				neg_index.append(counter)
			counter += 1

		pos_text_full=[]
		pos_sentiment=[]

		print('\nSorting positive tweets')
		for item in tqdm(pos_index):
			pos_text_full.append(train_text[int(item)])
			pos_sentiment.append(train_sentiment[int(item)])

		neg_text_full=[]
		neg_sentiment=[]

		print('\nSorting negative tweets')
		for item in tqdm(neg_index):
			neg_text_full.append(train_text[int(item)])
			neg_sentiment.append(train_sentiment[int(item)])

		#change value to change training count
		pos_text=[]
		neg_text=[]
		counter = 0
		while counter < int(os.environ.get('TRAINING_DATA_COUNT')):
			pos_text.append(pos_text_full[counter])
			neg_text.append(neg_text_full[counter])
			counter += 1

		pos_tweets = zip(pos_text, pos_sentiment)
		neg_tweets = zip(neg_text, neg_sentiment)
		tweets = []

		#text preprocessing
		self.pr = text_preprocess()

		print('\nPreprocessing texts')
		for (tweet, sentiments) in tqdm(pos_tweets):
			words_filtered = [words.lower() for words in self.pr.preprocess(tweet) if words not in self.pr.stop]
			tweets.append((words_filtered, sentiments))

		for (tweet, sentiments) in tqdm(neg_tweets):
			words_filtered = [words.lower() for words in self.pr.preprocess(tweet) if words not in self.pr.stop]
			tweets.append((words_filtered, sentiments))

		print('\nDefining word features')
		self.word_features = self.get_word_features(self.get_word_in_tweets(tweets))

		print('\nBuilding training set')
		training_set = nltk.classify.util.apply_features(self.extract_features, tweets)
		self.classifier = nltk.NaiveBayesClassifier.train(training_set)

	#get word list of tweets
	def get_word_in_tweets(self, tweets):
		all_words=[]
		print('\nGetting list of words from tweets')
		for (words, sentiments) in tqdm(tweets):
			all_words.extend(words)
		return all_words

	def get_word_features(self, wordlist):
		print('\nAssigning word features')
		wordlist = nltk.FreqDist(wordlist)
		self.word_features = wordlist.keys()
		return self.word_features

	def extract_features(self, document):
		document_words = set(document)
		features = {}

		for word in self.word_features:
			features['contains(%s)' % word] = (word in document_words)
		return features

	#this function accept stuff to classify from other class 
	def classify_tweet(self, tweet):
		return self.classifier.classify(self.extract_features(self.pr.preprocess(tweet)))
