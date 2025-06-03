from django import forms
# from laptops.models import Brand
from laptops.models import laptop


# A mesma solução resumida com (ModelForm)
class laptopModelForm(forms.ModelForm):
  class Meta:
    model = laptop
    fields = '__all__'


  def clean_value(self): # validaçao de formulario (valor do laptopro)
    value = self.cleaned_data.get('value')
    if value < 2000:
      self.add_error('value', 'Valor mínimo de laptop deve ser de R$2000.')
    return value

  def clean_factory_year(self): # validaçao do ano de fabricação
    factory_year = self.cleaned_data.get('factory_year')
    if factory_year < 2005:
      self.add_error('factory_year', 'Não é possivel cadastrar laptops fabricados antes de 2005.')
    return factory_year



