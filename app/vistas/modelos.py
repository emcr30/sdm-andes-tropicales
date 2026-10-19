import streamlit as st

from sdm import config as C
from sdm import data as D
from sdm import graficos as G
from sdm import ui
from sdm.theme import T

ui.espacio()
st.html(
    '<div class="sdm-entra">'
    '<h1 class="sdm-display" style="font-size:var(--step-title)">Cómo se compararon los modelos</h1>'
    '<p class="sdm-lead" style="margin-top:16px">Random Forest, SVM, LightGBM y MaxEnt recibieron exactamente los mismos datos. '
    "La diferencia está en cómo se les tomó el examen.</p>"
    "</div>"
)

# ---------- los cuatro ----------
ui.espacio()
cols = st.columns(4, gap="medium")
for col, m in zip(cols, C.MODELOS):
    with col:
        with st.container(key=f"panel-m-{m}"):
            st.html(f'<p class="sdm-body" style="font-weight:600"><i class="sdm-punto" style="background:{C.COLOR_MODELO[m]}"></i>'
                    f'{C.NOMBRE_MODELO[m]}</p><p class="sdm-note" style="margin-top:6px;color:var(--ink)">{C.DESCRIPCION_MODELO[m]}</p>')

# ---------- inflación ----------
ui.seccion()
c1, c2 = st.columns([1, 2], gap="large")
with c1:
    ui.titulo(
        "Validar al azar engaña",
        "Si se separan los datos de prueba al azar, quedan puntos de prueba a pocos kilómetros de puntos de entrenamiento, "
        "con el mismo clima. El modelo “acierta” porque ya vio un vecino casi idéntico.",
    )
    ui.espacio()
    st.html('<p class="sdm-body">Por eso la tesis prueba cada modelo en <b>bloques geográficos</b> que no vio al entrenar. '
            "El tamaño del bloque sale de la distancia a la que el clima deja de parecerse (semivariograma).</p>")
    ui.espacio()
    met_inf = ui.segmentado("Métrica", ["auc_roc", "tss_opt"], "met_inf", default="auc_roc", format_func=G.METRICAS.get)
with c2:
    ui.grafico(G.inflacion(met_inf), key="inflacion")
    ui.nota("Círculo vacío: validación aleatoria. Círculo lleno: validación espacial. Promedio de las estrategias aleatoria y buffer. "
            "En las aves la caída suele ser clara; en la rana, cuyas presencias están muy agrupadas en Junín, casi no hay diferencia.")

# ---------- pliegues ----------
ui.seccion()
ui.titulo(
    "El resultado, pliegue por pliegue",
    "Cada punto es una prueba sobre un bloque geográfico distinto; la raya es el promedio. "
    "La dispersión importa tanto como el promedio: con pocas presencias, un solo bloque puede cambiar mucho la nota.",
)
ui.espacio()
f1, f2, _ = st.columns([1.2, 1, 1.4], gap="medium")
with f1:
    met = ui.segmentado("Métrica", list(G.METRICAS), "met_pl", default="auc_roc", format_func=G.METRICAS.get)
with f2:
    estr = ui.segmentado("Pseudoausencias", ["buffer", "aleatoria"], "estr_pl", default="buffer", format_func=C.ESTRATEGIAS.get)
ui.grafico(G.pliegues(met, estr), key="pliegues")
g1, g2 = st.columns(2, gap="large")
with g1:
    ui.nota(f"<b>{G.METRICAS[met]}</b>: {C.GLOSARIO['TSS' if met == 'tss_opt' else ('AUC-PR' if met == 'auc_pr' else 'AUC-ROC')]}")
with g2:
    ui.nota(f"<b>Pseudoausencias {C.ESTRATEGIAS[estr].lower()}</b>: {C.DESCRIPCION_ESTRATEGIA[estr]} "
            "La estrategia ambiental no entra al ranking porque separa demasiado fácil.")

# ---------- ranking ----------
ui.seccion()
r1, r2 = st.columns([1, 1.4], gap="large")
t17 = D.tabla("17_mejor_modelo")
with r1:
    ui.titulo(
        "El ranking por especie",
        "En cada especie y estrategia se ordena a los modelos en AUC-ROC, AUC-PR y TSS (1 = mejor) y se promedian los puestos.",
    )
    ui.espacio()
    fr = D.tabla("18_friedman")
    if len(fr):
        pmin = fr["p-valor"].min()
        ui.nota(f"Prueba de Friedman: ningún p-valor baja de 0.05 (el menor es {pmin:.3f}). Con solo tres especies como bloques, "
                "la prueba casi no tiene potencia: no permite afirmar que un modelo sea mejor, solo describir la tendencia.")
with r2:
    filas = ['<div class="sdm-cab" style="grid-template-columns:minmax(0,1.6fr) repeat(4,minmax(0,1fr))"><span>Especie</span>'
             + "".join(f"<span>{C.NOMBRE_MODELO[m]}</span>" for m in C.MODELOS) + "</div>"]
    for _, f in t17.iterrows():
        esp = next(e for e, i in C.ESPECIES.items() if i["nombre"] == f["Especie"])
        celdas = []
        for m in C.MODELOS:
            v = f[f"Puesto promedio {m}"]
            gana = m == f["Mejor modelo"]
            estilo = f'color:{T["ink"]}' if gana else f'color:{T["muted"]};font-weight:400'
            celdas.append(f'<div><div class="v" style="{estilo}">{v:.2f}</div>'
                          f'<div class="k">{"mejor" if gana else "&nbsp;"}</div></div>')
        filas.append('<div class="sdm-fila" style="grid-template-columns:minmax(0,1.6fr) repeat(4,minmax(0,1fr))">'
                     f'<div><div class="t" style="font-size:1.0625rem">{C.ESPECIES[esp]["comun"]}</div>'
                     f'<div class="s sdm-sci">{f["Especie"]}</div></div>' + "".join(celdas) + "</div>")
    st.html(f'<div class="sdm-lista">{"".join(filas)}</div>')
    ui.nota("Puesto promedio (1 = mejor, 4 = peor) en las estrategias aleatoria y buffer con validación espacial.")

# ---------- sensibilidad ----------
fig_s = G.sensibilidad(st.session_state.get("estr_sens", "buffer"))
if fig_s is not None:
    ui.seccion()
    s1, s2 = st.columns([1, 2], gap="large")
    with s1:
        ui.titulo(
            "¿Y si se ajustaban de otra forma?",
            "Se probaron todas las combinaciones de hiperparámetros de la Tabla 5 (2 202 modelos en total). "
            "La caja muestra el rango de AUC-ROC que alcanza cada algoritmo; el rombo, la configuración que se usó.",
        )
        ui.espacio()
        estr_s = ui.segmentado("Pseudoausencias", ["buffer", "aleatoria"], "estr_sens", default="buffer",
                               format_func=C.ESTRATEGIAS.get)
        ui.espacio()
        t20 = D.tabla("20_sensibilidad_ranking")
        cambia = t20[t20["¿Cambia con la mediana?"] == "Sí"]
        if len(cambia):
            ui.nota(f"El mejor modelo solo cambia en {len(cambia)} de {len(t20)} casos (la lechucita: con la mediana de la grilla gana Random Forest en vez de SVM). "
                    "En el resto, el ranking se mantiene.")
    with s2:
        ui.grafico(fig_s, key="sens")
        ui.nota("El máximo de cada caja es optimista: se elige y se evalúa en los mismos pliegues. Por eso se compara la mediana.")

ui.pie()
