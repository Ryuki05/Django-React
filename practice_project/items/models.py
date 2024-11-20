from django.db import models

# Create your models here.

class Items_table(models.Model):
    #item_id = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    
