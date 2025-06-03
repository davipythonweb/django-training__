from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from laptops.models import laptop, laptopInventory

from django.db.models import Sum


def laptop_invetory_update():
    laptops_count = laptop.objects.all().count() # calcula a qtd de laptopros no estoque
    laptops_value = laptop.objects.aggregate(total_value=Sum('value'))['total_value'] # calcula o o valor total da soma(R$) dos laptopros do estoque
    laptopInventory.objects.create(laptops_count=laptops_count, laptops_value=laptops_value) # cria a nova tabela no banco
    
    
@receiver(pre_save, sender=laptop)
def laptop_pre_save(sender, instance, **kwargs):
   if not instance.bio:
       instance.bio = 'Para mais informações: faleconosco@contato.com'
        
@receiver(post_save, sender=laptop)
def laptop_post_save(sender, instance, **kwargs):
    laptop_invetory_update()
    
@receiver(post_delete, sender=laptop)
def laptop_post_delete(sender, instance, **kwargs):
    laptop_invetory_update()
    