# Generated by Django 4.1.4 on 2022-12-20 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pagos', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=200)),
                ('Description', models.CharField(max_length=200)),
                ('Logo', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment_user',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Amount', models.FloatField(default=0.0)),
                ('PaymentDate', models.DateField(auto_now_add=True)),
                ('ExpirationDate', models.DateField()),
                ('Service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagos.services')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
