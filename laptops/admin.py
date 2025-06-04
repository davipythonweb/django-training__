# from django.contrib import admin
# from laptops.models import Laptop, Brand

# class BrandAdmin(admin.ModelAdmin):
#   list_display = ('name',)
#   search_fields = ('name',)

# class LaptopAdmin(admin.ModelAdmin):
#   list_display = ('model', 'brand', 'factory_year','cpu','ram','gpu','rom', 'model_year', 'value')
#   search_fields = ('model','brand')


# admin.site.register(Brand, BrandAdmin)
# admin.site.register(Laptop, LaptopAdmin)

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Laptop, Brand, Inventory
from .forms import LaptopModelForm, BrandModelForm

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    fields = ('laptops_count', 'total_value', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = False
    max_num = 1
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandModelForm
    list_display = ('name', 'founded_year', 'website_link', 'laptops_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    
    def website_link(self, obj):
        if obj.website:
            return format_html(
                '<a href="{}" target="_blank">Acessar</a>',
                obj.website
            )
        return '-'
    website_link.short_description = 'Website'
    
    def laptops_count(self, obj):
        count = obj.laptops.count()
        url = (
            reverse('admin:laptops_laptop_changelist') 
            + f'?brand__id__exact={obj.id}'
        )
        return format_html(
            '<a href="{}">{} laptops</a>',
            url,
            count
        )
    laptops_count.short_description = 'Total de Laptops'

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    form = LaptopModelForm
    list_display = (
        'thumbnail',
        'full_model',
        'price_formatted',
        'condition_display',
        'created_at'
    )
    list_filter = ('brand', 'condition', 'created_at')
    search_fields = ('model', 'brand__name', 'specs')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    autocomplete_fields = ('brand',)
    date_hierarchy = 'created_at'
    save_on_top = True
    inlines = [InventoryInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('brand', 'model', 'slug', 'condition')
        }),
        ('Detalhes Técnicos', {
            'fields': ('specs', 'price', 'photo'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide',)
        }),
    )
    
    def thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: contain;" />',
                obj.photo.url
            )
        return '-'
    thumbnail.short_description = 'Foto'
    
    def full_model(self, obj):
        return f"{obj.brand} {obj.model}"
    full_model.short_description = 'Modelo'
    full_model.admin_order_field = 'model'
    
    def price_formatted(self, obj):
        return f"R$ {obj.price:,.2f}"
    price_formatted.short_description = 'Preço'
    price_formatted.admin_order_field = 'price'
    
    def condition_display(self, obj):
        color = {
            'N': 'green',
            'U': 'orange',
            'R': 'blue'
        }.get(obj.condition, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_condition_display()
        )
    condition_display.short_description = 'Condição'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'laptops_count', 'total_value_formatted')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def total_value_formatted(self, obj):
        return f"R$ {obj.total_value:,.2f}"
    total_value_formatted.short_description = 'Valor Total'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False