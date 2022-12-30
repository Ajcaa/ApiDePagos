from django.contrib import admin
from . models import Services, Payment_user, Expired_payments
# Register your models here.

admin.site.register(Services)
admin.site.register(Payment_user)
admin.site.register(Expired_payments)