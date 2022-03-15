# Generated by Django 4.0.2 on 2022-03-16 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.BigIntegerField()),
                ('kakao_nickname', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=200)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='PassengerInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('gender', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=200)),
                ('birth_date', models.CharField(max_length=45)),
                ('price', models.DecimalField(decimal_places=1, max_digits=20)),
                ('flight_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.flightschedule')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.reservation')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.seat')),
            ],
            options={
                'db_table': 'passenger_informations',
            },
        ),
    ]