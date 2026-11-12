from django.contrib import admin

from .models import Herramienta
from .models import ConsultaCliente


@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "marca")
    search_fields = ("nombre", "marca")
    list_filter = ("categoria", "marca")



@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "correo",
        "producto_interes",
        "fecha"
    )

    search_fields = (
        "nombre",
        "correo"
    )