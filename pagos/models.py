from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
# Create your models here.

class Pagos(models.Model):
    class Servicios(models.TextChoices):
        NETFLIX = 'NF', _('Netflix')
        AMAZON = 'AP', _('Amazon Video')
        START = 'ST', _('Start+')
        PARAMOUNT = 'PM', _('Paramount+')


    
    servicio = models.CharField(
        max_length=2,
        choices=Servicios.choices,
        default=Servicios.NETFLIX,
    )
    fecha_pago = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete =models.CASCADE, related_name='users')
    monto = models.FloatField(default=0.0)




class Services(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=200)
    Logo = models.URLField()

    def __str__(self):
        return self.Name


class Payment_user(models.Model):
    Id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    Amount =  models.FloatField(default=0.0)
    PaymentDate = models.DateField(auto_now_add=True)
    ExpirationDate = models.DateField()

    def __str__(self):
        return str(self.Service_id)


class Expired_payments(models.Model):
    Id = models.AutoField(primary_key=True)
    Payment_user_id = models.ForeignKey(Payment_user, on_delete=models.CASCADE)
    Penalty_fee_amount = models.FloatField(default=0.0)