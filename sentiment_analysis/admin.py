from django.contrib import admin

from .models import Keyword_search, User_details, User_tweets, Keyword_tweets


class Keyword_tweetsInline(admin.StackedInline):
	model = Keyword_tweets


class Keyword_searchAdmin(admin.ModelAdmin):
	inlines = [Keyword_tweetsInline]


class User_tweetsInline(admin.StackedInline):
	model = User_tweets


class User_detailsAdmin(admin.ModelAdmin):
	inlines = [User_tweetsInline]


# Register your models here
admin.site.register(Keyword_search, Keyword_searchAdmin)
admin.site.register(User_details, User_detailsAdmin)
