# from django import forms
# from laptops.models import Laptop


# # A mesma solução resumida com (ModelForm)
# class LaptopModelForm(forms.ModelForm):
#   class Meta:
#     model = Laptop
#     fields = '__all__'


#   def clean_value(self): # validaçao de formulario (valor do laptop)
#     value = self.cleaned_data.get('value')
#     if value < 2000:
#       self.add_error('value', 'Valor mínimo de laptop deve ser de R$2000.')
#     return value

#   def clean_factory_year(self): # validaçao do ano de fabricação
#     factory_year = self.cleaned_data.get('factory_year')
#     if factory_year < 2005:
#       self.add_error('factory_year', 'Não é possivel cadastrar laptops fabricados antes de 2005.')
#     return factory_year



from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Laptop, Brand
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Laptop, Brand
import re
import json

class LaptopModelForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
        widgets = {
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: XPS 15 9520'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'specs': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '{"cpu": "Intel i7", "ram": "16GB", "storage": "512GB SSD"}',
                'rows': 5
            }),
        }
        labels = {
            'model': _('Modelo do Laptop'),
            'price': _('Preço (R$)'),
        }
        help_texts = {
            'specs': _('Informe as especificações técnicas em formato JSON'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all().only('id', 'name')

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_model(self):
        model = self.cleaned_data['model']
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', model):
            raise ValidationError(
                _('O modelo deve conter apenas letras, números, espaços e hífens.')
            )
        return model.strip()

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 2000:
            raise ValidationError(
                _('O preço mínimo para um laptop é R$ 2.000,00.')
            )
        return round(price, 2)

    def clean_specs(self):
        specs = self.cleaned_data['specs']
        if not isinstance(specs, dict):
            raise ValidationError(_('As especificações devem ser um objeto JSON.'))

        # Validação opcional: garantir que algumas chaves existam
        required_keys = ['cpu', 'ram', 'storage']
        missing_keys = [key for key in required_keys if key not in specs]

        if missing_keys:
            raise ValidationError(
                _(f'As especificações devem incluir: {", ".join(required_keys)}.')
            )

        return specs



class BrandModelForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if Brand.objects.filter(name__iexact=name).exists():
            raise ValidationError(_('Esta marca já está cadastrada.'))
        return name.title()