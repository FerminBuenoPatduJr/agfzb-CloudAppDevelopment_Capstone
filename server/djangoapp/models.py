from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Car Make - default')
    description = models.CharField(null=False, max_length=30, default='Description Car Make - default')

    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    dealerid = models.IntegerField()
    name = models.CharField(null=False, max_length=30, default='Car Model - default')
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    cartype = models.CharField(
        null=False,
        max_length=20,
        choices=CAR_TYPE,
        default=SEDAN
    )
    year = models.DateField(null=True)
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Dealer ID: " + str(self.dealerid) + ", " + \
               "Name: " + self.name + ", " + \
               "Name: " + self.cartype + ", " + \
               "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
        # Dealer state
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, color):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.color = color
    
    def __str__(self):
        return "ID: " + str(self.id) + ", " + \
               "Dealership: " + str(self.dealership) + ", " + \
               "Name: " + self.name + ", " + \
               "Purchase: " + self.purchase + ", " + \
               "Review: " + str(self.review) + ", " + \
               "Purchase Date: " + str(self.purchase_date) + ", " + \
               "Car Make: " + self.car_make + ", " + \
               "Car Model: " + self.car_model + ", " + \
               "Car Year: " + self.car_year  + ", " + \
               "Sentiment: " + self.sentiment
  
