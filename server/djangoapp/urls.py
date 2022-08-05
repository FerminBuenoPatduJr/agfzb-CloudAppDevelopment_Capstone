from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.get_all_dealerships, name='index'),


    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path('registration', views.registration_request, name='registration'),

    # path for login
    path(route='login', view=views.login_request, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    # path for dealer reviews view
    path(route='review', view=views.get_dealerships, name='review'),

    # path for add a review view
    path(route='<int:id>:/add_review', view=views.add_review, name='add_review'),

    path(route='<int:id>:/send_review', view=views.send_review, name='send_review'),

    path(route='dealership', view=views.dealer_details, name='dealership'),

    path(route='get_dealer', view=views.get_dealer, name='get_dealer'),

    path(route='<int:id>:/dealer_details_id', view=views.dealer_details_id, name='dealer_details_id'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
