from datetime import datetime, date
from app.models import Ventas, DetalleVenta, Productos
from app.extensions import db
from sqlalchemy import func

# Retornar una lista de las ventas
def get_all_ventas():
    try:
        ventas = Ventas.query.all()
        ventas_data = [{
            "venta_id": v.venta_id,
            "usuario_id": v.usuario_id,
            "fecha": v.fecha.isoformat() if v.fecha else None,
            "total": float(v.total),
            "cantidad_art": v.cantidad_art
        } for v in ventas]
        return ventas_data, 200  # (data, status)
    except Exception as e:
        return {"error": str(e)}, 500
    

# Retornar una venta por su ID
def get_venta_by_id(venta_id):
    try:
        venta = Ventas.query.get(venta_id)
        if not venta:  # Manejar caso cuando la venta no existe
            return {"error": "Venta no encontrada"}, 404
        
        return {
            "venta_id": venta.venta_id,
            "usuario_id": venta.usuario_id,
            "fecha": venta.fecha.isoformat() if venta.fecha else None,
            "total": float(venta.total),
            "cantidad_art": venta.cantidad_art
        }, 200  # Ahora retorna (data, status) siempre
    except Exception as e:
        return {"error": str(e)}, 500

#obtener todas las ventas por el ID del cliente
def get_ventas_by_cliente_id(usuario_id):
    try:
        ventas = Ventas.query.filter_by(usuario_id=usuario_id).all()
        if not ventas:  # Manejar caso cuando la venta no existe
            return {"error" : "No tiene ventas registradas"}, 200
        ventas_data = [{
            "venta_id": v.venta_id,
            "usuario_id": v.usuario_id,
            "fecha": v.fecha.isoformat() if v.fecha else None,
            "total": float(v.total),
            "cantidad_art": v.cantidad_art
        } for v in ventas]
        return ventas_data, 200
    except Exception as e:
        return {"error": str(e)}


# Crear una nueva venta
def create_venta(venta_data):
    try:
        venta = Ventas(
            venta_id = venta_data["venta_id"],
            usuario_id = venta_data["usuario_id"],
            cantidad_art = venta_data["cantidad_art"],
            total = venta_data["total"],
            fecha = venta_data["fecha"],
        )
        db.session.add(venta)
        db.session.commit()
        return {
            "message": "Venta creada con éxito",
            "venta" : {
                "venta_id": venta.venta_id,
                "usuario_id": venta.usuario_id,
                "fecha": venta.fecha.isoformat() if venta.fecha else None,
                "total": float(venta.total),
                "cantidad_art": venta.cantidad_art
            }
            }, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Actualizar una venta por su ID
def update_venta(venta_id, venta_data):
    try:
        venta = Ventas.query.get(venta_id)
        if not venta:
            return {"error": "Venta no encontrada"}, 500
        
        venta.venta_id = venta_data["venta_id"]
        venta.usuario_id = venta_data["usuario_id"]
        venta.cantidad_art = venta_data["cantidad_art"]
        venta.total = venta_data["total"]
        venta.fecha = venta_data["fecha"]
        db.session.commit()
        return {
            "message": "Venta actualizada con éxito",
            "venta": {
                "venta_id": venta.venta_id,
                "usuario_id": venta.usuario_id,
                "cantidad_art": venta.cantidad_art,
                "total": venta.total,
                "fecha": venta.fecha
            }
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
# Eliminar una venta por su ID
def delete_venta(venta_id):
    try:
        venta = Ventas.query.get(venta_id)
        if not venta:
            return {"error": "Venta no encontrada"}, 500
        
        db.session.delete(venta)
        db.session.commit()
        return {"message": "Venta eliminada con éxito"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
# Obtener estadísticas de ventas por mes
def get_estadisticas_ventas():
    print('Estadísticas de ventas por mes')
    try:
        current_year = datetime.now().year
        result = []
        
        for month in range(1, 13):
            # Usa date() en lugar de datetime()
            start_date = date(year=current_year, month=month, day=1)
            end_date = date(
                year=current_year,
                month=month,
                day=28 if month == 2 else 30 if month in [4,6,9,11] else 31
            )
            
            ventas_mes = Ventas.query.filter(
                Ventas.fecha >= start_date,
                Ventas.fecha <= end_date
            ).all()
            
            if not ventas_mes:
                # Si no hay ventas en el mes, agregar objeto vacío
                result.append({
                    "productos_mas_vendidos": [],
                    "productos_menos_vendidos": [],
                    "ventas_totales_mes": {
                        "mes": f"{current_year}-{month:02d}",
                        "total_ventas": 0,
                        "total_transacciones": 0
                    }
                })
                continue
            
            # Calcular totales del mes
            total_ventas = sum(venta.total for venta in ventas_mes)
            total_transacciones = len(ventas_mes)
            
            # Obtener productos más y menos vendidos (requiere relación con DetalleVenta)
            productos_mas_vendidos = db.session.query(
                DetalleVenta.producto_id,
                Productos.nombre,
                func.sum(DetalleVenta.cantidad).label('total_vendidos')
            ).join(Productos).filter(
                DetalleVenta.venta_id.in_([v.venta_id for v in ventas_mes])
            ).group_by(DetalleVenta.producto_id, Productos.nombre
            ).order_by(func.sum(DetalleVenta.cantidad).desc()
            ).limit(5).all()
            
            productos_menos_vendidos = db.session.query(
                DetalleVenta.producto_id,
                Productos.nombre,
                func.sum(DetalleVenta.cantidad).label('total_vendidos')
            ).join(Productos).filter(
                DetalleVenta.venta_id.in_([v.venta_id for v in ventas_mes])
            ).group_by(DetalleVenta.producto_id, Productos.nombre
            ).order_by(func.sum(DetalleVenta.cantidad).asc()
            ).limit(5).all()
            
            # Formatear resultados
            result.append({
                "productos_mas_vendidos": [
                    {
                        "producto_id": p.producto_id,
                        "nombre": p.nombre,
                        "total_vendidos": p.total_vendidos
                    } for p in productos_mas_vendidos
                ],
                "productos_menos_vendidos": [
                    {
                        "producto_id": p.producto_id,
                        "nombre": p.nombre,
                        "total_vendidos": p.total_vendidos
                    } for p in productos_menos_vendidos
                ],
                "ventas_totales_mes": {
                    "mes": f"{current_year}-{month:02d}",
                    "total_ventas": round(total_ventas, 2),
                    "total_transacciones": total_transacciones
                }
            })
            
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500