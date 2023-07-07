from django.db import models

# Create your models here.
class Title(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'gscholar'

class Authen(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField(blank=True,null=True)
    password = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'gscholarusers'