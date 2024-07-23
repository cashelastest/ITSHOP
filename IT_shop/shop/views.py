from django.shortcuts import render
def home(request):
	return render(request, 'shop/home.html')
# Create your views here.
