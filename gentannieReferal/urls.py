from django.contrib.auth import views as auth_views
from django.urls import path
# from .views import signupview
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:ref_code>/', referal_views, name='referal_views'),
    # path('<str:ref_code>/', signup_view, name='signup_view'),

    path('referal_views', views.Referal_views, name='Referal_views'),

    path('referal_profile', my_recomms_views, name='my_recomms_views'),
    path('signup_view', signup_view, name='signup_view'),        
    path('terms_n_conditions',views.terms_n_condition, name='terms_n_condition'),
]
