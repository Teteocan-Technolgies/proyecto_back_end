from dotenv import load_dotenv
from google import genai
import os
from flask import Flask, request, jsonify
from google.genai import types
from ..controllers.venta_controller import get_estadisticas_ventas  # ✅ Nombre original del controlador

load_dotenv()
api_key = 'AIzaSyCRcJxhvCHlho2GHmmQcKSpo9UInH1Q3A0'

# Función para obtener datos dinámicos de ventas
def obtener_datos_ventas(data):
    try:
        # Obtener estadísticas desde el controlador SIN MODIFICAR NOMBRES
        response, status = get_estadisticas_ventas()  # ✅ Función original
        if status != 200:
            raise Exception("Error al obtener estadísticas")

        # Procesar datos respetando claves originales
        productos_mas_vendidos = {}
        productos_menos_vendidos = {}
        ventas_totales_mensuales = {}
        totales_anuales = {}

        # Mapeo de meses (para mantener compatibilidad con datos estáticos previos)
        nombres_meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

        # Acumular datos anuales y mensuales
        for mes_data in response:
            # Extraer datos con claves originales del controlador ✅
            ventas_mes = mes_data['ventas_totales_mes']  # Clave original
            mes_num = int(ventas_mes['mes'].split('-')[1])
            nombre_mes = nombres_meses[mes_num]
            
            # Ventas mensuales
            ventas_totales_mensuales[nombre_mes] = ventas_mes['total_ventas']  # Clave original
            
            # Productos más vendidos (acumulación anual)
            for producto in mes_data['productos_mas_vendidos']:  # Clave original
                nombre = producto['nombre']  # Clave original
                totales_anuales[nombre] = totales_anuales.get(nombre, 0) + producto['total_vendidos']  # Clave original

        # Ordenar productos
        sorted_productos = sorted(totales_anuales.items(), key=lambda x: x[1], reverse=True)
        productos_mas_vendidos = dict(sorted_productos[:5])
        productos_menos_vendidos = dict(sorted_productos[-5:]) if len(sorted_productos) >=5 else {}
        
        datos_totales_usario = {
            'productos_mas_vendidos': productos_mas_vendidos,
            'productos_menos_vendidos': productos_menos_vendidos,
            'ventas_totales_anuales': sum(totales_anuales.values()),  # Sumar totales anuales
            'ventas_totales_mensuales': ventas_totales_mensuales,
        }

        return datos_totales_usario
    except Exception as e:
        print(f"Error en obtener_datos_ventas: {e}")
        return {}


#iniciado del bot
def chat_bot(data, datos_totales_usario):
    try:
        # Crear cliente con la API key
        cliente = genai.Client(api_key=api_key)
        
        # Generar contenido con el modelo
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            
            contents=f"""
            # Asistente Analítico de Ventas Empresariales
            
            
            Eres un analista avanzado de datos de ventas con experiencia en business intelligence. Tu objetivo es proporcionar
            análisis precisos y accionables basados en los datos disponibles para apoyar la toma de decisiones estratégicas.
            
            -recuerda agregar emojis a la respuesta para que sea mas amigable y entendible para el usuario
            
            -Inegociable, no debes dar tantos renglones y la respuesta debe ser corta y concisa, no te extiendas tanto en la respuesta.


            ## Conjuntos de Datos Disponibles:
            - Datos generales de ventas
            - Top 5 productos de mayor rendimiento
            - Top 5 productos de menor rendimiento
            - Ventas totales anuales
            - Ventas totales mensuales

            ## Directrices para el Análisis:
            - Identifica tendencias claras y patrones significativos en los datos
            - Destaca correlaciones importantes entre diferentes métricas
            - Calcula KPIs relevantes cuando sea aplicable (tasa de crecimiento, ganancias, etc.)
            - Segmenta el análisis por períodos de tiempo cuando sea útil
            - Proporciona contexto empresarial para los hallazgos estadísticos

            ## Formato de Respuesta:
            1. Resumen ejecutivo breve (1-2 oraciones)
            2. Análisis detallado basado en los datos relevantes
            3. 2-3 recomendaciones accionables cuando sea apropiado
            4. Sugerencias sobre qué métricas monitorear en el futuro

            Si no dispones de suficientes datos para responder con precisión, indica qué información adicional
            sería necesaria para un análisis más completo.
            
            
            -Datos empresariales: {get_estadisticas_ventas} y {datos_totales_usario}
            -Utiliza exclusivamente estos datos como base para tus análisis y conclusiones.

            Consulta del usuario: "{data["consulta"]}"
            
            -optimaza la resputa para que sea entendible para el usuario, no utilices tecnisismos ni palabras complicadas.
            -Recuerda que la respusta debe ser sencilla y corta para que el usuario pueda entenderla sin problemas.
            
            
            """,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1000))
        ),

        
        mensaje = respuesta [0].text       
        return {'success':True, 'data': mensaje}
    except Exception as e:
        print(f"Error al generar mensaje: {e}")
        return {'success': False, 'data': "No se pudo generar."}


#print(chat_bot())



#Respuesta del bot y endpoint de la api


#@app.route('/api/chatbot', methods=['POST'])


def procesar_consulta_chatbot(data):
    try:
        data = request.get_json()
        
        # Validar la entrada
        if not data or 'consulta' not in data:
            return {"error": "Falta el campo 'consulta' en el cuerpo de la solicitud"}, 400
            
        # Obtener respuesta del chatbot con la consulta del usuario
        mensaje = chat_bot(data['consulta'])
        
        return {
            "exito": True,
            "respuesta": mensaje,
        }, 200
        
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }, 500



#endpoint muestra
"""""
def create_producto():
    data = request.get_json()
    producto, status_code = producto_controller.create_producto(data)
    return jsonify(producto), status_code
    
"""