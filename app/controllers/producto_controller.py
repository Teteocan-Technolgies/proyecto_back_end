from app.models import Productos
from app.extensions import db


## Retornar una lista de todos los productos
def get_all_productos():
    try:
        productos = Productos.query.filter(Productos.baja == False).all()
        return {
            "productos": [
                {
                    "producto_id": producto.producto_id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "baja": producto.baja,
                }
                for producto in productos
            ]
        }, 201
    except Exception as e:
        return {"error": str(e)}, 500  

#Retornar un producto por su ID
def get_producto_by_id(id):
    try:
        producto = Productos.query.get(id)
        return {
            "producto" : {
                "prodicto_id" : producto.producto_id,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock": producto.stok,
                "baja": producto.baja,
            }
        }
    except Exception as e:
        return {"error": str(e)}, 500  
    
# Crear un nuevo producto
def create_producto(data):
    try:
        nuevo_producto = Productos(
            nombre = data['nombre'],
            descripcion = data['descripcion'],
            precio = data['precio'],
            stock = data['stock'],
            baja = False
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return {
            "message" : "Producto registrado",
            "producto": {
                "nombre": nuevo_producto.nombre,
                "descripcion": nuevo_producto.descripcion,
                "precio": nuevo_producto.precio,
                "stock": nuevo_producto.stock,
            }
        }, 201
    except Exception as e:
        return {"error": str(e)}, 500  
    
# Actualizar un producto por su ID
def update_producto(id, data):
    try:
        producto = Productos.query.get(id)
        if not producto:
            return {'error': 'Producto no encontrado'}, 404
        else:
            producto.nombre = data['nombre']
            producto.descripcion = data['descripcion']
            producto.precio = data['precio']
            producto.stock = data['stock']
            
            db.session.add(producto)
            db.session.commit()
            return {
                "message": "Producto actualizado",
                "producto": {
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                }
            }, 200
    except Exception as e:
        return {"error": str(e)}, 500  

# Eliminar un producto por su ID
def delete_producto(id):
    try:
        producto = Productos.query.get(id)        
        if not producto:
            return {'error': 'Producto no encontrado'}, 404
        else:
            db.session.delete(producto)
            db.session.commit()
            return {
                "message": "Producto dado de baja"
            }, 200
    except Exception as e:
        db.session.rollback()  # En caso de error, revertir cualquier cambio
        return {"error": "Error interno del servidor. Detalles: " + str(e)}, 500 
