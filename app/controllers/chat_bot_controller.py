from dotenv import load_dotenv
from google import genai
import os
from flask import Flask, request, jsonify
from google.genai import types
from ..controllers.venta_controller import get_estadisticas_ventas  # ✅ Nombre original del controlador

load_dotenv()
api_key = 'AIzaSyCRcJxhvCHlho2GHmmQcKSpo9UInH1Q3A0'

# Función para obtener datos dinámicos de ventas
def obtener_datos_ventas(data, get_estadisticas_ventas):
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
        
        #Almacenar los datos en un diccionario
        datos_ventas = {
            'productos_mas_vendidos': productos_mas_vendidos,
            'productos_menos_vendidos': productos_menos_vendidos,
            'ventas_totales_mensuales': ventas_totales_mensuales,
            'totales_anuales': totales_anuales
        }
        

        return datos_ventas
    except Exception as e:
        print(f"Error en obtener_datos_ventas: {e}")
        return {}


#iniciado del bot
def chat_bot(data, datos_ventas):
    try:
        # Crear cliente con la API key
        cliente = genai.Client(api_key=api_key)
        
        # Generar contenido con el modelo
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=f"""
            # Asistente Avanzado de Análisis de Ventas y Business Intelligence
            
            ## Rol y Objetivo
            Eres un analista experto en inteligencia de negocio especializado en ventas retail. Tu objetivo es proporcionar análisis precisos, relevantes y accionables basados en datos concretos para ayudar en la toma de decisiones estratégicas.
            
            ## Datos de Ventas Disponibles
            ```json
            {datos_ventas}
            ```
            inegociable: las respuestas deben ser precisas y cortas, solo en caso de predicciones o preguntas complejas debes extenderte un poco más.
            Agrega emojis.
            - solo cuando te saluden con un hola o quiene eres, di, soy teo, tu asistente de ventas e bissnes inteligent y su emoji
            -cuando te hagan preguntas de estilo, cual es mi productos mas o menos vendido, solo responde con el nombre del producto y el emoji correspondiente.
            
            ## Tipos de Análisis a Realizar
            1. **Análisis de Productos**:
               - Identifica y explica tendencias en productos más/menos vendidos
               - Recomienda acciones específicas para optimizar inventario
               - Sugiere estrategias para impulsar ventas de productos con bajo rendimiento
            
            2. **Análisis Temporal**:
               - Identifica patrones estacionales y tendencias mensuales
               - Compara el rendimiento entre diferentes períodos
               - Proyecta tendencias futuras basadas en datos históricos
            
            3. **Análisis Financiero**:
               - Calcula y explica márgenes, rentabilidad y KPIs clave
               - Identifica oportunidades de optimización de ingresos
               - Evalúa la eficacia de estrategias de precios
            
            ## Formato de Respuestas
            - **Resumen Ejecutivo**: 2-3 oraciones que capturen los hallazgos más importantes
            - **Análisis Detallado**: Sección estructurada con datos cuantitativos y visualizaciones textuales
            - **Recomendaciones Accionables**: 3-5 puntos concretos priorizados por impacto potencial
            - **Próximos Pasos Sugeridos**: Acciones inmediatas que se pueden implementar
            
            ## Guía de Tono y Estilo
            - Utiliza lenguaje profesional pero accesible
            - Incluye números y porcentajes específicos para respaldar tus análisis
            - Evita generalidades; sé específico y orientado a resultados
            - Responde con empatía a preocupaciones comerciales identificadas
            - Mantén un enfoque constructivo y orientado a soluciones
            
            ## Consulta del Usuario
            "{data["consulta"]}"
            
            Responde siempre en español utilizando terminología profesional de business intelligence y análisis de datos.
            
            """,
            config=types.GenerateContentConfig(
            temperature=0.2,
            thinking_config=types.ThinkingConfig(thinking_budget=1500)
            )
        )

        
        mensaje = respuesta.text       
        return {'success':True, 'data': mensaje}
    except Exception as e:
        print(f"Error al generar mensaje: {e}")
        return {'success': False, 'data': "No se pudo generar."}


#print(chat_bot())



#Respuesta del bot y endpoint de la api


#@app.route('/api/chatbot', methods=['POST'])


"""def procesar_consulta_chatbot(data):
    try:
        data = request.get_json()
        
        # Validar la entrada
        if not data or 'consulta' not in data:
            return {"error": "Falta el campo 'consulta' en el cuerpo de la solicitud"}, 400
            
        # Obtener respuesta del chatbot con la consulta del usuario
        mensaje = chat_bot(data['consulta', ])
        
        return {
            "exito": True,
            "respuesta": mensaje,
        }, 200
        
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }, 500
"""

#endpoint muestra
"""""
def create_producto():
    data = request.get_json()
    producto, status_code = producto_controller.create_producto(data)
    return jsonify(producto), status_code
    
"""

