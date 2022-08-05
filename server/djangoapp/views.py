from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealers_by_id_from_cf, get_reviews_by_id_from_cf, post_request, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "POST":

        if isNotNumber(request.POST['id']):
            context['message'] = 'Enter only numbers'
            return render(request, 'djangoapp/review.html', context)
        
        id = int(request.POST['id'])

        if id <= 0:
            context['message'] = 'Enter only positive numbers'
            return render(request, 'djangoapp/review.html', context)

        url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"

        # Get dealers from the URL
        dealership = get_dealers_by_id_from_cf(url, id)
        
        if dealership == []:
            context['message'] = 'Dealership not found'
            return render(request, 'djangoapp/review.html', context)

        carmake = CarMake.objects.all()
        carmodel = CarModel.objects.all()

        context['dealership'] = dealership
        context['id'] = id
        context['carmake'] = carmake
        context['carmodel'] = carmodel
        

    return render(request, 'djangoapp/review.html', context)


def isNotNumber(value):
    try:
         int(value)
    except ValueError:
         return True
    return False


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, id):

    
    #dealership = request.POST['dealer']

    id = int(id)

    sentiment = analyze_review_sentiments(request.POST['review'])

    review = {}
    review['ID'] = 9
    review['NAME'] = request.user.first_name + " " + request.user.last_name
    review['DEALERSHIP'] = id
    review['REVIEW'] = request.POST['review']

    purchase = request.POST.get('purchasecheck', False)

    review['PURCHASE'] = purchase

    review['ANOTHER'] = ''
    review['PURCHASEDATE'] = request.POST['purchasedate']
    review['CARMAKE'] = request.POST['carmake']
    review['CARMODEL'] = request.POST['carmodel']
    review['CARYEAR'] = int(request.POST['caryear'])
    review['SENTIMENT'] = sentiment
    
    context = {}

    url = 'https://c46b6c26.us-south.apigw.appdomain.cloud/api2/postreviews'
    
    context['add_review'] = post_request(url, review)

    context['id'] = int(id)


    # Get dealers from the URL
    url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"
    dealership = get_dealers_by_id_from_cf(url, id)

        # Return a detail of dealer
    context['dealership'] = dealership
    context['id'] = id

    url = 'https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getreviews'

    reviews = get_reviews_by_id_from_cf(url, id)


    context['reviews'] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

def get_all_dealerships(request):
    context = {}
    
    url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"

        # Get dealers from the URL
    dealerships = get_dealers_from_cf(url, context)
        
    context['dealerships'] = dealerships
    
    return render(request, 'djangoapp/index.html', context)

def dealer_details(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer(request):
    context = {}
    if request.method == "GET":

        if isNotNumber(request.GET['id']):
            context['message'] = 'Enter only numbers'
            return render(request, 'djangoapp/dealer_details.html', context)
        
        id = int(request.GET['id'])

        if id <= 0:
            context['message'] = 'Enter only positive numbers'
            return render(request, 'djangoapp/dealer_details.html', context)

        url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"

        # Get dealers from the URL
        dealership = get_dealers_by_id_from_cf(url, id)
        
        if dealership == []:
            context['message'] = 'Dealership not found'
            return render(request, 'djangoapp/dealer_details.html', context)

        # Return a detail of dealer
        context['dealership'] = dealership
        for dealer in dealership:
            context['id'] = dealer.id 

        url = 'https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getreviews'

        reviews = get_reviews_by_id_from_cf(url, id)

        if reviews == []:
            for dealer in dealership:
                context['messagereview'] = 'There aren''t reviews for '+dealer.full_name
            return render(request, 'djangoapp/dealer_details.html', context)

        context['reviews'] = reviews
    
    return render(request, 'djangoapp/dealer_details.html', context)

def dealer_details_id(request, id):
    context = {}
    if request.method == "GET":

        id = int(id)

        # Get dealers from the URL
        url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"
        dealership = get_dealers_by_id_from_cf(url, id)
        
        if dealership == []:
            context['message'] = 'Dealership not found'
            return render(request, 'djangoapp/dealer_details.html', context)

        # Return a detail of dealer
        context['dealership'] = dealership
        context['id'] = id

        url = 'https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getreviews'

        reviews = get_reviews_by_id_from_cf(url, id)

        if reviews == []:
            for dealer in dealership:
                context['messagereview'] = 'There aren''t reviews for '+dealer.full_name
            return render(request, 'djangoapp/dealer_details.html', context)

        context['reviews'] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

def send_review(request, id):
    context = {}

    if request.method == 'GET':

        id = int(id)

        url = "https://c46b6c26.us-south.apigw.appdomain.cloud/api2/getdealerships"

        # Get dealers from the URL
        dealership = get_dealers_by_id_from_cf(url, id)

        carmake = CarMake.objects.all()
        carmodel = CarModel.objects.all()

        context['dealership'] = dealership
        context['id'] = id
        context['carmake'] = carmake
        context['carmodel'] = carmodel
        

    return render(request, 'djangoapp/review.html', context)
