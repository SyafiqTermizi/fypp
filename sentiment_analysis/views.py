from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from .forms import SearchForm, TrendForm
from .module_1 import module_one
from .module_2 import module_two
from .models import Keyword_search, Keyword_tweets, User_details, User_tweets
from .fusioncharts import FusionCharts
import math

a = module_two()

def index(request):
	template = loader.get_template('sentiment_analysis/index.html')
	return HttpResponse(template.render())

def get_search_form(request):

	if request.method == 'GET':
		form = SearchForm(request.GET)

		tw = module_one()

		#if search by screen name
		if int(form.data['choice']) == 1:
			searchCount = int(form.data['search_count'])
			searchItem = form.data['search_item']

			#if user specify the max id
			if int(form.data['max_id'])!=0:
				maxId = int(form.data['max_id'])

			#if user do not specify max id
			elif int(form.data['max_id'])==0:
				maxId = None

			tw.clearVariables()
			tw.searhByUser(searchItem, searchCount, maxId)

			if not tw.result_text:
				context = {
					'searchItem' : searchItem,
				}
				return render(request, 'sentiment_analysis/result item not found.html', context)

			else:

				tw.saveUser()
				context = {
					'searchItem' : '@'+searchItem,
					'result_all' : tw.result_keyword_list_zip,
					'userName' : tw.result_user_name[0],
					'userId' : tw.result_user_id[0],
					'userVerified': tw.result_user_verified[0],
					'followersCount' : tw.result_user_followers_count[0],
					'userLocation' : tw.result_user_location[0],
					'statusCount' : tw.result_user_status_count[0],
					'userDescription' : tw.result_user_description[0],
					'followingCount' : tw.result_user_friends_count[0],
					'favouritesCount' : tw.result_user_favourites_count[0],
					'joinedTwitter' : tw.result_user_created_at[0],
				}
				return render(request, 'sentiment_analysis/result user.html', context)

		if int(form.data['choice']) == 2:

			searchCount = int(form.data['search_count'])
			searchItem = form.data['search_item']

			tw.clearVariables()
			tw.searchByKeyword(searchItem, searchCount)
			tw.saveKeyword(searchItem, searchCount)

			context = {
				'searchItem' : searchItem,
				'result_all' : tw.result_keyword_list_zip,
			}
			return render(request, 'sentiment_analysis/result keyword.html', context)

		if int(form.data['choice']) == 3:

			searchItem = form.data['search_item']

			tw.clearVariables()
			tw.searchByTweetId(searchItem)
			result_all = tw.result_keyword_list_zip

			context = {
				'searchItem' : searchItem,
				'result_all' : result_all,
			}
			return render(request, 'sentiment_analysis/result keyword.html', context)

def trends(request):

	tr = module_one()
	tr.clearVariables()
	tr.trendsDefault()

	context = {
		'trendLocation' : tr.result_trend_location_name[0],
		'result_all' : tr.result_trend_data_zip,
	}
	return render(request, 'sentiment_analysis/trends search.html', context)
	
def trends_search(request):

	import tweepy
	if request.method == 'GET':
		form = TrendForm(request.GET)

		if form.is_valid():
			searchItem = int(form.cleaned_data['search_trends'])
			tr = module_one()
			tr.clearVariables()

			tr.searchTrendsByWoeid(searchItem)

			if not tr.result_trend_data_zip:

				context = {
					'searchItem' : searchItem,
				}
				return render(request, 'sentiment_analysis/result item not found.html', context)

			else:

				context = {
					'trendLocation' : tr.result_trend_location_name[0],
					'result_all' : tr.result_trend_data_zip,
				}
				return render(request, 'sentiment_analysis/trends search.html', context)

	else:
		form = SearchForm()
	
	return render(request, 'sentiment_analysis/trends search.html', {'form': form})

def saved_items(request):
	r = module_one()
	r.displaySavedItem()
	
	context = {
		'result_user_details' : r.result_user_list_zip,
		'result_keywords' : r.result_keyword_list_zip
	}

	return render(request, 'sentiment_analysis/saved items.html', context)

def saved_tweets(request, userId):
	t = module_one()
	t.displaySavedTweets(userId)

	context = {
		'result_for' : t.result_user_name[0],
		'result_all' : t.savedTweetsZip
	}

	return render(request, 'sentiment_analysis/saved tweets.html', context)

def saved_keyword_tweets(request, keyword):

	k = module_one()
	k.displaySavedKeywordTweets(keyword)	

	context = {
		'result_for' : k.result_keyword[0],
		'result_all' : k.savedTweetsZip
	}

	return render(request, 'sentiment_analysis/saved tweets.html', context)

def analyse_tweets(request, analysis_item):
	
	a.clearVariables()
	a.searchDatabase(analysis_item)
	a.doAnalysis()

	print('pos: %d' % a.positive_tweet)
	print('neg: %d' % a.negative_tweet)

	#for graph 1, 20 most used word
	graph_one = {}
	graph_one['chart'] = { 
		"caption": "20 Most used word",
			"xAxisName": "Word",
			"yAxisName": "Count",
			"theme": "ocean"
		}

	graph_one['data'] = []
	for term, number in a.most_used_word_zip:
		data = {}
		data['label'] = term
		data['value'] = number
		graph_one['data'].append(data)

	graph_one_render = FusionCharts("column2D", "graph_one" , "600", "350", "chart_one", "json", graph_one).render()

	#for graph 2, 10 most used bigrams
	graph_two = {}
	graph_two['chart'] = { 
		"caption": "10 Most used bigrams",
			"xAxisName": "Bigrams",
			"yAxisName": "Count",
			"theme": "ocean"
		}

	graph_two['data'] = []
	for bigrams, count in a.most_used_bigrams_zip:
		data = {}
		data['label'] = bigrams
		data['value'] = count
		graph_two['data'].append(data)

	graph_two_render = FusionCharts("column2D", "graph_two" , "600", "350", "chart_two", "json", graph_two).render()

	#for gauge one, word distribution
	positive_percent = math.floor((a.positive/(a.negative + a.positive))*100)
	pointer_location = positive_percent

	gauge_one = {}
	gauge_one['chart'] = {
		"caption": "Word distribution for The tweets",
		"subcaption": "-",
		"lowerLimit": "0",
		"upperLimit": 100,
		"theme": "ocean"
	}

	gauge_one['colorRange'] = {
		"color": [{
			"minValue": "0",
			"maxValue": "50",
			"code": "#e74c3c"
			},{
			"minValue": "50",
			"maxValue": "100",
			"code": "#2ecc71"
			}]
	}

	gauge_one['dials'] = {
			"dial": [{
			"value": (pointer_location)
		}]
	}

	gauge_one['annotations'] = {
        "origw": "650",
        "origh": "300",
        "autoscale": "1",
        "showBelow": "0",
        "groups": [
            {
                "id": "arcs",
                "items": [
                    {
                        "id": "positive-bg",
                        "type": "rectangle",
                        "x": "$chartCenterX+2",
                        "y": "$chartEndY - 45",
                        "tox": "$chartCenterX + 130",
                        "toy": "$chartEndY - 25",
                        "fillcolor": "#2ecc71"
                    },
                    {
                        "id": "positive-text",
                        "type": "Text",
                        "color": "#ffffff",
                        "label": "Positive",
                        "fontSize": "12",
                        "align": "left",
                        "x": "$chartCenterX + 7",
                        "y": "$chartEndY - 35"
                    },
                    {
                        "id": "negative-bg",
                        "type": "rectangle",
                        "x": "$chartCenterX-2",
                        "y": "$chartEndY - 45",
                        "tox": "$chartCenterX - 103",
                        "toy": "$chartEndY - 25",
                        "fillcolor": "#e74c3c"
                    },
                    {
                        "id": "negative-text",
                        "type": "Text",
                        "color": "#ffffff",
                        "label": "Negative",
                        "fontSize": "12",
                        "align": "right",
                        "x": "$chartCenterX - 7",
                        "y": "$chartEndY - 35"
                    }
                ]
            }
        ]
	}

	gauge_one_render = FusionCharts("angulargauge", "gauge_one" , "450", "300", "meter_one", "json", gauge_one).render()

	#gauge 3 for sentiment analysis
	tweets_sentiment_score = math.floor((a.positive_tweet / (a.positive_tweet + a.negative_tweet)) * 100)

	gauge_two = {}
	gauge_two['chart'] = {
		"caption": "Overall tweet sentiment score",
		"subcaption": "-",
		"lowerLimit": "0",
		"upperLimit": 100,
		"theme": "ocean"
	}

	gauge_two['colorRange'] = {
		"color": [{
			"minValue": "0",
			"maxValue": "50",
			"code": "#e74c3c"
			},{
			"minValue": "50",
			"maxValue": "100",
			"code": "#2ecc71"
			}]
	}

	gauge_two['dials'] = {
			"dial": [{
			"value": (tweets_sentiment_score)
		}]
	}

	gauge_two['annotations'] = {
        "origw": "650",
        "origh": "300",
        "autoscale": "1",
        "showBelow": "0",
        "groups": [
            {
                "id": "arcs",
                "items": [
                    {
                        "id": "positive-bg",
                        "type": "rectangle",
                        "x": "$chartCenterX+2",
                        "y": "$chartEndY - 45",
                        "tox": "$chartCenterX + 130",
                        "toy": "$chartEndY - 25",
                        "fillcolor": "#2ecc71"
                    },
                    {
                        "id": "positive-text",
                        "type": "Text",
                        "color": "#ffffff",
                        "label": "Positive",
                        "fontSize": "12",
                        "align": "left",
                        "x": "$chartCenterX + 7",
                        "y": "$chartEndY - 35"
                    },
                    {
                        "id": "negative-bg",
                        "type": "rectangle",
                        "x": "$chartCenterX-2",
                        "y": "$chartEndY - 45",
                        "tox": "$chartCenterX - 103",
                        "toy": "$chartEndY - 25",
                        "fillcolor": "#e74c3c"
                    },
                    {
                        "id": "negative-text",
                        "type": "Text",
                        "color": "#ffffff",
                        "label": "Negative",
                        "fontSize": "12",
                        "align": "right",
                        "x": "$chartCenterX - 7",
                        "y": "$chartEndY - 35"
                    }
                ]
            }
        ]
	}

	gauge_two_render = FusionCharts("angulargauge", "gauge_two" , "450", "300", "meter_two", "json", gauge_two).render()

	context = {
		'output_2': graph_two_render,
		'output': graph_one_render,
		'analysisItem': analysis_item,
		'result_id': a.result_id,
		'user_id': a.result_user_id,
		'tweet_text': a.result_text,
		'user_verified': a.result_user_verified,
		'created_at': a.result_created_at,
		'user_name': a.result_user_name,
		'rt_count': a.result_retweet_count,
		'output_3' : gauge_one_render,
		'output_4' : gauge_two_render,
	}

	return render(request, 'sentiment_analysis/analyse tweets.html', context)