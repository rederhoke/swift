from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import coin_progress,profile, upgrade,verificationForm,withdraw_request
from .forms import signupForm,veriForm,withdraw_request_form,upgrade_form
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

from pycoingecko import CoinGeckoAPI

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as update_session_auth_hash,
)
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from gentannieReferal.form import *
from gentannieReferal.models import user_referal
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string, get_template

UserModel = get_user_model()

class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

cg = CoinGeckoAPI()

def index(request):
    latest = withdraw_request.objects.order_by('-withdraw_date')[0:5]
    deposit_history = coin_progress.objects.order_by('-date_created')[0:5]

    cypto_update = None
    try:
        cypto_id = cg.get_price(ids=['bitcoin','litecoin','ethereum','ripple','iota'],
          vs_currencies=['usd','eur','gbp']
          )
        cypto_update = [cypto_id]
    except:
        print("try again")
        cypto_update = ['bitcoin','litecoin','ethereum','ripple','iota']

    context = {
        'Btc':'',
        'Eth':'',
        'Btc cash ':'',
        'Litcoin':'',
        'Ripple':'',
        }

    if request.user.is_authenticated:
        # coin_table = coin_progress.objects.filter(user=request.user)
        context = {
            'latest':latest,
            'deposit_history':deposit_history,
            "cypto_update":cypto_update,
            }
        return render(request,'miniCryptoApp/index.html',context)
    else:
        context = {
            'latest':latest,
            'deposit_history':deposit_history,
            "cypto_update":cypto_update,
            }
        return render(request,'miniCryptoApp/index.html',context)
        
def userPanel(request):
    if request.method == 'POST':
        form = veriForm(request.POST, request.FILES)
        form2 = withdraw_request_form(request.POST)        
        plan_upgrade = upgrade_form(request.POST)

        if form2.is_valid():
            post2 = form2.save()
            post2.save()
            messages.success(request,"Your withdrawal request has been received and is being processed. Please be patient!!!")
            return  redirect('userPanel')
    
        if form.is_valid():
            post = form.save()
            coin_progress.objects.filter(user=request.user).update(acc_verified=True) #updates the data item acc_verified in the coin_progress table
            post.save()
            # messages.success(request,"form submited!!! please do not resend as your request is being processed.")
            return  redirect('userPanel')

        if plan_upgrade.is_valid():
            post3 = plan_upgrade.save()
            post33 = plan_upgrade.cleaned_data.get("Account_type")
            profile.objects.filter(user=request.user).update(Account_type = post33)
            post3.save()
            
    else:
        form = veriForm()
        form2 = withdraw_request_form
        plan_upgrade = upgrade_form

    # ********** Referal Section **********
    recom_profiles = user_referal.objects.get(user=request.user)
    my_recs = recom_profiles.get_recommended_profiles()

    recom_len =  len(my_recs)
    recomms_rewards = recom_len*10

    referal_no_check = user_referal.objects.all().filter(user=request.user).filter(numbers_refered=10).exists()
    referal_no = user_referal.objects.all().filter(user=request.user)
    referal_no.update(numbers_refered=recom_len, Referal_bonus=recomms_rewards)

    Num_refered = user_referal.objects.all().filter(user=request.user)
    # ********** / .Referal Section ***********

    coin_table = coin_progress.objects.filter(user=request.user)
    user_profile = profile.objects.filter(user=request.user)
    veri_table = verificationForm.objects.filter(username=request.user)

    context = {
        'form2':form2,
        'form':form,
        'coin_table':coin_table,
        'user_profile' :user_profile,
        'veri_table': veri_table,
        "plan_upgrade":plan_upgrade,

        "referal_no_check":referal_no_check,
        "Num_refered":Num_refered,
        "recomms_rewards":recomms_rewards,
        "recom_profiles":recom_profiles,
        }

    return render(request,'miniCryptoApp/panel_wallet.html',context)

def exc_dark(request):
    return render(request,'miniCryptoApp/exchange-dark-live-price.html',None)

def market_overview(request):
    return render(request,'miniCryptoApp/market-overview-dark.html',None)

def market(request):

    return render(request,'miniCryptoApp/markets-dark.html',None)


def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()
            user.profile.country = form.cleaned_data.get("country")
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            # user.profil   e.currency = form.cleaned_data.get("currency")
            user.profile.Account_type = form.cleaned_data.get("Account_type")
            user.profile.password = form.cleaned_data.get("password1")
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            coin_progress.objects.create(user=user)

            get_mail = form.cleaned_data.get('email')
            # welcome_mail_sending(get_mail,username,password)

            login(request, user)
            return redirect('login')
    else:
        form = signupForm()
    return render(request,'registration/signup.html',{'form':form})

def logoutUser(request):
    logout(request)
    messages.info(request, "You have log Out!!!")
    return redirect("index")

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def welcome_mail_sending(get_mail,username,password):
    EMAIL_HOST_USER = 'yesterhoke@gmail.com'
    subject =  "Welcome to swiftxbt"
    # message = "Your account is ready "
    # recepient = ['informaniac665@gmail.com']
    # try:
    #     send_mail(subject,
    #         message, 'support@gentannie.com', [get_mail], fail_silently=False)
    # except:
    #     print('MAIL not sent')
    context = {
        "get_mail":get_mail,
        "username":username,
        "password":password,
    }

    message = get_template("miniCryptoApp/mail.html").render(context)
    msg = EmailMessage(
        subject,
        message,
        'yesterhoke@gmail.com',
        [str(get_mail)],
    )
    msg.content_subtype = 'html'
    msg.send()
    print('mail send successfully')