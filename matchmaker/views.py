from django.shortcuts import render
from .models import Seller, Country
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import SellerForm, MatchForm

def home(request):
    sellers_in_egypt = Seller.objects.filter(country_name='Egypt')
    return render(request, 'home.html', {'sellers_in_egypt': sellers_in_egypt})

### THIS IS SOLELY FOR MILESTONE 2 PROGRESS REPORT
def test(request):
    sellers_in_egypt = Seller.objects.filter(country_name='Egypt')
    return render(request, 'test.html', {'sellers_in_egypt': sellers_in_egypt})
###

def matchmaker(request):
	prices, countries, sortBy = [], [], []
	if request.method == 'POST':
		info = MatchForm(request.POST)

		if info.is_valid():
			info = info.clean_match_form()
			prices = [info['minPrice'], info['maxPrice']]
			countries = info['countries']
			sortBy = info['sortBy']
			info = MatchForm()
	else: 
		info = MatchForm()

	# for before the form is submitted
	if len(prices) > 0:
		table = Seller.objects.filter(price_per_kwh__gte=prices[0], price_per_kwh__lte=prices[1])
	else: table = Seller.objects.all()

	if len(countries) > 0:
		table = table.filter(country_name__in=countries)

	if len(sortBy) == 1:
			table = table.order_by(sortBy[0])
	if len(sortBy) == 2:
		table = table.order_by(sortBy[0], sortBy[1])

	return render(request, 'matchmaker.html', {'matches': table, 'info': info})

def newseller(request):
	if request.method == 'POST':
		form = SellerForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/newseller/thankyou/')
	else:
		form = SellerForm()
	return render(request, 'newseller.html', {'form': form})

def thankyou(request):
	return render(request, 'thankyou.html')
    
def countries(request):
	
	hasSeller = []
	for c in Country.objects.all():
		if (c==s.country_name for s in Seller.objects.all()):
			hasSeller.append('yes')
		else:
			hasSeller.append('no')
	myList= zip(Country.objects.values_list('name'), Country.objects.values_list('percent_pop_needs_elec'), hasSeller)
	return render(request, 'countries.html', {'myList': myList})



    
