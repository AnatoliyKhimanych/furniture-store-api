from django.db import models

class Furniture(models.Model):
  CATEGORIES = [
    ('table', 'Стол'),
    ('chair', 'Стул'),
    ('sofa', 'Диван')
  ]

  name = models.CharField('Название', max_length=30)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  category = models.CharField(max_length=10, choices=CATEGORIES, db_index=True)

class Order(models.Model):
  email = models.EmailField(max_length=30, db_index=True)
  goods_list = models.ManyToManyField(Furniture)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateTimeField(auto_now_add=True)
