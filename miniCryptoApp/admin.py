from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group
from .models import coin_progress,profile,User,verificationForm,withdraw_request

admin.site.site_header = "swiftxbt Portal📈"
admin.site.index_title = "swiftxbt Admin-Panel "

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'deposit', 'bonus','acc_verified','payed','pin_payed','date_created','message')
    search_fields = ('user',)

class VeriAdmin(admin.ModelAdmin):
    list_display = ('username','Document_type','document_upload','time_uploaded')
    search_fields = ('user',)

class ProfileInline(admin.StackedInline):
    model = profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'
    # fields = ('username','email','first_name','last_name','is_staff','country','phone_number')

class UserAdmin(UserAdmin):
    inlines = [ProfileInline, ]
    list_display = ['username','first_name','last_name','email','is_staff','profile']
    list_dispaly_related = ('profile', )

    def get_country(self, instance):
        return instance.profile.country
        get_country.short_description = 'country'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super (UserAdmin,self).get_inline_instances(request, obj)

class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number','country','Account_type','password')
    # list_display = ('user', 'phone_number','currency','country','Account_type','password')
    search_fields = ('user',)

class withdrawAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount','wallet_address','Email','withdraw_date')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(coin_progress,PostAdmin)
admin.site.register(profile,profileAdmin)
admin.site.register(verificationForm,VeriAdmin)
admin.site.register(withdraw_request,withdrawAdmin)
admin.site.unregister(Group)



