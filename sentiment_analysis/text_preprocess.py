import re
import string

from nltk.corpus import stopwords


class text_preprocess:

	def __init__(self):

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

		#stopwords stuff
		self.punctuation = list(string.punctuation)
		self.stop = stopwords.words('english') + self.punctuation + ['rt', 'via']


	def tokenize(self, s):
		return self.tokens_re.findall(s)
 
	def preprocess(self, s, lowercase=False):
		tokens = self.tokenize(s)
		if lowercase:
			tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
		return tokens