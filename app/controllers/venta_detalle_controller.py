from app.models import DetalleVenta
from app.extensions import db

# Funciones para gestionar los detalles de venta

#obtener todos los detalles de venta
def get_all_detalle_ventas():
    try:
        detalle_venta = DetalleVenta.query.all()

        detalles = []
        for detalle in detalle_venta:
            detalles.append({
                "detalle_venta_id" : detalle.detalle_venta_id,
                "venta_id" : detalle.venta_id,
                "producto_id" : detalle.producto_id,
                "cantidad" : detalle.cantidad,
                "precio" : detalle.precio,
                "total" : detalle.total,
            })

        return detalles , 200
    except Exception as e:
        return f'Error: {str(e)}', 500
    
#obtener detalle de venta por id
def get_detalle_venta_by_id(id):
    try:
        detalle_venta = DetalleVenta.query.get(id)
        if detalle_venta:
            return {
                "detalle_venta" : {
                    "detalle_venta_id" : detalle_venta.detalle_venta_id,
                    "venta_id" : detalle_venta.venta_id,
                    "producto_id" : detalle_venta.producto_id,
                    "cantidad" : detalle_venta.cantidad,
                    "precio" : detalle_venta.precio,
                    "total" : detalle_venta.total,
                }
            }, 200
        else:
            return {'message' : 'Detalle de venta no encontrado'}, 404
    except Exception as e:
        return f'Error: {str(e)}', 500

#crear un detalle de venta
def create_detalle_venta(detalle_venta):
    try:
        new_detalle_venta = DetalleVenta(
            venta_id = detalle_venta['venta_id'],
            producto_id = detalle_venta['producto_id'],
            cantidad = detalle_venta['cantidad'],
            precio = detalle_venta['precio'],
            total = detalle_venta['total'],
        )
        db.session.add(new_detalle_venta)
        db.session.commit()
        return {
            "message" : "Detalle de venta creado exitosamente",
            "detalle_venta" : {
                "detalle_venta_id" : new_detalle_venta.detalle_venta_id,
                "venta_id" : new_detalle_venta.venta_id,
                "producto_id" : new_detalle_venta.producto_id,
                "cantidad" : new_detalle_venta.cantidad,
                "precio" : new_detalle_venta.precio,
                "total" : new_detalle_venta.total,
            }
        }, 201
    except Exception as e:
        return f'Error: {str(e)}', 500

#actualizar un detalle de venta
def update_detalle_venta(id, detalle_venta):
    try:
        detalle_venta_db = DetalleVenta.query.get(id)
        if not detalle_venta_db:
            return {'message' : 'Detalle de venta no encontrado'}, 404
        
        detalle_venta_db.venta_id = detalle_venta['venta_id']
        detalle_venta_db.producto_id = detalle_venta['producto_id']
        detalle_venta_db.cantidad = detalle_venta['cantidad']
        detalle_venta_db.precio = detalle_venta['precio']
        detalle_venta_db.total = detalle_venta['total']

        db.session.add(detalle_venta_db)
        db.session.commit()
        return {
            "detalle_venta" : {
                "venta_id" : detalle_venta_db.venta_id,
                "producto_id" : detalle_venta_db.producto_id,
                "cantidad" : detalle_venta_db.cantidad,
                "precio" : detalle_venta_db.precio,
                "total" : detalle_venta_db.total,
            }
        }, 200
    except Exception as e:
        return f'Error: {str(e)}', 500

# eliminar un detalle de venta
def delete_detalle_venta(id):
    try:
        detalle_venta_db = DetalleVenta.query.get(id)
        if not detalle_venta_db:
            return {'message' : 'Detalle de venta no encontrado'}, 404
        
        db.session.delete(detalle_venta_db)
        db.session.commit()
        return {'message' : 'Detalle de venta eliminado'}, 200
    except Exception as e:
        return f'Error: {str(e)}', 500
