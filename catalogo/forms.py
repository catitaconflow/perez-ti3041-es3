from django import forms
from .models import Herramienta
from .models import ConsultaCliente

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre', 'categoria', 'precio', 'stock', 'marca']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ConsultaClienteForm(forms.ModelForm):

    class Meta:
        model = ConsultaCliente
        fields = [
            "nombre",
            "correo",
            "mensaje",
            "producto_interes"
        ]

    def clean_mensaje(self):
        mensaje = self.cleaned_data["mensaje"]

        if len(mensaje) < 10:
            raise forms.ValidationError(
                "El mensaje debe tener al menos 10 caracteres"
            )

        return mensaje