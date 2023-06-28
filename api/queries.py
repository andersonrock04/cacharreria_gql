import graphene
from graphql_jwt.decorators import login_required
from .types import *
from .models import *


class Query(graphene.ObjectType):
    proveedor = graphene.Field(ProveedorType, id=graphene.ID())

    @login_required
    def resolve_proveedor(self, info, id):
        try:
            proveedor = Proveedor.objects.get(pk=id)
        except Proveedor.DoesNotExist:
            return Proveedor.objects.none()
        if proveedor.usuario.id != info.context.user.id:
            return Proveedor.objects.none()
        return proveedor

    proveedores = graphene.List(ProveedorType)

    @login_required
    def resolve_proveedores(self, info):
        return Proveedor.objects.filter(usuario=info.context.user.id)


    categoria_insumo = graphene.Field(CategoriaInsumoType, id=graphene.ID(required=True))

    @login_required
    def resolve_categoria_insumo(self, info, id):
        try:
            categoria = CategoriaInsumo.objects.get(pk=id)
        except CategoriaInsumo.DoesNotExist:
            return CategoriaInsumo.objects.none()
        if categoria.usuario.id != info.context.user.id:
            return CategoriaInsumo.objects.none()
        return categoria

    categorias_insumos = graphene.List(CategoriaInsumoType)

    @login_required
    def resolve_categorias_insumos(self, info):
        return CategoriaInsumo.objects.filter(usuario=info.context.user)


    insumo = graphene.Field(InsumoType, id=graphene.ID())

    @login_required
    def resolve_insumo(self, info, id):
        try:
            insumo = Insumo.objects.get(pk=id)
        except Insumo.DoesNotExist:
            return Insumo.objects.none()
        if insumo.usuario.id != info.user.id:
            return Insumo.objects.none()
        return insumo

    insumos = graphene.List(InsumoType)

    @login_required
    def resolve_insumos(self, info):
        return Insumo.objects.filter(usuario=info.context.user.id)


    categoria = graphene.Field(CategoriaType, id=graphene.ID())

    @login_required
    def resolve_categoria(self, info, id):
        try:
            categoria = Categoria.objects.get(pk=id)
        except Categoria.DoesNotExist:
            return Categoria.objects.none()
        if categoria.usuario.id != info.user.id:
            return Categoria.objects.none()
        return categoria

    categorias = graphene.List(CategoriaType)

    @login_required
    def resolve_categorias(self, info):
        return Categoria.objects.filter(usuario=info.user.id)


    producto = graphene.Field(ProductoType, id=graphene.ID())

    @login_required
    def resolve_producto(self, info, id):
        try:
            producto = Producto.objects.get(pk=id)
        except Producto.DoesNotExist:
            return Producto.objects.none()
        if producto.usuario.id != info.user.id:
            return Producto.objects.none()
        return producto

    productos = graphene.List(ProductoType)

    login_required
    def resolve_productos(self, info):
        return Producto.objects.filter(usuario=info.user.id)

