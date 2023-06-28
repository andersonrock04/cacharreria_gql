import graphene
from graphene_django import DjangoObjectType
from .models import *


class CategoriaInsumoType(DjangoObjectType):
    class Meta:
        model = CategoriaInsumo
        fields = '__all__'


class ProveedorType(DjangoObjectType):
    class Meta:
        model = Proveedor
        fields = '__all__'


class InsumoType(DjangoObjectType):
    class Meta:
        model = Insumo
        fields = '__all__'


class CategoriaType(DjangoObjectType):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoType(DjangoObjectType):
    class Meta:
        model = Producto
        fields = '__all__'

