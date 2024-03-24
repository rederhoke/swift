from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from miniCryptoApp.views import signup
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin_portal/', admin.site.urls),
    path('',include('miniCryptoApp.urls')),
    path('',include('gentannieReferal.urls')),
    path('login_now',LoginView.as_view(),name='login'),
    path('signup/',signup,name='signup'),
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

