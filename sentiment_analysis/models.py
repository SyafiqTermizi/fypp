from django.db import models

class Keyword_search(models.Model):
	keyword = models.CharField(primary_key=True, max_length = 200)
	search_count = models.IntegerField()
	def __str__(self):
		return self.keyword

class Keyword_tweets(models.Model):
	tweet_id = models.BigIntegerField(primary_key=True)
	user_id = models.BigIntegerField()
	keyword = models.ForeignKey('Keyword_search', on_delete=models.CASCADE)
	tweet_text = models.CharField(max_length=140)
	reply_to_tweet_id = models.BigIntegerField(null=True)
	reply_to_user_id = models.BigIntegerField(null=True)
	geo_location = models.CharField(max_length=200, null=True)
	user_verified = models.BooleanField()
	created_at = models.DateTimeField()
	user_screen_name = models.CharField(max_length=200)
	no_of_rt = models.IntegerField(null=True)

class User_details(models.Model):
	user_id = models.BigIntegerField(primary_key=True)
	screen_name = models.CharField(max_length=200)
	verified = models.BooleanField()
	followers = models.IntegerField()
	following = models.IntegerField()
	no_of_tweets = models.IntegerField()
	favourites_count = models.IntegerField()
	description = models.CharField(max_length=200, null=True)
	joined_twitter = models.DateTimeField()
	location = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.screen_name

class User_tweets(models.Model):
	tweet_id = models.BigIntegerField(primary_key=True)
	user_id = models.ForeignKey('User_details', on_delete=models.CASCADE)
	tweet_text = models.CharField(max_length=140)
	reply_to_tweet_id = models.BigIntegerField(null=True)
	reply_to_user_id = models.BigIntegerField(null=True)
	geo_location = models.CharField(max_length=200, null=True)
	user_verified = models.BooleanField()
	created_at = models.DateTimeField()
	user_screen_name = models.CharField(max_length=200)
	no_of_rt = models.IntegerField(null=True)