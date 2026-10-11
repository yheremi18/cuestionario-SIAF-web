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

# Estilos CSS personalizados para replicar el modo oscuro y tarjetas de colores
st.markdown("""
    <style>
    .stApp { background-color: #291835; color: #ffffff; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff; }
    
    /* Botones de opciones estilo tarjeta */
    div.stButton > button {
        width: 100%;
        height: 90px;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        color: white !important;
        border: none !important;
        margin-bottom: 10px;
    }
    
    /* Colores personalizados para los 4 botones */
    div.stButton > button[key="btn_0"] { background-color: #2d82b7 !important; }
    div.stButton > button[key="btn_1"] { background-color: #32a29b !important; }
    div.stButton > button[key="btn_2"] { background-color: #dfa634 !important; }
    div.stButton > button[key="btn_3"] { background-color: #d8536d !important; }
    
    .stButton > button:hover { opacity: 0.95; transform: scale(1.01); }
    </style>
""", unsafe_allow_html=True)

# Inicializar variables globales en la sesión de Streamlit
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

    # Generar opciones solo una vez por pregunta
    if not st.session_state.respondido and len(st.session_state.opciones) == 0:
        otros = [k for k in TIPOS_OPERACION.keys() if k != codigo_actual]
        distractores = random.sample(otros, 3)
        opts = [TIPOS_OPERACION[k][0] for k in distractores + [codigo_actual]]
        random.shuffle(opts)
        st.session_state.opciones = opts

    col1, col2 = st.columns(2)

    # Renderizar los 4 botones en una cuadrícula de 2x2
    for idx, opt in enumerate(st.session_state.opciones):
        columna = col1 if idx % 2 == 0 else col2
        with columna:
            if st.button(opt, key=f"btn_{idx}", disabled=st.session_state.respondido):
                st.session_state.respondido = True
                st.session_state.seleccion = opt
                if opt == nombre_correcto:
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
        st.markdown("### ❌ Respuestas Incorrectas")
        if not st.session_state.errores:
            st.write("¡Perfecto! Sin errores.")
        else:
            for cod in st.session_state.errores:
                st.write(f"• **[{cod}]** {TIPOS_OPERACION[cod][0]}")

    st.divider()
    if st.button("↻ Reiniciar Cuestionario", type="primary"):
        reiniciar_juego()
        st.rerun()