from django.db import models
from django.contrib.auth.models import User


class Proveedor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class CategoriaInsumo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaInsumo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    stock = models.PositiveBigIntegerField()
    stock_minimo = models.PositiveIntegerField()
    unidades_paquete = models.PositiveIntegerField()
    costo_unidad = models.DecimalField(max_digits=15, decimal_places=3)
    unidad_peso = models.CharField(max_length=50, null=True, blank=True)
    peso = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    unidad_medida = models.CharField(max_length=50, null=True, blank=True)
    largo = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    alto = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria_principal = models.ForeignKey('Categoria', models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='categorias_imagenes', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    stock = models.PositiveBigIntegerField()
    stock_minimo = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=13, decimal_places=3)
    precio_unitario = models.DecimalField(max_digits=13, decimal_places=3)
    imagen1 = models.ImageField(upload_to='productos_imagenes')
    imagen2 = models.ImageField(upload_to='productos_imagenes', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Operador(models.Model):
    operador = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cuenta_operador')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.operador.username

