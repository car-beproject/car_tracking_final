# Generated by Django 3.0.1 on 2020-01-01 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser_db',
            fields=[
                ('u_name', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('p_word', models.CharField(max_length=70)),
                ('u_role', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='CameraDb',
            fields=[
                ('ip_address', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=70)),
                ('camera_type', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='New_camera_type_db',
            fields=[
                ('camera_type', models.CharField(max_length=70, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='New_location_db',
            fields=[
                ('location', models.CharField(max_length=70, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='New_role_db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=20)),
                ('vehicle_image', models.ImageField(upload_to='pics')),
                ('location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]