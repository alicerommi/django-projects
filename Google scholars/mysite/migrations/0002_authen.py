# Generated by Django 4.0.3 on 2022-03-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authen',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.TextField(blank=True, null=True)),
                ('password', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'gscholarusers',
            },
        ),
    ]
