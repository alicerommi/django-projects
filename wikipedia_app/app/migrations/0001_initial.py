# Generated by Django 4.0.2 on 2022-02-26 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wikipedia_keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=200)),
                ('keyword_description', models.TextField(max_length=500)),
                ('keyword_timedate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
