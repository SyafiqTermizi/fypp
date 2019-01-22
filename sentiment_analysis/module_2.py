import re, string, os

from collections import Counter

from nltk.corpus import stopwords
from nltk import bigrams

from fyp.settings import BASE_DIR
from .naive_bayes_oop import naive_bayes_c
from .models import Keyword_search, Keyword_tweets, User_details, User_tweets

pos_path = os.path.join(BASE_DIR, 'positive-words.txt')
neg_path = os.path.join(BASE_DIR, 'negative-words.txt')


class module_two():

	#variables list
	#retrieved_items
	#tokens_re
	#emoticon_re
	#retrieved_items_tweets
	#stop
	#terms_wo_stopword

	terms_wo_stopword=[]
	most_used_word=[]
	most_used_word_count=[]
	most_used_word_zip=[]
	common_word=[]
	words_bigram=[]
	common_bigrams=[]
	most_used_bigrams=[]
	most_used_bigrams_count=[]
	most_used_bigrams_zip=[]
	result_id = None
	result_user_id = None
	result_text = None
	result_in_reply_to_status_id = None
	result_in_reply_to_user_id = None
	result_geo = None
	result_user_verified = None
	result_created_at = None
	result_user_name = None
	result_retweet_count = None

	def __init__(self):

		#inititalising the classifier
		self.nb = naive_bayes_c()

		#declaring these items as tokens
		emoticons_str = r"""
			(?:
				[:=;] # Eyes
				[oO\-]? # Nose (optional)
				[D\)\]\(\]/\\OpP] # Mouth
			)"""

		regex_str = [
			emoticons_str,
			r'<[^>]+>', # HTML tags
			r'(?:@[\w_]+)', # @-mentions
			r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
			r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

			r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
			r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
			r'(?:[\w_]+)', # other words
			r'(?:\S)' # anything else
		]

		#compiling items above as tokens
		self.tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
		self.emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

		punctuation = list(string.punctuation)
		self.stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', 'THE', '’']

	def tokenize(self, s):
		return self.tokens_re.findall(s)

	def textPreProcess(self, s, lowercase=False):
		tokens = self.tokenize(s)
		if lowercase:
			tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
		return tokens

	def searchDatabase(self, analysis_item):

		try:
			self.retrieved_items = Keyword_search.objects.get(keyword = analysis_item)
			self.retrieved_items_tweets = self.retrieved_items.keyword_tweets_set.all()

		except Keyword_search.DoesNotExist:
			self.retrieved_items = User_details.objects.get(screen_name = analysis_item)
			self.retrieved_items_tweets = self.retrieved_items.user_tweets_set.all()

	def clearVariables(self):
		self.terms_wo_stopword=[]
		self.most_used_word=[]
		self.most_used_word_count=[]
		self.most_used_word_zip=[]
		self.common_word=[]
		self.words_bigram=[]
		self.common_bigrams=[]
		self.most_used_bigrams=[]
		self.most_used_bigrams_count=[]
		self.most_used_bigrams_zip=[]
		self.result_id = None
		self.result_user_id = None
		self.result_text = None
		self.result_in_reply_to_status_id = None
		self.result_in_reply_to_user_id = None
		self.result_geo = None
		self.result_user_verified = None
		self.result_created_at = None
		self.result_user_name = None
		self.result_retweet_count = None
		self.negative = 0
		self.positive = 0
		self.neutral = 0

	def doAnalysis(self):

		#for most common word
		for tweets in self.retrieved_items_tweets:
			for word in self.textPreProcess(tweets.tweet_text.lower()):
				if word not in self.stop:
					self.terms_wo_stopword.append(word)

		self.common_word = Counter(self.terms_wo_stopword).most_common(20)

		#extracting most used word from common_word_test tuple
		outer = 0
		while outer < 20:

			self.most_used_word.append(self.common_word[outer][0])
			self.most_used_word_count.append(self.common_word[outer][1])
			outer += 1

		self.most_used_word_zip = zip(self.most_used_word, self.most_used_word_count)

		#for bigrams
		self.words_bigram = list(bigrams(self.terms_wo_stopword))
		self.common_bigrams = Counter(self.words_bigram).most_common(10)

		#makesure the tuples in list only have string
		new_data=[]
		kira = 0
		while kira<10:
			new_data.append(' '.join(self.common_bigrams[kira][0]))
			kira += 1

		counter = 0
		while counter<10:
			self.most_used_bigrams.append(new_data[counter])
			self.most_used_bigrams_count.append(self.common_bigrams[counter][1])
			counter += 1

		self.most_used_bigrams_zip = zip(self.most_used_bigrams, self.most_used_bigrams_count)

		#find most rt ed tweets (not django style)
		maximum = 0
		tw_id = 0
		for tweets in self.retrieved_items_tweets:
			if tweets.no_of_rt > maximum:
				maximum = tweets.no_of_rt
				tw_id = tweets.tweet_id
		try:
			self.most_rt = Keyword_tweets.objects.get(tweet_id = tw_id)

		except Keyword_tweets.DoesNotExist:
			self.most_rt = User_tweets.objects.get(tweet_id = tw_id)

		self.result_id = (self.most_rt.tweet_id)
		self.result_user_id = (self.most_rt.user_id)
		self.result_text = (self.most_rt.tweet_text)
		self.result_in_reply_to_status_id = (self.most_rt.reply_to_tweet_id)
		self.result_in_reply_to_user_id = (self.most_rt.reply_to_user_id)
		self.result_geo = (self.most_rt.geo_location)
		self.result_user_verified = (self.most_rt.user_verified)
		self.result_created_at = (self.most_rt.created_at)
		self.result_user_name = (self.most_rt.user_screen_name)
		self.result_retweet_count = (self.most_rt.no_of_rt)

		#word distribution
		positive_vocab = [word.rstrip() for word in open(pos_path)]
		negative_vocab = [word.rstrip() for word in open(neg_path)]

		for words in self.terms_wo_stopword:
			if words in positive_vocab:
				self.positive += 1

			elif words in negative_vocab:
				self.negative += 1

			else:
				self.neutral += 1

		self.positive_tweet = 1
		self.negative_tweet = 1

		for tweet in self.retrieved_items_tweets:
			if self.nb.classify_tweet(tweet.tweet_text) == '4':
				self.positive_tweet += 1
			elif self.nb.classify_tweet(tweet.tweet_text) == '0':
				self.negative_tweet += 1