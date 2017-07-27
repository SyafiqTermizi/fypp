import tweepy
from .models import Keyword_search, Keyword_tweets, User_details, User_tweets

class module_one():

	""" module 1: search for specified item, and return it """

	result_search_count=[]
	result_keyword=[]
	result_text=[]
	result_id=[]
	result_in_reply_to_status_id=[]
	result_in_reply_to_screen_name=[]
	result_in_reply_to_user_id=[]	
	result_created_at=[]
	result_keyword_list_zip=[]
	result_geo=[]
	result_retweet_count=[]
	result_user_list_zip=[]
	result_user_id=[]
	result_user_verified=[]
	result_user_name=[]
	result_user_followers_count=[]
	result_user_location=[]
	result_user_status_count=[]
	result_user_description=[]
	result_user_friends_count=[]
	result_user_favourites_count=[]
	result_user_created_at=[]
	result_trend_name=[]
	result_trend_volume=[]
	result_trend_location_name=[]
	result_trend_data_zip=[]

	def __init__(self):
		import tweepy

		consumer_key = '#'
		consumer_secret = '#'

		access_token = '#'
		access_token_secret = '#'

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	def searhByUser(self, searchItem, searchCount, maxId):

		self.tmp_search_count = searchCount

		for tweet in self.api.user_timeline(screen_name=searchItem, count=searchCount, max_id=maxId):
			if tweet.user.id == 475820825:
				self.clearVariables()
				break

			else:
				self.result_user_name.append(tweet.user.name)
				self.result_user_id.append(tweet.user.id)
				self.result_user_verified.append(tweet.user.verified)
				self.result_user_followers_count.append(tweet.user.followers_count)
				self.result_user_friends_count.append(tweet.user.friends_count)
				self.result_user_status_count.append(tweet.user.statuses_count)
				self.result_user_favourites_count.append(tweet.user.favourites_count)
				self.result_user_description.append(tweet.user.description)
				self.result_user_created_at.append(tweet.user.created_at)
				self.result_user_location.append(tweet.user.location)

				#items in result_list_zip
				self.result_text.append(tweet.text)
				self.result_id.append(tweet.id)
				self.result_in_reply_to_status_id.append(tweet.in_reply_to_status_id)
				self.result_in_reply_to_screen_name.append(tweet.in_reply_to_screen_name)
				self.result_in_reply_to_user_id.append(tweet.in_reply_to_user_id)
				self.result_user_id.append(tweet.user.id)
				self.result_user_verified.append(tweet.user.verified)
				self.result_user_name.append(tweet.user.name)
				self.result_created_at.append(tweet.created_at)
				self.result_geo.append(tweet.geo)
				self.result_retweet_count.append(tweet.retweet_count)

		self.createKeywordListZip()

	def searchByKeyword(self, searchItem, searchCount):

		for tweet in self.api.search(q=searchItem, count=searchCount):
			self.result_text.append(tweet.text)
			self.result_id.append(tweet.id)
			self.result_in_reply_to_status_id.append(tweet.in_reply_to_status_id)
			self.result_in_reply_to_screen_name.append(tweet.in_reply_to_screen_name)
			self.result_in_reply_to_user_id.append(tweet.in_reply_to_user_id)
			self.result_user_id.append(tweet.user.id)
			self.result_user_verified.append(tweet.user.verified)
			self.result_user_name.append(tweet.user.name)
			self.result_created_at.append(tweet.created_at)
			self.result_geo.append(tweet.geo)
			self.result_retweet_count.append(tweet.retweet_count)

		self.createKeywordListZip()

	def searchByTweetId(self, searchItem):
		tweet = self.api.get_status(id=searchItem)
		self.result_text.append(tweet.text)
		self.result_id.append(tweet.id)
		self.result_in_reply_to_status_id.append(tweet.in_reply_to_status_id)
		self.result_in_reply_to_screen_name.append(tweet.in_reply_to_screen_name)
		self.result_in_reply_to_user_id.append(tweet.in_reply_to_user_id)
		self.result_user_id.append(tweet.user.id)
		self.result_user_verified.append(tweet.user.verified)
		self.result_user_name.append(tweet.user.name)
		self.result_created_at.append(tweet.created_at)
		self.result_geo.append(tweet.geo)
		self.result_retweet_count.append(tweet.retweet_count)
		self.createKeywordListZip()

	def searchTrendsByWoeid(self, woeid):

		local_trends = self.api.trends_place(id=woeid)

		trends_location = local_trends[0]['locations']

		for x in trends_location:
			self.result_trend_location_name.append(x['name'])

		trends = local_trends[0]['trends']

		for trend in trends:
			if trend['tweet_volume']!=None:
				self.result_trend_name.append(trend['name'])
				self.result_trend_volume.append(trend['tweet_volume'])

		self.createTrendDataZip()

	def trendsDefault(self):

		local_trends = self.api.trends_place(23424901)

		trends_location = local_trends[0]['locations']
		for x in trends_location:
			self.result_trend_location_name.append(x['name'])

		trends = local_trends[0]['trends']
		for trend in trends:
			if trend['tweet_volume']!=None:
				self.result_trend_name.append(trend['name'])
				self.result_trend_volume.append(trend['tweet_volume'])

		self.createTrendDataZip()

	def clearVariables(self):
		self.result_text=[]
		self.result_id=[]
		self.result_in_reply_to_status_id=[]
		self.result_in_reply_to_screen_name=[]
		self.result_in_reply_to_user_id=[]	
		self.result_created_at=[]
		self.result_keyword_list_zip=[]
		self.result_geo=[]
		self.result_retweet_count=[]
		self.result_user_list_zip=[]
		self.result_user_id=[]
		self.result_user_verified=[]
		self.result_user_name=[]
		self.result_user_followers_count=[]
		self.result_user_location=[]
		self.result_user_status_count=[]
		self.result_user_description=[]
		self.result_user_friends_count=[]
		self.result_user_favourites_count=[]
		self.result_user_created_at=[]
		self.result_trend_name=[]
		self.result_trend_volume=[]
		self.result_trend_location_name=[]
		self.result_trend_data_zip=[]
		self.savedTweetsZip=[]
		self.result_keyword=[]
		self.result_search_count=[]

	def createKeywordListZip(self):
		self.result_keyword_list_zip = zip(self.result_retweet_count, self.result_geo, self.result_created_at, self.result_text, self.result_id, self.result_in_reply_to_status_id, self.result_in_reply_to_screen_name, self.result_in_reply_to_user_id, self.result_user_id, self.result_user_verified, self.result_user_name)

	def createTrendDataZip(self):
		self.result_trend_data_zip = zip(self.result_trend_name, self.result_trend_volume)

	def saveKeyword(self, searchItem, searchCount):

		word_search = Keyword_search(keyword=searchItem, search_count=searchCount)
		word_search.save()

		counter = 0
		while (counter < searchCount):

			if word_search.keyword_tweets_set.filter(tweet_id = self.result_id[counter]).exists():
				counter += 1

			else:
				word_search.keyword_tweets_set.create(
					tweet_id = self.result_id[counter],
					user_id = self.result_user_id[counter],
					tweet_text = self.result_text[counter],
					reply_to_tweet_id = self.result_in_reply_to_status_id[counter],
					reply_to_user_id = self.result_in_reply_to_user_id[counter],
					geo_location = self.result_geo[counter],
					user_verified = self.result_user_verified[counter],
					created_at = self.result_created_at[counter],
					user_screen_name = self.result_user_name[counter],
					no_of_rt = self.result_retweet_count[counter])
				counter += 1

	def saveUser(self):
		#save user info to db
		user = User_details(
			user_id = self.result_user_id[0], 
			screen_name = self.result_user_name[0],
			verified = self.result_user_verified[0],
			followers = self.result_user_followers_count[0],
			following = self.result_user_friends_count[0],
			no_of_tweets = self.result_user_status_count[0],
			favourites_count = self.result_user_favourites_count[0],
			description = self.result_user_description[0],
			joined_twitter = self.result_user_created_at[0],
			location = self.result_user_location[0])
		user.save()

		#save user tweets to db
		counter = 0
		while (counter < self.tmp_search_count):

			if user.user_tweets_set.filter(tweet_id = self.result_id[counter]).exists():
				counter += 1

			else:
				user.user_tweets_set.create(
					tweet_id = self.result_id[counter],
					tweet_text = self.result_text[counter],
					reply_to_tweet_id = self.result_in_reply_to_status_id[counter],
					reply_to_user_id = self.result_in_reply_to_user_id[counter],
					geo_location = self.result_geo[counter],
					user_verified = self.result_user_verified[counter],
					created_at = self.result_created_at[counter],
					user_screen_name = self.result_user_name[counter],
					no_of_rt = self.result_retweet_count[counter])
				counter += 1

	def createUserListZip(self):
		self.result_user_list_zip = zip(self.result_user_id, self.result_user_name,	self.result_user_verified, self.result_user_followers_count, self.result_user_friends_count, self.result_user_status_count,	self.result_user_favourites_count, self.result_user_description, self.result_user_created_at, self.result_user_location)

	def displaySavedItem(self):
		self.clearVariables()

		#display saved user
		user_details_list = User_details.objects.all()

		for items in user_details_list:
			self.result_user_id.append(items.user_id)
			self.result_user_name.append(items.screen_name)
			self.result_user_verified.append(items.verified)
			self.result_user_followers_count.append(items.followers)
			self.result_user_friends_count.append(items.following)
			self.result_user_status_count.append(items.no_of_tweets)
			self.result_user_favourites_count.append(items.favourites_count)
			self.result_user_description.append(items.description)
			self.result_user_created_at.append(items.joined_twitter)
			self.result_user_location.append(items.location)

		self.createUserListZip()

		#display saved keyword
		keyword_details_list = Keyword_search.objects.all()

		for items in keyword_details_list:
			self.result_keyword.append(items.keyword)
			self.result_search_count.append(items.keyword_tweets_set.count())

		self.result_keyword_list_zip = zip(self.result_keyword, self.result_search_count)

	def displaySavedTweets(self, userId):
		self.clearVariables()
		user = User_details.objects.get(user_id=userId)
		user_tweets_list = user.user_tweets_set.all()

		for items in user_tweets_list:
			self.result_id.append(items.tweet_id)
			self.result_user_id.append(items.user_id)
			self.result_text.append(items.tweet_text)
			self.result_in_reply_to_status_id.append(items.reply_to_tweet_id)
			self.result_in_reply_to_user_id.append(items.reply_to_user_id)
			self.result_geo.append(items.geo_location)
			self.result_user_verified.append(items.user_verified)
			self.result_created_at.append(items.created_at)
			self.result_user_name.append(items.user_screen_name)
			self.result_retweet_count.append(items.no_of_rt)

		self.savedTweetsZip = zip(self.result_id, self.result_user_id, self.result_text, self.result_in_reply_to_status_id, self.result_in_reply_to_user_id, self.result_geo, self.result_user_verified, self.result_created_at, self.result_user_name,	self.result_retweet_count)

	def displaySavedKeywordTweets(self, key_word):
		self.clearVariables()
		keyword_search = Keyword_search.objects.get(keyword=key_word)
		keyword_tweets_list = keyword_search.keyword_tweets_set.all()
		self.result_keyword.append(keyword_search.pk)

		for items in keyword_tweets_list:
			self.result_id.append(items.tweet_id)
			self.result_user_id.append(items.user_id)
			self.result_text.append(items.tweet_text)
			self.result_in_reply_to_status_id.append(items.reply_to_tweet_id)
			self.result_in_reply_to_user_id.append(items.reply_to_user_id)
			self.result_geo.append(items.geo_location)
			self.result_user_verified.append(items.user_verified)
			self.result_created_at.append(items.created_at)
			self.result_user_name.append(items.user_screen_name)
			self.result_retweet_count.append(items.no_of_rt)

		self.savedTweetsZip = zip(self.result_id, self.result_user_id, self.result_text, self.result_in_reply_to_status_id, self.result_in_reply_to_user_id, self.result_geo, self.result_user_verified, self.result_created_at, self.result_user_name,	self.result_retweet_count)
