from django.db import models

class Brand(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Laptop(models.Model):
  id = models.AutoField(primary_key=True)
  model = models.CharField(max_length=200)
  brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='laptop_brand')
  factory_year = models.IntegerField(blank=True, null=True)
  model_year = models.IntegerField(blank=True, null=True)
  plate = models.CharField(max_length=10, blank=True, null=True)
  value = models.FloatField(blank=True, null=True)
  photo = models.ImageField(upload_to='laptops/', blank=True, null=True)
  bio = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.model


class LaptopInventory(models.Model):
  laptops_count = models.IntegerField()
  laptops_value = models.FloatField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-created_at']
    
  def __str__(self):
    return f'{self.laptops_count} - {self.laptops_value}'