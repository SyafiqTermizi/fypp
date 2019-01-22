from django import forms

CHOICES = (
	('1' , 'Search by User'),
	('2' , 'Search by Keyword'),
	('3' , 'Search by Tweet ID')
	)


class SearchForm(forms.Form):
	search_item = forms.CharField(label='search_item', max_length=100)
	max_id = forms.CharField(label='max_id', max_length=100)
	search_count = forms.CharField(label='search_count', max_length=100)
	choice = forms.ChoiceField(choices=CHOICES)


class TrendForm(forms.Form):
	search_trends = forms.CharField(label='search_trends', max_length=100)
