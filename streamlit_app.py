import streamlit as st
import json
from datetime import datetime

class MattressSalesAssistant:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
        
    def setup_page(self):
        st.set_page_config(
            page_title="Asistente Ventas Colchones + IA",
            page_icon="🛏️",
            layout="wide"
        )
        
    def initialize_session_state(self):
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
        if 'conversacion_actual' not in st.session_state:
            st.session_state.conversacion_actual = []

    def run(self):
        st.sidebar.title("🔧 Modo de Acceso")
        modo = st.sidebar.radio("Selecciona el modo:", ["MODO JEFE", "MODO COMERCIAL"])
        
        if modo == "MODO JEFE":
            self.modo_jefe()
        else:
            self.modo_comercial()

    def modo_jefe(self):
        st.title("🎛️ MODO JEFE - Panel de Control")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 Configurar Prioridades")
            nuevas_prioridades = st.text_area(
                "Prioridades de la semana (una por línea):",
                value="\n".join(st.session_state.estrategia['prioridades_semana']),
                height=150
            )
            
            st.subheader("📋 Proceso de Venta")
            nuevo_proceso = st.text_area(
                "Pasos del proceso (uno por línea):", 
                value="\n".join(st.session_state.estrategia['proceso_venta']),
                height=150
            )
            
            if st.button("💾 Guardar Estrategia", type="primary"):
                st.session_state.estrategia['prioridades_semana'] = [p.strip() for p in nuevas_prioridades.split('\n') if p.strip()]
                st.session_state.estrategia['proceso_venta'] = [p.strip() for p in nuevo_proceso.split('\n') if p.strip()]
                st.success("✅ Estrategia actualizada para todos los comerciales")
        
        with col2:
            st.subheader("👥 Comerciales Activos")
            st.metric("Conectados", "3/20")
            st.metric("Ventas Hoy", "7")
            st.metric("Tasa Conversión", "35%")
            
            st.subheader("📊 IA - Recomendaciones")
            st.info("""
            **Sugerencias basadas en datos:**
            - 70% de clientes preguntan por colchones frescos
            - Objeción 'precio' aparece en 60% de ventas  
            - Cierres aumentan 25% con prueba gratuita
            """)

    def modo_comercial(self):
        st.title("🛏️ Asistente de Ventas + IA")
        
        # Barra superior con info clave
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🎯 **Prioridades:** " + " | ".join(st.session_state.estrategia['prioridades_semana'][:2]))
        with col2:
            st.warning("📋 **Paso Actual:** " + st.session_state.estrategia['proceso_venta'][0])
        with col3:
            st.success("💡 **IA Activa:** Lista para consultas")
        
        st.divider()
        
        # Área principal - Asistente IA
        col_izq, col_der = st.columns([2, 1])
        
        with col_izq:
            st.header("🤖 Asistente IA - Consultas en Tiempo Real")
            
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
                    "Otra situación..."
                ]
            )
            
            detalles = st.text_area("Proporciona más detalles:", placeholder="Ej: Cliente dice que nuestro colchón es caro comparado con la competencia...")
            
            if st.button("🔍 Consultar a IA", type="primary"):
                if detalles:
                    respuesta_ia = self.consultar_ia(situacion, detalles)
                    st.session_state.conversacion_actual.append({
                        'situacion': situacion,
                        'detalles': detalles, 
                        'respuesta': respuesta_ia,
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
            
            # Mostrar conversación
            st.subheader("💬 Historial Consulta")
            for consulta in reversed(st.session_state.conversacion_actual[-3:]):
                with st.expander(f"🕐 {consulta['timestamp']} - {consulta['situacion']}"):
                    st.write(f"**Comercial:** {consulta['detalles']}")
                    st.write(f"**IA:** {consulta['respuesta']}")
        
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
            
            # Acciones rápidas
            st.write("**🚀 Acciones Sugeridas**")
            st.button("📞 Llamar para seguimiento")
            st.button("📧 Enviar catálogo digital") 
            st.button("🎁 Ofrecer promoción especial")

    def consultar_ia(self, situacion, detalles):
        consejos = {
            "Cliente indeciso - necesita ayuda": [
                "Haz 2-3 preguntas más profundas sobre sus hábitos de sueño",
                "Ofrece probar 2 modelos contrastados (firme/suave)",
                "Cuenta un caso de éxito de cliente similar",
                "Conecta con la PRIORIDAD: Prueba 30 noches sin riesgo"
            ],
            "Objeción de precio - no ve el valor": [
                "Divide el precio en costo por noche de sueño",
                "Recuerda la garantía de 12 años vs competencia (8-10 años)",
                "Destaca el ahorro en salud a largo plazo",
                "Aplica PRIORIDAD: Garantía 12 años como diferencial"
            ],
            "Cliente compara con competencia": [
                "Pregunta: ¿Qué características valora más?",
                "Enfócate en nuestra tecnología CoolMax exclusiva",
                "Ofrece prueba comparativa en tienda",
                "Destaca PRIORIDAD: Tecnología refrescante superior"
            ],
            "No detecto necesidades claras": [
                "Usa preguntas abiertas: '¿Cómo sería su sueño ideal?'",
                "Pregunta por molestias al despertar (calor, dolor)",
                "Habla de beneficios emocionales (energía, productividad)",
                "Aplica PRIORIDAD: Enfoque en colchones refrescantes"
            ],
            "Momento de cierre - cómo proceder": [
                "Pregunta de elección: ¿Prefiere entrega viernes o sábado?",
                "Ofrece financiación a 36 meses sin intereses",
                "Recuerda la prueba de 30 noches sin riesgo",
                "Usa PRIORIDAD: Cierre con prueba 30 noches"
            ],
            "Cliente con problemas de espalda": [
                "Enfoca en las 7 zonas de firmeza para soporte lumbar",
                "Pregunta por tipo específico de dolor (lumbar, cervical)",
                "Ofrece prueba con colchón de firmeza media-alta",
                "Conecta con garantía 12 años para tranquilidad"
            ]
        }
        
        respuesta = f"**Análisis IA - {situacion}**\n\n"
        
        if situacion in consejos:
            respuesta += "**Consejos específicos:**\n"
            for consejo in consejos[situacion]:
                respuesta += f"• {consejo}\n"
        else:
            respuesta += "**Estrategia general recomendada:**\n"
            respuesta += "• Mantén la escucha activa\n• Conecta con necesidades emocionales\n• Usa preguntas poderosas\n• Crea urgencia con beneficios\n"
        
        respuesta += f"\n**🎯 Aplica las prioridades del jefe:**\n"
        for prioridad in st.session_state.estrategia['prioridades_semana'][:2]:
            respuesta += f"• {prioridad}\n"
            
        return respuesta

def main():
    assistant = MattressSalesAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
