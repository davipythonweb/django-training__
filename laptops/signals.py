from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from laptops.models import Laptop, LaptopInventory

from django.db.models import Sum


def laptop_invetory_update():
    laptops_count = Laptop.objects.all().count() # calcula a qtd de laptopros no estoque
    laptops_value = Laptop.objects.aggregate(total_value=Sum('value'))['total_value'] # calcula o o valor total da soma(R$) dos laptopros do estoque
    LaptopInventory.objects.create(laptops_count=laptops_count, laptops_value=laptops_value) # cria a nova tabela no banco
    
    
@receiver(pre_save, sender=Laptop)
def laptop_pre_save(sender, instance, **kwargs):
   if not instance.bio:
       instance.bio = 'Para mais informações: faleconosco@contato.com'
        
@receiver(post_save, sender=Laptop)
def laptop_post_save(sender, instance, **kwargs):
    laptop_invetory_update()
    
@receiver(post_delete, sender=Laptop)
def laptop_post_delete(sender, instance, **kwargs):
    laptop_invetory_update()
    