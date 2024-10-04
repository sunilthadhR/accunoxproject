# Generated by Django 4.2.16 on 2024-09-26 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('Age', models.IntegerField(blank=True, null=True)),
                ('phonenumber', models.BigIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(blank=True, max_length=20, null=True)),
                ('version', models.CharField(blank=True, max_length=20, null=True)),
                ('Serialnumber', models.CharField(blank=True, max_length=20, null=True)),
                ('create_on', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='usertable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile', models.BigIntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=20)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_key', models.CharField(blank=True, max_length=100, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='session', to='new.device')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='new.usertable')),
            ],
        ),
        migrations.CreateModel(
            name='FriendList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=20, null=True)),
                ('friend_list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend_list', to='new.customer')),
            ],
        ),
    ]
