# from django.db.models.signals import pre_save, post_save, post_delete
# from django.dispatch import receiver
# from laptops.models import Laptop, LaptopInventory

# from django.db.models import Sum


# def laptop_invetory_update():
#     laptops_count = Laptop.objects.all().count() # calcula a qtd de laptops no estoque
#     laptops_value = Laptop.objects.aggregate(total_value=Sum('value'))['total_value'] # calcula o o valor total da soma(R$) dos laptops do estoque
#     LaptopInventory.objects.create(laptops_count=laptops_count, laptops_value=laptops_value) # cria a nova tabela no banco
    
    
# @receiver(pre_save, sender=Laptop)
# def laptop_pre_save(sender, instance, **kwargs):
#    if not instance.bio:
#        instance.bio = 'Para mais informações: faleconosco@contato.com'
        
# @receiver(post_save, sender=Laptop)
# def laptop_post_save(sender, instance, **kwargs):
#     laptop_invetory_update()
    
# @receiver(post_delete, sender=Laptop)
# def laptop_post_delete(sender, instance, **kwargs):
#     laptop_invetory_update()
    
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.cache import cache
from django.db.models import Count, Sum
from .models import Laptop, Inventory
import logging
from django.utils.text import slugify

logger = logging.getLogger(__name__)

def update_inventory():
    """
    Atualiza o inventário de forma atômica e thread-safe.
    Inclui tratamento de erros e logging.
    """
    try:
        with transaction.atomic():
            # Cálculo das estatísticas
            stats = Laptop.objects.aggregate(
                total=Count('id'),
                value=Sum('price')
            )
            
            # Criação do registro de inventário
            Inventory.objects.create(
                laptops_count=stats['total'] or 0,
                total_value=stats['value'] or 0
            )
            
            # Garantia que 'None' não cause erro de formatação
            valor = stats['value'] or 0
            logger.info(f"Inventário atualizado: {stats['total'] or 0} laptops, R$ {valor:.2f}")
            
    except Exception as e:
        logger.error(f"Erro ao atualizar inventário: {str(e)}")
        raise  # Re-lança a exceção para que o Django a registre

@receiver(pre_save, sender=Laptop)
def laptop_pre_save(sender, instance, **kwargs):
    """
    Pré-processamento antes de salvar:
    - Gera slug automático
    - Valida preço mínimo
    - Limpa cache relacionado
    """
    if not instance.slug:
        base_slug = f"{instance.brand.name if instance.brand else 'no-brand'}-{instance.model}"
        instance.slug = slugify(base_slug)[:200]
    
    if instance.price is None or instance.price < 2000:
        instance.price = 2000
        logger.warning(f"Preço ajustado para o mínimo em {instance}")

@receiver(post_save, sender=Laptop)
def laptop_post_save(sender, instance, created, **kwargs):
    """
    Pós-salvamento:
    - Atualiza inventário se for novo registro ou preço alterado
    """
    if created or 'price' in instance.tracker.changed():
        update_inventory()
    
    cache.delete('laptops:stats')

@receiver(post_delete, sender=Laptop)
def laptop_post_delete(sender, instance, **kwargs):
    """
    Pós-exclusão:
    - Força atualização do inventário
    """
    update_inventory()
    
    if instance.pk:
        cache.delete(f'laptops:detail:{instance.pk}')

# Registro de signals via ready() (Método recomendado)
def register_signals():
    from django.apps import apps
    
    if apps.ready:
        # Conexão explícita para evitar duplicações
        post_save.connect(laptop_post_save, sender=Laptop, weak=False)
        post_delete.connect(laptop_post_delete, sender=Laptop, weak=False)
        pre_save.connect(laptop_pre_save, sender=Laptop, weak=False)
        logger.info("Signals do app Laptops registrados com sucesso")
