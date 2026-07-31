from django.db import models

class Furniture(models.Model):
  name = models.CharField('Название', max_length=30)
  price = models.DecimalField(max_digits=10, decimal_places=2)
