# Generated by Django 2.2.5 on 2019-09-12 09:06

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('name', models.TextField(unique=True)),
                ('price', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('gameID', models.AutoField(primary_key=True, serialize=False)),
                ('timesBought', models.IntegerField(default=0)),
                ('releaseDate', models.DateField(default=datetime.date.today)),
                ('description', models.TextField()),
                ('ageRating', models.IntegerField(default=7)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagId', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.TextField(validators=[django.core.validators.MaxLengthValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('dob', models.DateField()),
                ('first_name', models.TextField(max_length=50)),
                ('last_name', models.TextField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('recovered_email', models.EmailField(max_length=254)),
                ('username', models.TextField(max_length=25, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewId', models.AutoField(primary_key=True, serialize=False)),
                ('reviewText', models.TextField(validators=[django.core.validators.MinLengthValidator(5)])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.User')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemID', models.AutoField(primary_key=True, serialize=False)),
                ('newItemPrice', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('itemDescription', models.TextField(validators=[django.core.validators.MinLengthValidator(5)])),
                ('itemName', models.TextField(unique=True)),
                ('itemCondition', models.CharField(choices=[('FN', 'Factory New'), ('FT', 'Field Tested'), ('BS', 'Battle Scarred')], default='FN', max_length=2)),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='reviews',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Review'),
        ),
        migrations.AddField(
            model_name='game',
            name='tags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Tag'),
        ),
        migrations.CreateModel(
            name='DLC',
            fields=[
                ('name', models.TextField(unique=True)),
                ('ageRating', models.IntegerField(default=7)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('DLCid', models.AutoField(primary_key=True, serialize=False)),
                ('timesBought', models.IntegerField(default=0)),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Review')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Tag')),
            ],
        ),
    ]
