# Generated by Django 2.2.5 on 2019-09-15 17:48

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('dob', models.DateField(null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('recovery_email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BuyOrder',
            fields=[
                ('listingDate', models.DateTimeField(auto_now_add=True)),
                ('buyPrice', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('BuyID', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('name', models.CharField(max_length=40, unique=True)),
                ('price', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('gameID', models.AutoField(primary_key=True, serialize=False)),
                ('timesBought', models.IntegerField(default=0)),
                ('releaseDate', models.DateField(default=datetime.date.today)),
                ('description', models.TextField()),
                ('ageRating', models.IntegerField(default=7)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemID', models.AutoField(primary_key=True, serialize=False)),
                ('newItemPrice', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('itemDescription', models.TextField(validators=[django.core.validators.MinLengthValidator(5)])),
                ('itemName', models.CharField(max_length=50, unique=True)),
                ('itemCondition', models.CharField(choices=[('FN', 'Factory New'), ('FT', 'Field Tested'), ('BS', 'Battle Scarred')], default='FN', max_length=2)),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagId', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=20, validators=[django.core.validators.MaxLengthValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('amount', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('transactionID', models.AutoField(primary_key=True, serialize=False)),
                ('credited_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditor', to=settings.AUTH_USER_MODEL)),
                ('debited_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debitor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('transactionType', models.CharField(choices=[('CR', 'Credit'), ('DR', 'Debit')], max_length=2)),
                ('WalletID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Wallet')),
                ('transactionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Transaction')),
            ],
        ),
        migrations.AddField(
            model_name='wallet',
            name='transactions',
            field=models.ManyToManyField(through='marketplace.WalletTransaction', to='marketplace.Transaction'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SellOrder',
            fields=[
                ('listingDate', models.DateTimeField(auto_now_add=True)),
                ('sellingPrice', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('sellorderID', models.AutoField(primary_key=True, serialize=False)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Item')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewId', models.AutoField(primary_key=True, serialize=False)),
                ('reviewText', models.TextField(validators=[django.core.validators.MinLengthValidator(5)])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isPublic', models.BinaryField(default=1)),
                ('games', models.ManyToManyField(to='marketplace.Game')),
                ('items', models.ManyToManyField(to='marketplace.Item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FullfilledOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulfillmentDate', models.DateTimeField(auto_now_add=True)),
                ('fulfillmentPrice', models.DecimalField(decimal_places=1, default=0.0, max_digits=5)),
                ('buyorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.BuyOrder')),
                ('sellOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.SellOrder')),
            ],
        ),
        migrations.CreateModel(
            name='DLC',
            fields=[
                ('DLCid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('ageRating', models.IntegerField(default=7)),
                ('stars', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('timesBought', models.IntegerField(default=0)),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Review')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='buyorder',
            name='itemID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Item'),
        ),
        migrations.AddField(
            model_name='buyorder',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GameTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Tag')),
            ],
            options={
                'unique_together': {('tag', 'gameID')},
            },
        ),
        migrations.CreateModel(
            name='GameReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Review')),
            ],
            options={
                'unique_together': {('review', 'gameID')},
            },
        ),
        migrations.CreateModel(
            name='gameDLC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DLCid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.DLC')),
                ('gameID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Game')),
            ],
            options={
                'unique_together': {('gameID', 'DLCid')},
            },
        ),
        migrations.CreateModel(
            name='DLCTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DLCid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.DLC')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Tag')),
            ],
            options={
                'unique_together': {('tag', 'DLCid')},
            },
        ),
        migrations.CreateModel(
            name='DLCReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DLCid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.DLC')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.Review')),
            ],
            options={
                'unique_together': {('review', 'DLCid')},
            },
        ),
    ]
