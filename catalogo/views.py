# Create your views here.
from django.http import HttpResponse

def index(request):
    return redirect("herramientas")

import json
from django.http import HttpResponseNotFound
from pathlib import Path
from django.shortcuts import render, redirect
from .forms import ConsultaClienteForm


# catalogo/views.py
from .models import Herramienta
from django.shortcuts import get_object_or_404
from .forms import HerramientaForm # Asegúrate de tener tu form creado

from django.db.models import Count, Avg

# --- ETAPA 1: CRUD DESDE LA WEB (Conectado a la BD) ---


def crear_herramienta(request):

    if not request.session.get("es_admin"):
        return redirect("login")

    if request.method == "POST":
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_herramientas') # Redirige al listado principal tras crear
    else:
        form = HerramientaForm()
    return render(request, "catalogo/herramienta_form.html", {"form": form})

def editar_herramienta(request, pk):
    if not request.session.get("es_admin"):
        return redirect("login")

    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == "POST":
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            return redirect('listado_herramientas') # Redirige al listado principal tras editar
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, "catalogo/herramienta_form.html", {"form": form})

def eliminar_herramienta(request, pk):
    if not request.session.get("es_admin"):
        return redirect("login")

    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == "POST":
        herramienta.delete()
        return redirect('listado_herramientas') # Redirige al listado principal tras eliminar
    return render(request, "catalogo/herramienta_confirm_delete.html", {"herramienta": herramienta})

def listado_herramientas(request):
    # Consulta todos los registros desde la BD
    herramientas = Herramienta.objects.all()

    contexto = {
        "herramientas": herramientas,
        "total": herramientas.count(),
        "disponibles": herramientas.filter(stock__gt=0).count(),
    }

    visitas = request.session.get("visitas", 0)
    visitas += 1
    request.session["visitas"] = visitas

    herramientas = Herramienta.objects.all()

    contexto = {
        "herramientas": herramientas,
        "total": herramientas.count(),
        "disponibles": herramientas.filter(stock__gt=0).count(),
        "visitas": visitas,
    }

    return render(request, "catalogo/lista.html", contexto)


def detalle_herramienta(request, id):
    ruta = Path(__file__).resolve().parent / "data" / "herramientas.json"

    with open(ruta, encoding="utf-8") as f:
        herramientas = json.load(f)

    herramienta = next((h for h in herramientas if h.get("id") == id), None)

    if herramienta is None:
        return HttpResponseNotFound("<h2>Herramienta no encontrada</h2>")

    ultimos = request.session.get("ultimos_productos", [])

    nombre = herramienta["nombre"]

    if nombre in ultimos:
        ultimos.remove(nombre)

    ultimos.insert(0, nombre)

    ultimos = ultimos[:3]

    request.session["ultimos_productos"] = ultimos

    return render(
        request,
        "catalogo/detalle.html",
        {
            "herramienta": herramienta,
            "ultimos": ultimos
        }
    )

#agregar la vista de sesiones entrada y recargas a la pagina


def login_view(request):
    mensaje = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "cata" and password == "1234":
            request.session["usuario"] = username
            request.session["es_admin"] = True
            return redirect("herramientas")

        mensaje = "Credenciales inválidas"

    return render(request, "catalogo/login.html", {"mensaje": mensaje})

def logout_view(request):
    request.session.flush()
    return redirect("herramientas")

import json
from pathlib import Path
from django.shortcuts import render, redirect

# Ruta al archivo JSON
DATA_PATH = Path(__file__).resolve().parent / "data" / "herramientas.json"

def cargar_herramientas():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Detalle de una herramienta
def detalle_herramienta(request, id):
    herramientas = cargar_herramientas()
    herramienta = next((h for h in herramientas if h["id"] == id), None)
    return render(request, "catalogo/detalle.html", {"herramienta": herramienta})


def guardar_herramientas(herramientas):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(herramientas, f, ensure_ascii=False, indent=2)

# Carrito: agregar producto

def agregar_carrito(request, id):
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad", 1))
        carrito = request.session.get("carrito", {})
        carrito[str(id)] = carrito.get(str(id), 0) + cantidad
        request.session["carrito"] = carrito
    return redirect("ver_carrito")


#reportes

def reporte_categoria(request):

    if not request.session.get("es_admin"):
        return redirect("login")

    reporte = Herramienta.objects.values("categoria").annotate(
        cantidad=Count("id"),
        promedio_precio=Avg("precio")
    )

    return render(
        request,
        "catalogo/reporte_categoria.html",
        {"reporte": reporte}
    )

def reporte_stock(request):

    if not request.session.get("es_admin"):
        return redirect("login")

    herramientas = Herramienta.objects.filter(
        stock__lt=10
    ).order_by("stock")

    return render(
        request,
        "catalogo/reporte_stock.html",
        {"herramientas": herramientas}
    )

#consultadecliente por formulario de contacto

def contacto(request):

    if request.method == "POST":

        form = ConsultaClienteForm(request.POST)

        if form.is_valid():
            form.save()

            return render(
                request,
                "catalogo/contacto_exito.html"
            )

    else:
        form = ConsultaClienteForm()

    return render(
        request,
        "catalogo/contacto.html",
        {"form": form}
    )


# Carrito: ver contenido

def ver_carrito(request):
    herramientas = cargar_herramientas()
    carrito = request.session.get("carrito", {})
    items, total = [], 0

    for id, cantidad in carrito.items():
        herramienta = next((h for h in herramientas if h["id"] == int(id)), None)
        if herramienta:
            subtotal = herramienta["precio"] * cantidad  # ✅ cálculo correcto
            items.append({
                "herramienta": herramienta,
                "cantidad": cantidad,
                "subtotal": subtotal
            })
            total += subtotal

    return render(request, "catalogo/carrito.html", {"items": items, "total": total})



# Carrito: confirmar compra
def confirmar_compra(request):
    herramientas = cargar_herramientas()
    carrito = request.session.get("carrito", {})
    mensajes = []

    for id, cantidad in carrito.items():
        herramienta = next((h for h in herramientas if h["id"] == int(id)), None)
        if herramienta:
            if herramienta["stock"] >= cantidad:
                herramienta["stock"] -= cantidad
                mensajes.append(f"Compra realizada: {herramienta['nombre']} x{cantidad}")
            else:
                mensajes.append(f"No hay stock suficiente de {herramienta['nombre']}")

    guardar_herramientas(herramientas)  # 🔹 guarda los cambios en el JSON
    request.session["carrito"] = {}  # vacía el carrito

    return render(request, "catalogo/confirmacion.html", {"mensajes": mensajes})

def eliminar_del_carrito(request, id):
    carrito = request.session.get("carrito", {})
    id_str = str(id)

    if id_str in carrito:
        if carrito[id_str] > 1:
            carrito[id_str] -= 1  # 🔹 resta una unidad
        else:
            del carrito[id_str]   # 🔹 elimina el producto si llega a 0
        request.session["carrito"] = carrito

    return redirect("ver_carrito")


def cancelar_compra(request):
    request.session["carrito"] = {}
    return redirect("ver_carrito")
