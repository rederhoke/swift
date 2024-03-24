from django.db.models.expressions import F
from django.shortcuts import render,redirect
from miniCryptoApp.models import *
from .models import *
from .form import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail



def Referal_views(request,  *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = user_referal.objects.get(code=code)
        request.session['ref_profile'] = profiles.id
        print('id', profiles.id)
    except:
        pass
    session = request.session.get_expiry_age()
    context = {
        'session':session
    }
    # return render(request, 'gentannieReferal/dash/referal_view.html', context)
    return render(request, 'swiftxbtApp/dash/Referal_page.html', context)

def my_recomms_views(request):
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    user_referal_profile = user_referal.objects.filter(user=request.user)

    context = {
        'recomms_rewards':recomms_rewards,
        'my_recs':my_recs,
        'user_referal_profile':user_referal_profile,
        'recom_len':recom_len,
    }
    return render (request, 'gentannieReferal/index2.html', context)


def index(request):
    
    return render(request,'gentannieReferal/index.html',None)

def terms_n_condition(request):
    context={}
    return render(request,'gentannieReferal/terms_n_conditions.html',context)

def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id **(--)*** ', profile_id)
    # form = UserCreationForm(request.POST or None)
    form = signupForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = user_referal.objects.get(id=profile_id)

            user = form.save()
            user.refresh_from_db()
            user.profile.country = form.cleaned_data.get("country")
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            # user.profile.currency = form.cleaned_data.get("currency")
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            coin_progress.objects.create(user=user)

            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = user_referal.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('userPanel')
        # return redirect('my_recomms_views')
    context={
        'form':form
    }

    return render(request,'registration/signup.html', context)

# ************** Referal section ******************
def referal_views(request,  *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = user_referal.objects.get(code=code)
        request.session['ref_profile'] = profiles.id
        print('id', profiles.id)
    except:
        pass
    print('site will espire in ', request.session.get_expiry_date())

    session = request.session.get_expiry_age()
    context = {
        'session':session
    }
    return render(request, 'gentannieReferal/dash/referal_view.html', context)

def my_recomms_views(request):
    recom_profiles = user_referal.objects.get(user=request.user)

    my_recs = recom_profiles.get_recommended_profiles()
    recom_len =  len(my_recs)
    recomms_rewards = recom_len*1000

    user_profile = user_referal.objects.all().filter(user=request.user)

    user_investment_check = users_investment_progress.objects.all().filter(user=request.user)
    user_investment_check.exists()
    context = {
        'recomms_rewards':recomms_rewards,
        'my_recs':my_recs,
        'user_profile':user_profile,
        'recom_len':recom_len,
        "user_investment_check":user_investment_check,
    }
    return render (request, 'miniCryptoApp/Referal_page.html', context)
    # return render (request, 'gentannieReferal/index2.html', context)

