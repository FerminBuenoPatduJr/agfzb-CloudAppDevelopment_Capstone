import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_request_review(url):
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_by_id_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, {'id':id})
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            if dealer_doc["id"] == id:
                results.append(dealer_obj)

    return results

def get_reviews_by_id_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request_review(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
                        
            color = ''

            sentiment = review_doc["sentiment"]

            if sentiment == 'positive':
                color = '$blue-100'
            if sentiment == 'negative':
                color = '$red-100'
            if sentiment == 'neutral':
                color = '$yellow-100'


            review_obj = DealerReview(id=review_doc["id"], dealership=review_doc["dealership"], name=review_doc["name"], 
            purchase=review_doc["purchase"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],
            car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"],
            sentiment=review_doc["sentiment"], color=color)
            if review_doc["dealership"] == id:
                results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/a9ba0d30-e646-4c14-b6fa-6bf297135b89"
    apikey = "yTrDJAF0D3zmg00KmGU1zpEz3RtCm3X_T4KhE_sEer_W"
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    response = natural_language_understanding.analyze(
    text=text, language="en", 
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()
    
    conception = response["keywords"][0]["sentiment"]["label"]
    return conception

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload):
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return response
