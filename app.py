import streamlit as st
import random

# Base de datos oficial de Tipos de Operación SIAF
TIPOS_OPERACION = {
    "A": ("ENCARGO INTERNO", "Entrega de dinero con cargo a de rendir cuentas a personal de la Entidad (no incluye viáticos)."),
    "AV": ("ENCARGO INTERNO PARA VIATICOS", "Entrega de dinero a personal de la Entidad con cargo a de rendir cuentas por viáticos."),
    "C": ("GASTO-FONDO FIJO PARA CAJA CHICA (APERTURA Y/O AMPLIACIONES)", "Registro de la Apertura y/o Ampliaciones del Fondo Fijo para Caja Chica."),
    "EO": ("ENCARGO OTORGADO", "Para encargos otorgados a UEs que cuentan con el SIAF, aperturan una Cuenta Central de Encargo y Cuentas de Reversión."),
    "N": ("GASTO-ADQUISICION DE BIENES Y SERVICIOS", "Operaciones de gasto (adquisición de bienes o prestación de servicios) que afectan el presupuesto. El Proveedor es identificado por su RUC cuando es nacional o con un código de proveedor cuando es extranjero."),
    "OG": ("GASTO-OTROS GASTOS DEFINITIVOS (SIN PROVEEDOR)", "Operaciones de gastos con afectación presupuestal, diferentes a Planillas. Ejemplo: Gastos Bancarios, Pagos de Sentencias Judiciales, Subvenciones, etc."),
    "ON": ("GASTO-PLANILLAS", "Pago de Planillas de Haberes, Pensionistas, Racionamiento, Movilidad, etc."),
    "RC": ("GASTO-FONDO CAJA CHICA (RENDICION Y REEMBOLSO)", "Rendiciones del Fondo de Caja Chica, el Sistema controla que no supere 3 veces el monto del fondo."),
    "SD": ("SERVICIO DE LA DEUDA", "Pago de Deuda Pública, interna o externa, tanto el principal como los intereses."),
    "TF": ("TRANSFERENCIA FINANCIERA OTORGADA", "Para el registro de Transferencias Financieras Otorgadas por las Entidades, identificando a la Entidad a quien se le otorga la transferencia."),
    "S": ("GASTO- SIN CLASIFICADOR", "Operaciones de gastos sin afectación presupuestal. etc."),
    "TC": ("TRANSFERENCIA ENTRE CUENTAS BANCARIAS", "Transferencia entre sus Cuentas Bancarias, ya sea dentro de una misma Entidad Financiera o entre diferentes Entidades Financieras."),
    "YC": ("INGRESO-SIN CLASIFICADOR", "Operaciones de ingreso sin afectación presupuestal."),
    "Y/G": ("OPERACIÓN GASTO/INGRESO", "Registro de operaciones sin afectación presupuestal que involucran gasto e ingresos, se registran en un mismo Expediente."),
    "Y": ("INGRESO-OPERACIONES VARIAS", "Operaciones de Ingresos."),
    "YF": ("TRANSFERENCIA FINANCIERA RECIBIDA", "Registro de la Transferencia Financiera Recibida, identificando a la UE quien le entregó la transferencia."),
    "YT": ("INGRESOS TRANSFERENCIA", "Transferencias de ingresos de una UE a su Pliego o entre UEs. Convenio para la transferencia de parte de lo recaudado."),
    "YV": ("IGV-REBAJA INGRESOS X PAGO A SUNAT", "Pago del IGV a la SUNAT.")
}

st.set_page_config(page_title="Cuestionario SIAF", page_icon="📝", layout="centered")

# Estilos CSS con asignación directa por clase 'st-key' de Streamlit
st.markdown("""
    <style>
    /* Fondo principal morado oscuro */
    .stApp { 
        background-color: #291835 !important; 
    }
    div[data-testid="stMarkdownContainer"] p { 
        color: #ffffff !important; 
    }
    
    /* Reglas generales para los botones de opciones */
    .st-key-btn_0 button, .st-key-btn_1 button, .st-key-btn_2 button, .st-key-btn_3 button {
        width: 100% !important;
        height: 110px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        transition: transform 0.1s ease, opacity 0.1s ease !important;
    }

    /* BOTÓN 1: AZUL */
    .st-key-btn_0 button, .st-key-btn_0 button:disabled {
        background-color: #2d82b7 !important;
        color: #ffffff !important;
    }

    /* BOTÓN 2: VERDE AGUA */
    .st-key-btn_1 button, .st-key-btn_1 button:disabled {
        background-color: #32a29b !important;
        color: #ffffff !important;
    }

    /* BOTÓN 3: AMARILLO */
    .st-key-btn_2 button, .st-key-btn_2 button:disabled {
        background-color: #dfa634 !important;
        color: #ffffff !important;
    }

    /* BOTÓN 4: ROSA */
    .st-key-btn_3 button, .st-key-btn_3 button:disabled {
        background-color: #d8536d !important;
        color: #ffffff !important;
    }

    /* Efecto al pasar el cursor */
    .st-key-btn_0 button:hover, .st-key-btn_1 button:hover, 
    .st-key-btn_2 button:hover, .st-key-btn_3 button:hover {
        opacity: 0.9 !important;
        transform: scale(1.02) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialización de la sesión
if "iniciado" not in st.session_state:
    st.session_state.preguntas = list(TIPOS_OPERACION.keys())
    random.shuffle(st.session_state.preguntas)
    st.session_state.indice = 0
    st.session_state.aciertos = []
    st.session_state.errores = []
    st.session_state.respondido = False
    st.session_state.opciones = []
    st.session_state.iniciado = True

total_preguntas = len(st.session_state.preguntas)

def reiniciar_juego():
    st.session_state.preguntas = list(TIPOS_OPERACION.keys())
    random.shuffle(st.session_state.preguntas)
    st.session_state.indice = 0
    st.session_state.aciertos = []
    st.session_state.errores = []
    st.session_state.respondido = False
    st.session_state.opciones = []

# PANTALLA DE PREGUNTAS
if st.session_state.indice < total_preguntas:
    codigo_actual = st.session_state.preguntas[st.session_state.indice]
    nombre_correcto, descripcion = TIPOS_OPERACION[codigo_actual]

    st.caption(f"Pregunta {st.session_state.indice + 1} de {total_preguntas}")
    st.markdown("### ¿A qué tipo de operación corresponde la abreviatura?")
    st.markdown(f"<h1 style='text-align: center; font-size: 55px; color: #ffffff;'>[{codigo_actual}]</h1>", unsafe_allow_html=True)
    st.divider()

    # Generar opciones (1 correcta y 3 distractores)
    if not st.session_state.respondido and len(st.session_state.opciones) == 0:
        otros = [k for k in TIPOS_OPERACION.keys() if k != codigo_actual]
        distractores = random.sample(otros, 3)
        opts = [TIPOS_OPERACION[k][0] for k in distractores + [codigo_actual]]
        random.shuffle(opts)
        st.session_state.opciones = opts

    # Fila 1 de botones
    c1, c2 = st.columns(2)
    with c1:
        if st.button(st.session_state.opciones[0], key="btn_0", disabled=st.session_state.respondido):
            st.session_state.respondido = True
            st.session_state.seleccion = st.session_state.opciones[0]
            if st.session_state.opciones[0] == nombre_correcto:
                st.session_state.aciertos.append(codigo_actual)
            else:
                st.session_state.errores.append(codigo_actual)
            st.rerun()

    with c2:
        if st.button(st.session_state.opciones[1], key="btn_1", disabled=st.session_state.respondido):
            st.session_state.respondido = True
            st.session_state.seleccion = st.session_state.opciones[1]
            if st.session_state.opciones[1] == nombre_correcto:
                st.session_state.aciertos.append(codigo_actual)
            else:
                st.session_state.errores.append(codigo_actual)
            st.rerun()

    # Fila 2 de botones
    c3, c4 = st.columns(2)
    with c3:
        if st.button(st.session_state.opciones[2], key="btn_2", disabled=st.session_state.respondido):
            st.session_state.respondido = True
            st.session_state.seleccion = st.session_state.opciones[2]
            if st.session_state.opciones[2] == nombre_correcto:
                st.session_state.aciertos.append(codigo_actual)
            else:
                st.session_state.errores.append(codigo_actual)
            st.rerun()

    with c4:
        if st.button(st.session_state.opciones[3], key="btn_3", disabled=st.session_state.respondido):
            st.session_state.respondido = True
            st.session_state.seleccion = st.session_state.opciones[3]
            if st.session_state.opciones[3] == nombre_correcto:
                st.session_state.aciertos.append(codigo_actual)
            else:
                st.session_state.errores.append(codigo_actual)
            st.rerun()

    # Retroalimentación post-respuesta
    if st.session_state.respondido:
        st.write("")
        if st.session_state.seleccion == nombre_correcto:
            st.success("¡Respuesta Correcta! ✔️")
        else:
            st.error(f"Respuesta Incorrecta ❌. La respuesta correcta era: **{nombre_correcto}**")

        st.info(f"**Descripción Oficial:**\n\n_{descripcion}_")

        btn_label = "Siguiente Pregunta ➔" if st.session_state.indice + 1 < total_preguntas else "Ver Resultados 📊"
        if st.button(btn_label, type="primary"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.opciones = []
            st.rerun()

# PANTALLA DE RESUMEN FINAL
else:
    puntaje = len(st.session_state.aciertos)
    st.markdown("<h2 style='text-align: center;'>🏆 Resumen Final del Cuestionario</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #dfa634;'>{puntaje} / {total_preguntas}</h1>", unsafe_allow_html=True)
    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### ✅ Respuestas Correctas")
        if not st.session_state.aciertos:
            st.write("Ninguna.")
        else:
            for cod in st.session_state.aciertos:
                st.write(f"• **[{cod}]** {TIPOS_OPERACION[cod][0]}")

    with col_b:
        st.markdown("### ❌
