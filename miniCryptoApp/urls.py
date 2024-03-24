from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup
from . import views
from gentannieReferal.views import *

urlpatterns = [
    path('', views.index,name='index'),
    path('userPanel/', views.userPanel,name='userPanel'),
    path('logout/', views.logoutUser,name='logout'),    
    path('signup/',signup,name='signup'),
    path('exc_dark/',views.exc_dark,name='exc_dark'),
    path('market/',views.market,name='market'),
    path('market_overview/',views.market_overview,name='market_overview'),


    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/',auth_views.PasswordChangeView.as_view(), 
        name='password_change'),

    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/',auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

]

  