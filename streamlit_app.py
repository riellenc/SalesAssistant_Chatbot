import streamlit as st
from datetime import datetime
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Asistente Ventas Colchones + IA DeepSeek",
    page_icon="🛏️",
    layout="wide"
)

# Configuración DeepSeek API - REEMPLAZA CON TU API KEY
DEEPSEEK_API_KEY = "tu-api-key-de-deepseek-aqui"  # ← CONSÍGUELA EN platform.deepseek.com
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def consultar_deepseek(situacion, detalles, prioridades):
    """Consulta REAL a DeepSeek API"""
    
    prompt = f"""
    Eres un asistente de ventas experto en colchones. Un comercial te describe esta situación:
    
    SITUACIÓN: {situacion}
    DETALLES: {detalles}
    
    PRIORIDADES DEL JEFE QUE DEBES APLICAR:
    {chr(10).join(f"• {p}" for p in prioridades)}
    
    Proporciona:
    1. Análisis rápido de la situación
    2. 3-4 consejos prácticos y específicos
    3. Cómo aplicar las prioridades del jefe
    4. Frases concretas que puede usar el comercial
    
    Sé directo, práctico y enfocado en resultados de venta.
    """
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "Eres un experto en ventas de colchones con 15 años de experiencia. Das consejos prácticos, específicos y accionables. Siempre aplicas las prioridades del jefe de ventas."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Error en la API DeepSeek: {response.status_code}\n\nMientras tanto, te recomiendo:\n• Escuchar activamente al cliente\n• Conectar con sus necesidades específicas\n• Aplicar las prioridades del jefe: {', '.join(prioridades[:2])}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}\n\n**Consejos generales:**\n• Mantén la calma y escucha\n• Haz preguntas abiertas\n• Enfócate en {prioridades[0] if prioridades else 'resolver necesidades'}"

# Inicializar estado de la sesión
if 'estrategia' not in st.session_state:
    st.session_state.estrategia = {
        'prioridades_semana': [
            "ENFOCARSE EN COLCHONES REFRESCANTES - 70% de clientes preguntan por calor nocturno",
            "DESTACAR GARANTÍA 12 AÑOS - vs 8-10 años de competencia",  
            "CIERRE CON PRUEBA 30 NOCHES - elimina el riesgo del cliente"
        ],
        'proceso_venta': [
            "SALUDO + DIAGNÓSTICO - 3 preguntas clave sobre sueño actual",
            "DEMOSTRACIÓN INTERACTIVA - probar tecnologías en tienda",
            "PERSONALIZACIÓN - conectar necesidades con beneficios", 
            "MANEJO OBJECIONES - respuestas preparadas",
            "CIERRE AVANZADO - prueba 30 noches + financiación"
        ],
        'argumentarios': {
            'tecnologia_refrescante': "Nuestro sistema CoolMax dispersa 30% más calor que memory foam tradicional",
            'garantia': "Garantía 12 años - 3 años más que la competencia promedio",
            'soporte_lumbar': "7 zonas de firmeza para mantener la columna alineada"
        },
        'objeciones': {
            'precio': "Divida el precio: son solo $X por noche de sueño reparador + ahorro en salud",
            'pensarlo': "Le ofrezco prueba 30 noches en casa sin riesgo + financiación a 36 meses"
        }
    }

if 'conversaciones' not in st.session_state:
    st.session_state.conversaciones = []

# Selector de modo
st.sidebar.title("🔧 Modo de Acceso")
modo = st.sidebar.radio("Selecciona el modo:", ["MODO JEFE", "MODO COMERCIAL"])

if modo == "MODO JEFE":
    st.title("🎛️ MODO JEFE - Panel de Control")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Configurar Prioridades")
        nuevas_prioridades = st.text_area(
            "Prioridades de la semana (una por línea):",
            value="\n".join(st.session_state.estrategia['prioridades_semana']),
            height=150,
            key="prioridades_jefe"
        )
        
        st.subheader("📋 Proceso de Venta")
        nuevo_proceso = st.text_area(
            "Pasos del proceso (uno por línea):", 
            value="\n".join(st.session_state.estrategia['proceso_venta']),
            height=150,
            key="proceso_jefe"
        )
        
        if st.button("💾 Guardar Estrategia", type="primary", key="guardar_jefe"):
            st.session_state.estrategia['prioridades_semana'] = [p.strip() for p in nuevas_prioridades.split('\n') if p.strip()]
            st.session_state.estrategia['proceso_venta'] = [p.strip() for p in nuevo_proceso.split('\n') if p.strip()]
            st.success("✅ Estrategia actualizada para todos los comerciales")
    
    with col2:
        st.subheader("👥 Comerciales Activos")
        st.metric("Conectados", "3/20")
        st.metric("Ventas Hoy", "7")
        st.metric("Tasa Conversión", "35%")
        
        st.subheader("🔑 Configuración API")
        st.info("""
        **DeepSeek API:**
        1. Ve a platform.deepseek.com
        2. Consigue tu API Key gratis
        3. Reemplaza en el código
        4. ¡IA real funcionando!
        """)

else:  # MODO COMERCIAL
    st.title("🛏️ Asistente de Ventas + IA DeepSeek")
    
    # Barra superior con info clave
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎯 **Prioridades:** " + " | ".join(st.session_state.estrategia['prioridades_semana'][:2]))
    with col2:
        st.warning("📋 **Paso Actual:** " + st.session_state.estrategia['proceso_venta'][0])
    with col3:
        if DEEPSEEK_API_KEY != "tu-api-key-de-deepseek-aqui":
            st.success("🤖 **IA DeepSeek:** CONECTADA")
        else:
            st.error("🤖 **IA DeepSeek:** CONFIGURA API KEY")
    
    st.divider()
    
    # Área principal - Asistente IA
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.header("🤖 Asistente IA DeepSeek - Consultas Reales")
        
        if DEEPSEEK_API_KEY == "tu-api-key-de-deepseek-aqui":
            st.error("""
            **⚠️ Configura la API Key primero:**
            1. Ve a https://platform.deepseek.com
            2. Regístrate y consigue tu API Key
            3. Reemplaza 'tu-api-key-de-deepseek-aqui' en el código
            4. Recarga la app
            """)
        
        # Situación actual del comercial
        situacion = st.selectbox(
            "Describe tu situación actual:",
            [
                "Cliente indeciso - necesita ayuda",
                "Objeción de precio - no ve el valor", 
                "Cliente compara con competencia",
                "No detecto necesidades claras", 
                "Momento de cierre - cómo proceder",
                "Cliente con problemas de espalda",
                "Cliente preocupado por calor nocturno",
                "Otra situación..."
            ],
            key="situacion_comercial"
        )
        
        detalles = st.text_area(
            "Proporciona más detalles:", 
            placeholder="Ej: Cliente dice que nuestro colchón es caro comparado con la competencia, tiene budget de $800...",
            key="detalles_comercial"
        )
        
        if st.button("🔍 Consultar a IA DeepSeek", type="primary", key="consultar_ia"):
            if not detalles.strip():
                st.warning("⚠️ Por favor describe la situación para obtener ayuda de la IA")
            elif DEEPSEEK_API_KEY == "tu-api-key-de-deepseek-aqui":
                st.error("❌ Configura primero la API Key de DeepSeek")
            else:
                with st.spinner("🤖 Consultando a DeepSeek AI..."):
                    respuesta_ia = consultar_deepseek(
                        situacion, 
                        detalles, 
                        st.session_state.estrategia['prioridades_semana']
                    )
                    
                    nueva_consulta = {
                        'situacion': situacion,
                        'detalles': detalles, 
                        'respuesta': respuesta_ia,
                        'timestamp': datetime.now().strftime("%H:%M"),
                        'prioridades': st.session_state.estrategia['prioridades_semana'][:2]
                    }
                    st.session_state.conversaciones.append(nueva_consulta)
                
                st.success("✅ Respuesta recibida de DeepSeek AI")
        
        # Mostrar conversación
        st.subheader("💬 Historial de Consultas")
        if not st.session_state.conversaciones:
            st.info("📝 Aún no hay consultas. ¡Haz tu primera consulta a la IA!")
        else:
            for i, consulta in enumerate(reversed(st.session_state.conversaciones[-3:])):
                with st.expander(f"🕐 {consulta['timestamp']} - {consulta['situacion']}", expanded=i==0):
                    st.write(f"**📞 Comercial:** {consulta['detalles']}")
                    st.divider()
                    st.write(f"**🤖 IA DeepSeek:** {consulta['respuesta']}")
    
    with col_der:
        st.header("🎯 Estrategia del Jefe")
        
        st.write("**Prioridades de la semana:**")
        for i, prioridad in enumerate(st.session_state.estrategia['prioridades_semana'], 1):
            st.write(f"{i}. {prioridad}")
        
        st.divider()
        
        st.write("**Proceso de venta:**")
        for paso in st.session_state.estrategia['proceso_venta']:
            st.write(f"→ {paso}")
        
        st.divider()
        
        st.write("**Argumentarios clave:**")
        for key, argumento in st.session_state.estrategia['argumentarios'].items():
            st.write(f"• {argumento}")
        
        st.divider()
        
        st.write("**🚀 Acciones Rápidas**")
        if st.button("📞 Llamar para seguimiento", key="llamar"):
            st.info("💡 Sugerencia: Programa llamada en 2-3 días")
        if st.button("📧 Enviar catálogo digital", key="catalogo"):
            st.info("💡 Incluye modelos refrescantes y garantías")
        if st.button("🎁 Ofrecer promoción especial", key="promocion"):
            st.info("💡 Destaca prueba 30 noches + financiación")

# Información de configuración en sidebar
st.sidebar.divider()
st.sidebar.info("""
**🔧 Para conectar con IA real:**
1. Ve a platform.deepseek.com
2. Consigue API Key gratis
3. Reemplaza en línea 13 del código
4. ¡Consulta inteligente activa!
""")
