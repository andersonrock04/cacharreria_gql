import graphene
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required
import graphql_jwt
from django.contrib.auth.models import User
from .types import *
from .models import *


class ProveedorMutation(graphene.Mutation):
    proveedor = graphene.Field(ProveedorType)

    class Arguments:
        nombre = graphene.String(required=True)
        telefono = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, nombre, telefono):
        proveedor = Proveedor.objects.create(usuario=info.context.user, nombre=nombre, telefono=telefono)
        proveedor.save()
        return cls(proveedor=proveedor)


class ProveedorUpdate(graphene.Mutation):
    proveedor = graphene.Field(ProveedorType)

    class Arguments:
        id = graphene.ID()
        nombre = graphene.String()
        telefono = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        try:
            proveedor = Proveedor.objects.get(pk=id)
        except Proveedor.DoesNotExist:
            return Proveedor.objects.none()
        if proveedor.usuario.id != info.context.user.id:
            return Proveedor.objects.none()
        nombre = kwargs.get('nombre')
        if nombre is not None:
            proveedor.nombre = nombre
        telefono = kwargs.get('telefono')
        if telefono is not None:
            proveedor.telefono = telefono
        proveedor.save()
        return cls(proveedor=proveedor)


class ProveedorDelete(graphene.Mutation):
    eliminacion_efectuada = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            proveedor = Proveedor.objects.get(pk=id)
        except Proveedor.DoesNotExist:
            return cls(eliminacion_efectuada=False)
        if proveedor.usuario.id != info.context.user.id:
            return cls(eliminacion_efectuada=False)
        proveedor.delete()
        return cls(eliminacion_efectuada=True)


class CategoriaInsumoMutation(graphene.Mutation):
    categoria_insumo = graphene.Field(CategoriaInsumoType)

    class Arguments:
        nombre = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, nombre):
        categoria_insumo = CategoriaInsumo.objects.create(usuario=info.context.user, nombre=nombre)
        categoria_insumo.save()
        return cls(categoria_insumo=categoria_insumo)


class CategoriaInsumoUpdate(graphene.Mutation):
    categoria_insumo = graphene.Field(CategoriaInsumoType)

    class Arguments:
        id = graphene.ID()
        nombre = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, id,nombre):
        try:
            categoria_insumo = CategoriaInsumo.objects.get(pk=id)
        except CategoriaInsumo.DoesNotExist:
            return CategoriaInsumo.objects.none()
        if categoria_insumo.usuario.id != info.context.user.id:
            return CategoriaInsumo.objects.none()
        categoria_insumo.nombre = nombre
        categoria_insumo.save()
        return cls(categoria_insumo=categoria_insumo)


class CategoriaInsumoDelete(graphene.Mutation):
    eliminacion_efectuada = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            categoria_insumo = CategoriaInsumo.objects.get(pk=id)
        except CategoriaInsumo.DoesNotExist:
            return cls(eliminacion_efectuada=False)
        if categoria_insumo.usuario.id != info.context.user.id:
            return cls(eliminacion_efectuada=False)
        categoria_insumo.delete()
        return cls(eliminacion_efectuada=True)


class InsumoMutation(graphene.Mutation):
    insumo = graphene.Field(InsumoType)

    class Arguments:
        proveedor = graphene.Int(required=True)
        nombre = graphene.String(required=True)
        categoria = graphene.Int(required=True)
        stock = graphene.Int(required=True)
        stock_minimo = graphene.Int(required=True)
        unidades_paquete = graphene.Int(required=True)
        costo_unidad = graphene.Float(required=True)
        unidad_peso = graphene.String()
        peso = graphene.Float()
        unidad_medida = graphene.String()
        largo = graphene.Float()
        alto = graphene.Float()

    @classmethod
    @login_required
    def mutate(cls, root, info, proveedor, nombre, categoria, stock, stock_minimo, unidades_paquete, costo_unidad, **kwargs):
        try:
            proveedor_relacionado = Proveedor.objects.get(pk=proveedor)
            categoria_relazionada = CategoriaInsumo.objects.get(pk=categoria)
        except (Proveedor.DoesNotExist, CategoriaInsumo.DoesNotExist):
            return Insumo.objects.none()
        if proveedor_relacionado.usuario.id != info.context.user.id or categoria_relazionada.usuario.id != info.context.user.id:
            return Insumo.objects.none()
        insumo = Insumo.objects.create(
            usuario = info.context.user,
            proveedor=proveedor_relacionado,
            categoria=categoria_relazionada,
            nombre=nombre,
            stock=stock,
            stock_minimo=stock_minimo,
            unidades_paquete=unidades_paquete,
            costo_unidad=costo_unidad)
        unidad_peso = kwargs.get('unidad_peso')
        if unidad_peso is not None:
            insumo.unidad_peso = unidad_peso
        unidad_medida = kwargs.get('unidad_medida')
        if unidad_medida is not None:
            insumo.unidad_medida = unidad_medida
        largo = kwargs.get('largo')
        if largo is not None:
            insumo.largo = largo
        alto = kwargs.get('alto')
        if alto is not None:
            insumo.alto = alto
        insumo.save()
        return cls(insumo=insumo)


class InsumoUpdate(graphene.Mutation):
    insumo = graphene.Field(InsumoType)

    class Arguments:
        id = graphene.ID()
        proveedor = graphene.Int()
        nombre = graphene.String()
        categoria = graphene.Int()
        stock = graphene.Int()
        stock_minimo = graphene.Int()
        unidades_paquete = graphene.Int()
        costo_unidad = graphene.Float()
        unidad_peso = graphene.String()
        peso = graphene.Float()
        unidad_medida = graphene.String()
        largo = graphene.Float()
        alto = graphene.Float()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        try:
            insumo = Insumo.objects.get(pk=id)
        except Insumo.DoesNotExist:
            return Insumo.objects.none()
        if insumo.usuario.id != info.context.user.id:
            return Insumo.objects.none()
        proveedor = kwargs.get('proveedor')
        if proveedor is not None:
            try:
                proveedor_relacionado = Proveedor.objects.get(pk=proveedor)
            except Proveedor.DoesNotExist:
                return Insumo.objects.none()
            if proveedor_relacionado.usuario.id != info.context.user.id:
                return Insumo.objects.none()
            insumo.proveedor = proveedor_relacionado
        categoria = kwargs.get('categoria')
        if categoria is not None:
            try:
                categoria_relacionada = CategoriaInsumo.objects.get(pk=categoria)
            except CategoriaInsumo.DoesNotExist:
                return CategoriaInsumo.objects.none()
            if categoria_relacionada.usuario.id != info.context.user.id:
                return Insumo.objects.none()
            insumo.categoria = categoria_relacionada
        nombre = kwargs.get('nombre')
        if nombre is not None:
            insumo.nombre=nombre
        stock = kwargs.get('stock')
        if stock is not None:
            insumo.stock=stock
        stock_minimo = kwargs.get('stock_minimo')
        if stock_minimo is not None:
            insumo.stock_minimo=stock_minimo
        unidades_paquete = kwargs.get('unidades_paquete')
        if unidades_paquete is not None:
            insumo.unidades_paquete=unidades_paquete
        costo_unidad = kwargs.get('costo_unidad')
        if costo_unidad is not None:
            insumo.costo_unidad=costo_unidad
        unidad_peso = kwargs.get('unidad_peso')
        if unidad_peso is not None:
            insumo.unidad_peso=unidad_peso
        peso = kwargs.get('peso')
        if peso is not None:
            insumo.peso=peso
        unidad_medida = kwargs.get('unidad_medida')
        if unidad_medida is not None:
            insumo.unidad_medida=unidad_medida
        largo = kwargs.get('largo')
        if largo is not None:
            insumo.largo=largo
        alto = kwargs.get('alto')
        if alto is not None:
            insumo.alto=alto
        insumo.save()
        return cls(insumo=insumo)


class InsumoDelete(graphene.Mutation):
    eliminacion_efectuada = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            insumo = Insumo.objects.get(id=id)
        except Insumo.DoesNotExist:
            return cls(eliminacion_efectuada=False)
        if insumo.usuario.id != info.context.user.id:
            return cls(eliminacion_efectuada=False)
        insumo.delete()
        return cls(eliminacion_efectuada=True)


class CategoriaMutation(graphene.Mutation):
    categoria = graphene.Field(CategoriaType)

    class Arguments:
        categoria_principal = graphene.Int()
        nombre = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        imagen = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, nombre, descripcion, **kwargs):
        categoria = Categoria.objects.create(usuario=info.context.user, nombre=nombre, descripcion=descripcion)
        categoria_principal = kwargs.get('categoria_principal')
        if categoria_principal is not None:
            try:
                categoria_relacionada = Categoria.objects.get(pk=categoria_principal)
            except Categoria.DoesNotExist:
                return Categoria.objects.none()
            if categoria_relacionada.usuario.id != info.context.user.id:
                return Categoria.objects.none()
            categoria.categoria_principal = categoria_relacionada
        imagen = kwargs.get('imagen')
        if imagen is not None:
            categoria.imagen = imagen
        categoria.save()
        return cls(categoria=categoria)


class CategoriaUpdate(graphene.Mutation):
    categoria = graphene.Field(CategoriaType)

    class Arguments:
        id = graphene.ID()
        nombre = graphene.String()
        descripcion = graphene.String()
        categoria_principal = graphene.Int()
        imagen = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        try:
            categoria = Categoria.objects.get(pk=id)
        except categoria.DoesNotExist:
            return Categoria.objects.none()
        if categoria.usuario.id != info.context.user.id:
            return Categoria.objects.none()
        categoria_principal = kwargs.get('categoria_principal')
        if categoria_principal is not None:
            try:
                categoria_relacionada = Categoria.objects.get(pk=categoria_principal)
            except Categoria.DoesNotExist:
                return Categoria.objects.none()
            if categoria_relacionada.usuario.id != info.context.user.id:
                return Categoria.objects.none()
            categoria.categoria_principal = categoria_relacionada
        nombre = kwargs.get('nombre')
        if nombre is not None:
            categoria.nombre = nombre
        descripcion = kwargs.get('descripcion')
        if descripcion is not None:
            categoria.descripcion = descripcion
        imagen = kwargs.get('imagen')
        if imagen is not None:
            categoria.imagen = imagen
        categoria.save()
        return cls(categoria=categoria)


class CategoriaDelete(graphene.Mutation):
    eliminacion_efectuada = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            categoria = Categoria.objects.get(pk=id)
        except Categoria.DoesNotExist:
            return cls(eliminacion_efectuada=False)
        if categoria.usuario.id != info.context.user.id:
            return cls(eliminacion_efectuada=False)
        categoria.delete()
        return cls(eliminacion_efectuada=True)


class ProductoMutation(graphene.Mutation):
    producto = graphene.Field(ProductoType)

    class Arguments:
        categoria = graphene.Int(required=True)
        proveedor = graphene.Int(required=True)
        nombre = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        stock = graphene.Int(required=True)
        stock_minimo = graphene.String(required=True)
        precio_unitario = graphene.Float(required=True)
        costo_unitario = graphene.Float(required=True)
        imagen1 = Upload(required=True)
        imagen2 = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, categoria, nombre, descripcion, stock, stock_minimo, costo_unitario, precio_unitario, imagen1, imagen2=None):
        try:
            categoria_relacionada = Categoria.objects.get(pk=categoria)
            proveedor_relacionado = Proveedor.objects.get(pk=proveedor)
        except (Categoria.DoesNotExist, Producto.DoesNotExist):
            return Producto.objects.none()
        if categoria_relacionada.usuario.id != info.context.user.id or proveedor_relacionado.usuario.id != info.context.user.id:
            return Producto.objects.none()
        producto = Producto.objects.create(usuario=info.context.info.user,
            categoria=categoria_relacionada,
            proveedor=proveedor_relacionado,
            nombre=nombre,
            descripcion = descripcion,
            stock = stock,
            stock_minimo = stock_minimo,
            costo_unitario = costo_unitario,
            precio_unitario = precio_unitario,
            imagen1 = imagen1,
            imagen2 = imagen2)
        producto.save()
        return cls(producto=producto)


class ProductoUpdate(graphene.Mutation):
    producto = graphene.Field(ProductoType)

    class Arguments:
        id = graphene.ID()
        categoria = graphene.Int()
        proveedor = graphene.Int()
        nombre = graphene.String()
        descripcion = graphene.String()
        stock = graphene.Int()
        stock_minimo = graphene.String()
        precio_unitario = graphene.Float()
        costo_unitario = graphene.Float()
        imagen1 = Upload()
        imagen2 = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        try:
            producto = Producto.objects.get(pk=id)
        except Producto.DoesNotExist:
            return Producto.objects.none()
        if producto.usuario.id != info.context.user.id:
            return Producto.objects.none()
        categoria = kwargs.get('categoria')
        if categoria is not None:
            try:
                categoria_relacionada = Categoria.objects.get(pk=categoria)
            except Categoria.DoesNotExist:
                return Producto.objects.none()
            if categoria_relacionada.usuario.id != info.context.user.id:
                return Producto.objects.none()
            producto.categoria = categoria_relacionada
        proveedor = kwargs.get('proveedor')
        if provedor is not None:
            try:
                producto.proveedor = Proveedor.objects.get(pk=proveedor)
            except Proveedor.DoesNotExist:
                return Producto.objects.none()
            if proveedor_relacionado.usuario.id != info.context.id:
                return Producto.objects.none()
            producto.proveedor = proveedor_relacionado
        nombre = kwargs.get('nombre')
        if nombre is not None:
            producto.nombre = nombre
        descripcion = kwargs.get('descripcion')
        if descripcion is not None:
            producto.descripcion = descripcion
        stock = kwargs.get('stock')
        if stock is not None:
            producto.stock = stock
        stock_minimo = kwargs.get('stock_minimo')
        if stock_minimo is not None:
            producto.stock_minimo = stock_minimo
        costo_unitario = kwargs.get('costo_unitario')
        if costo_unitario is not None:
            producto.costo_unitario = costo_unitario
        precio = kwargs.get('precio')
        if precio is not None:
            producto.precio_unitario = precio_unitario
        imagen1 = kwargs.get('imagen1')
        if imagen1 is not None:
            producto.imagen1 = imagen1
        imagen2 = kwargs.get('imagen2')
        if imagen2 is not None:
            producto.imagen2 = imagen2
        producto.save()
        return cls(producto=producto)


class ProductoDelete(graphene.Mutation):
    eliminacion_efectuada = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        try:
            producto = Producto.objects.get(pk=id)
        except Producto.DoesNotExist:
            return Producto.objects.none()
        producto.delete()
        return cls(eliminacion_efectuada=True)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    guardar_proveedor = ProveedorMutation.Field()
    actualizar_proveedor = ProveedorUpdate.Field()
    eliminar_proveedor = ProveedorDelete.Field()

    guardar_categoria_insumo = CategoriaInsumoMutation.Field()
    actualizar_categoria_insumo = CategoriaInsumoUpdate.Field()
    eliminar_categoria_insumo = CategoriaInsumoDelete.Field()

    guardar_insumo = InsumoMutation.Field()
    actualizar_insumo = InsumoUpdate.Field()
    eliminar_insumo = InsumoDelete.Field()

    guardar_categoria = CategoriaMutation.Field()
    actualizar_categoria = CategoriaUpdate.Field()
    eliminar_categoria = CategoriaDelete.Field()

    guardar_producto = ProductoMutation.Field()
    actualizar_producto = ProductoUpdate.Field()
    eliminar_producto = ProductoDelete.Field()
