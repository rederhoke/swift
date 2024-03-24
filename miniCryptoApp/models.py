from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django_countries import countries
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


Basic = 'Basic : $300 - $2,999'
Standard = 'Standard : $3,000 - $4,999'
Gold = 'Gold : $5,000 - $8,999'
Bronze = 'Bronze : $9,000 - $14,000'
Platinum = 'Platinum : $15,000 - $20,000'

Account_types = [
    (Basic,'Basic : $300 - $2,999'), (Standard,'Standard : $3,000 - $4,999'), 
    (Gold,'Gold : $5,000 - $8,999'), (Bronze,'Bronze : $9,000 - $14,999'),
    (Platinum,'Platinum : $15,000 - $20,000'),
    ]

Passport = 'Passport'
ID = 'ID'
Driving_licence = 'Driving_licence'
veri_type = [(Passport,'Passport'), (ID,'ID'),(Driving_licence,'Driving_licence')]

class coin_progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, default=User)
    deposit = models.CharField(max_length=20, default=0)
    bonus = models.CharField(max_length=20, default=0)
    acc_verified = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    pin_payed = models.BooleanField(default=False)
    upgraded = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=100, null=True, default='welcome to litexbt, proceed to verify your account.')

    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return self.username

class profile(models.Model):
    DOLLARS = 'USD'
    EURO = 'EUR'
    POUNDS = 'GBP'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    # phone_number = PhoneNumberField()
    country = CountryField(max_length=20,choices=list(countries))
    pay = [ (EURO,'EURO'),(DOLLARS,'dollars'),(POUNDS,'Pounds'), ]
    # currency = models.CharField(max_length=10,choices=pay,default='dollars')
    Account_type = models.CharField(max_length=40,choices=Account_types )
    password = models.CharField(max_length=40, )

    def __str__(self):
        # return  str(self.user) +"~" + str(self.phone_number) +'~'+ str(self.currency) + '~' + str(self.country.name) + '~' + str(self.Account_type) + '~'+ str(self.password)
        return  str(self.user) +"~" + str(self.phone_number) + '~' + str(self.Account_type) + '~'+ str(self.password)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance,created,**kwargs):
    if created:
        profile.objects.create(user=instance)
    instance.profile.save()

class verificationForm(models.Model):
    username = models.CharField(max_length=50)
    Document_type = models.CharField(max_length=50, choices=veri_type)
    document_upload = models.ImageField(upload_to='images/')
    time_uploaded = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.username) + str(self.Document_type)  + str(self.document_upload) + str(self.time_uploaded)

class withdraw_request(models.Model):
    username = models.CharField(max_length=40)
    amount = models.CharField(max_length=50,help_text="enter amount to withdraw")
    wallet_address = models.CharField(max_length=50, help_text= "enter/paste your wallet address")
    Email = models.EmailField()
    withdraw_date = models.DateTimeField(auto_now_add=True,)
    class Meta:
        ordering = ['-withdraw_date']

    def __str__(self):
        return str(self.username) + str(self.amount) + str(self.wallet_address) + str(self.withdraw_date)

class upgrade(models.Model):
    Account_type = models.CharField(max_length=40,choices=Account_types )