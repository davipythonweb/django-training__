# from django.db import models

# class Brand(models.Model):
#   id = models.AutoField(primary_key=True)
#   name = models.CharField(max_length=200)

#   def __str__(self):
#     return self.name

# class Laptop(models.Model):
#   id = models.AutoField(primary_key=True)
#   model = models.CharField(max_length=200)
#   brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='laptop_brand')
#   factory_year = models.IntegerField(blank=True, null=True)
#   model_year = models.IntegerField(blank=True, null=True)
#   cpu = models.CharField(max_length=10, blank=True, null=True)
#   gpu = models.CharField(max_length=10, blank=True, null=True)
#   ram = models.CharField(max_length=10, blank=True, null=True)
#   rom = models.CharField(max_length=10, blank=True, null=True)
#   value = models.FloatField(blank=True, null=True)
#   photo = models.ImageField(upload_to='laptops/', blank=True, null=True)
#   bio = models.TextField(blank=True, null=True)

#   def __str__(self):
#     return self.model


# class LaptopInventory(models.Model):
#   laptops_count = models.IntegerField()
#   laptops_value = models.FloatField()
#   created_at = models.DateTimeField(auto_now_add=True)
  
#   class Meta:
#     ordering = ['-created_at']
    
#   def __str__(self):
#     return f'{self.laptops_count} - {self.laptops_value}'

from django.utils.timezone import now
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.conf import settings
from model_utils import FieldTracker

class Brand(models.Model):
    """Modelo para marcas de laptops"""
    name = models.CharField(
        'Marca',
        max_length=200,
        unique=True,
        help_text='Nome da marca (ex: Dell, Apple)'
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    founded_year = models.PositiveIntegerField(
        'Ano de Fundação',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2023)
        ]
    )
    website = models.URLField('Website', blank=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('laptops:brand_detail', kwargs={'slug': self.slug})


class Laptop(models.Model):
    """Modelo principal para laptops"""
    CONDITION_CHOICES = [
        ('N', 'Novo'),
        ('U', 'Usado'),
        ('R', 'Recondicionado'),
    ]
    
    tracker = FieldTracker()
    
    model = models.CharField(
        'Modelo',
        max_length=200,
        help_text='Modelo específico do laptop'
    )
    slug = models.SlugField(max_length=200, blank=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='laptops',
        verbose_name='Marca'
    )
    
    
    condition = models.CharField(
        'Condição',
        max_length=1,
        choices=CONDITION_CHOICES,
        default='N'
    )


    cpu = models.CharField('Processador', max_length=100, blank=True)
    ram = models.CharField('Memória RAM', max_length=50, blank=True)
    storage = models.CharField('Armazenamento', max_length=100, blank=True)
    gpu = models.CharField('Placa de Vídeo', max_length=100, blank=True)
    screen = models.CharField('Tela', max_length=100, blank=True)
    os = models.CharField('Sistema Operacional', max_length=100, blank=True)
    other = models.TextField('Outras Informações', blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2000.00,
        validators=[MinValueValidator(2000)]
    )

    photo = models.ImageField(
        'Foto',
        upload_to='laptops/%Y/%m/%d/',
        blank=True
    )

    created_at = models.DateTimeField(
        'Data de criação',
        auto_now_add=True,
        null=True,  # Temporariamente permita nulo
        blank=True
    )
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='added_laptops'
    )

    class Meta:
        verbose_name = 'Laptop'
        verbose_name_plural = 'Laptops'
        ordering = ['-created_at']
        unique_together = ['brand', 'model']
        indexes = [
            models.Index(fields=['brand', 'model']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.brand} {self.model}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('laptops:laptop_detail', kwargs={'pk': self.pk})

    @property
    def is_new(self):
        return self.condition == 'N'


class Inventory(models.Model):
    laptop = models.ForeignKey(
        'Laptop', 
        on_delete=models.CASCADE,
        related_name='inventory_records',
        null=True,  # Opcional: permitir registros sem laptop
        blank=True
    )
    laptops_count = models.PositiveIntegerField('Total de Laptops', default=0)
    total_value = models.DecimalField('Valor Total', max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        verbose_name = 'Inventário'
        verbose_name_plural = 'Inventários'
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return f"Inventário {self.created_at.strftime('%d/%m/%Y')}"