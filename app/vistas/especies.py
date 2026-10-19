import streamlit as st

from sdm import config as C
from sdm import data as D
from sdm import graficos as G
from sdm import ui
from sdm.theme import T

esp = ui.selector_especie("esp_ficha")
info = C.ESPECIES[esp]
pres = D.presencias(esp)
bit = D.tabla("04_bitacora_limpieza")
bit = bit[bit["Especie"] == info["nombre"]]
descargados = int(bit["Registros"].iloc[0]) if len(bit) else 0
vars_ = D.variables_de(esp)
r_m = D.tabla("06_area_M")
r_m = r_m[r_m["Especie"] == info["nombre"]]

ui.espacio()
datos = [
    (f"{descargados:,}".replace(",", " "), "registros descargados de GBIF e iNaturalist"),
    (f"{len(pres)}", "presencias tras la limpieza, separadas al menos 5 km"),
    (ui.fmt_km2(float(r_m["Área aprox. (km²)"].iloc[0])) if len(r_m) else "—", "km² de área accesible M (100 km alrededor de las presencias)"),
    (f"{len(vars_)}", "variables ambientales no redundantes para el modelo"),
]
foto_col, texto_col = st.columns([1, 1.35], gap="large", vertical_alignment="center")
with foto_col:
    st.html(f'<div class="sdm-ficha sdm-revela">{ui.foto_html(esp)}</div>')
with texto_col:
    st.html(
        '<div class="sdm-entra">'
        f'<h1 class="sdm-display" style="font-size:var(--step-title);max-width:11ch">{info["comun"]}</h1>'
        f'<p class="sdm-lead" style="margin-top:16px"><span class="sdm-sci">{info["nombre"]}</span> · {info["grupo"]}</p>'
        f'<p class="sdm-body" style="margin-top:14px;color:var(--muted)">{info["habitat"]}</p>'
        '<dl class="sdm-datos" style="margin-top:44px">'
        + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for v, k in datos)
        + "</dl></div>"
    )

# ---------- limpieza ----------
ui.seccion()
c1, c2 = st.columns([1, 1.4], gap="large")
with c1:
    ui.titulo(
        "De cientos de registros a unas decenas",
        "Casi todo lo que se descarta son repeticiones: la misma especie anotada muchas veces en el mismo mirador o sendero. "
        "Si se dejaran, el modelo aprendería dónde van los observadores y no dónde vive la especie.",
    )
    ui.espacio()
    ui.nota(
        "iNaturalist desplaza al azar unos 22 km las coordenadas de especies amenazadas; como eso es más que una celda del mapa, "
        "esos registros se excluyen."
    )
with c2:
    ui.grafico(G.embudo(esp), key=f"embudo_{esp}")

# ---------- dónde ----------
ui.seccion()
ui.titulo(
    "Presencias y pseudoausencias",
    "Los modelos necesitan ejemplos de “aquí no”. Como nadie registra ausencias, se eligen puntos dentro del área accesible M "
    "con tres criterios distintos. Cambia el criterio para ver dónde caen.",
)
ui.espacio()
opciones = {"ninguna": "Solo presencias", "aleatoria": "Aleatoria", "buffer": "Buffer", "ambiental": "Ambiental"}
estr = ui.segmentado("Pseudoausencias", list(opciones), f"pseudo_{esp}", default="buffer", format_func=opciones.get,
                     label_visibility="collapsed")
m1, m2 = st.columns([1.5, 1], gap="large")
with m1:
    ui.grafico(G.mapa_puntos(esp, None if estr == "ninguna" else estr), key=f"puntos_{esp}")
with m2:
    st.html(
        '<p class="sdm-leyenda">'
        f'<span><i style="background:{T["ink"]}"></i>Presencia</span>'
        f'<span><i style="background:transparent;box-shadow:inset 0 0 0 2px {T["accent"]}"></i>Pseudoausencia</span>'
        f'<span><b style="background:transparent;border-top:2px dotted {T["ink"]};height:0;border-radius:0"></b>Límite de M</span>'
        "</p>"
    )
    ui.espacio()
    if estr == "ninguna":
        st.html(f'<p class="sdm-body">{len(pres)} presencias. Cada una ocupa una celda distinta y está a 5 km o más de la siguiente.</p>')
    else:
        st.html(f'<p class="sdm-head" style="font-size:1.375rem">{C.ESTRATEGIAS[estr]}</p>'
                f'<p class="sdm-body" style="margin-top:8px">{C.DESCRIPCION_ESTRATEGIA[estr]}</p>')
        ui.espacio()
        ui.nota(f"Proporción 1:1: {len(pres)} pseudoausencias para {len(pres)} presencias. Nunca se usa una celda que tiene una presencia.")

# ---------- ambiente ----------
ui.seccion()
ui.titulo(
    "En qué ambiente aparece",
    "Cada variable que usó el modelo, comparando las presencias con las pseudoausencias tipo buffer. "
    "Cuanto menos se solapan los dos grupos, más útil es la variable para separarlos.",
)
ui.espacio()
d1, d2 = st.columns([1.5, 1], gap="large")
with d1:
    ui.grafico(G.distribuciones(esp, "buffer"), key=f"dist_{esp}")
    st.html(
        '<p class="sdm-leyenda">'
        f'<span><i style="background:{T["ink"]}"></i>Presencias</span>'
        f'<span><i style="background:transparent;box-shadow:inset 0 0 0 2px {T["accent"]}"></i>Pseudoausencias (buffer)</span>'
        "</p>"
    )
with d2:
    partes = []
    for v in vars_:
        nombre, unidad = C.VARIABLES[v]
        partes.append(f'<dt>{nombre} <span style="color:var(--muted);font-weight:400">· {v}</span></dt>'
                      f'<dd>{C.LECTURA_VARIABLE.get(v, "")}</dd>')
    st.html(f'<dl class="sdm-glosario" style="grid-template-columns:1fr">'
            + "".join(f"<div>{p}</div>" for p in partes)
            + "</dl>")

# ---------- importancia ----------
ui.seccion()
fig_imp, modelo_imp = G.importancia(esp)
i1, i2 = st.columns([1, 1.4], gap="large")
with i1:
    ui.titulo(
        "Qué variable pesa más",
        f"Para el mejor modelo de esta especie ({C.NOMBRE_MODELO[modelo_imp]}) se desordena una variable a la vez y se mide "
        "cuánto empeora el AUC-ROC. Si al desordenarla el modelo casi no cambia, la variable no aportaba.",
    )
    ui.espacio()
    ui.nota("Promedio sobre los pliegues de validación espacial; la línea es una desviación estándar.")
with i2:
    ui.grafico(fig_imp, key=f"imp_{esp}")

# ---------- variables eliminadas ----------
ui.seccion()
sel = D.tabla("07_seleccion_variables")
sel = sel[sel["Especie"] == info["nombre"]]
ui.titulo(
    f"Por qué solo {len(vars_)} variables",
    "De las 20 capas de WorldClim muchas dicen casi lo mismo (por ejemplo, la temperatura media y la del trimestre más cálido). "
    "Se quitan las redundantes con Pearson ≥ 0.7 y luego VIF ≥ 5, calculados sobre las celdas de M y no sobre las pocas presencias.",
)
ui.espacio()
with st.expander(f"Ver las {len(sel)} variables eliminadas y el motivo"):
    tab = sel[["Variable", "Eliminada en", "Motivo"]].copy()
    tab.insert(1, "Descripción", tab["Variable"].map(lambda v: C.VARIABLES.get(v, ("",))[0]))
    st.dataframe(tab, hide_index=True, width="stretch")

ui.pie()
