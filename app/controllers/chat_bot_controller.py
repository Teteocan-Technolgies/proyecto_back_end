from dotenv import load_dotenv
from google import genai
from flask import Flask, request, jsonify
from google.genai import types



#Necesito datos de la base de datos para que el bot pueda responder a las preguntas del usuario
load_dotenv()

respuesta_usario = "Quiero un analisis descriptivo de las ventas, de forma sencilla de entender"    #Agregen los datos de las tablos 


api_key = 'AIzaSyCRcJxhvCHlho2GHmmQcKSpo9UInH1Q3A0' # inicio de api key de geminis

#cambiar por los datos de la base
# Datos de los productos más vendidos



#datos = [["vendidos"] #maximo 5 productos ] mas y menos




productos_mas_vendidos = { #ingresar datos de la base
    'Producto A': 1500,
    'Producto B': 1200,
    'Producto C': 1000,
    'Producto D': 850,
    'Producto E': 700
}

# Datos de los productos menos vendidos
productos_menos_vendidos = {
    'Producto V': 120,
    'Producto W': 105,
    'Producto X': 90,
    'Producto Y': 75,
    'Producto Z': 50
}

# Datos generales de ventas por trimestre y producto
datos_ventas = {
    'Q1': {
        'Producto A': 350, 'Producto B': 280, 'Producto C': 230, 
        'Producto D': 190, 'Producto E': 160, 'Producto V': 30,
        'Producto W': 25, 'Producto X': 20, 'Producto Y': 18, 'Producto Z': 12
    },
    'Q2': {
        'Producto A': 380, 'Producto B': 310, 'Producto C': 250, 
        'Producto D': 210, 'Producto E': 170, 'Producto V': 32,
        'Producto W': 28, 'Producto X': 22, 'Producto Y': 19, 'Producto Z': 13
    },
    'Q3': {
        'Producto A': 420, 'Producto B': 330, 'Producto C': 270, 
        'Producto D': 230, 'Producto E': 190, 'Producto V': 29,
        'Producto W': 27, 'Producto X': 24, 'Producto Y': 20, 'Producto Z': 12
    },
    'Q4': {
        'Producto A': 350, 'Producto B': 280, 'Producto C': 250, 
        'Producto D': 220, 'Producto E': 180, 'Producto V': 29,
        'Producto W': 25, 'Producto X': 24, 'Producto Y': 18, 'Producto Z': 13
    }
}

# Ventas totales anuales para los últimos 5 años
ventas_totales_anuales = {
    '2019': 3800000,
    '2020': 3200000,
    '2021': 4100000,
    '2022': 4500000,
    '2023': 4800000
}

# Ventas totales mensuales del año actual
ventas_totales_mensuales = {
    'Enero': 380000,
    'Febrero': 360000,
    'Marzo': 420000,
    'Abril': 390000,
    'Mayo': 410000,
    'Junio': 450000,
    'Julio': 470000,
    'Agosto': 490000,
    'Septiembre': 460000,
    'Octubre': 430000,
    'Noviembre': 510000,
    'Diciembre': 530000
}

# Ventas totales por categoría
ventas_total_G = { #total de ventas y total en $
    'Electrónica': 2100000,
    'Hogar': 1500000,
    'Deportes': 900000,
    'Juguetes': 750000,
    'Ropa': 650000
}


datos_generales = {
    'productos_mas_vendidos': productos_mas_vendidos,
    'datos_ventas': datos_ventas,
    'productos_menos_vendidos': productos_menos_vendidos,
    "Ventas Totales anuales": ventas_totales_anuales,
    "Ventas Totales mensuales": ventas_totales_mensuales,
    "ventas total G" : ventas_total_G 
}



#iniciado del bot
def chat_bot(datos_generales=datos_generales, respuesta_usario=respuesta_usario):
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
            
            -Datos empresariales: {datos_generales}
            -Utiliza exclusivamente estos datos como base para tus análisis y conclusiones.

            Consulta del usuario: "{respuesta_usario}"
            
            -optimaza la resputa para que sea entendible para el usuario, no utilices tecnisismos ni palabras complicadas.
            -Recuerda que la respusta debe ser sencilla y corta para que el usuario pueda entenderla sin problemas.
            
            
            """,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=1000))
        ),

        
        mensaje = respuesta [0].text       
        return mensaje
    except Exception as e:
        print(f"Error al generar mensaje: {e}")
        return "No se pudo generar."


print(chat_bot())



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